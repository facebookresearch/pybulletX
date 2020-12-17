# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import functools
import textwrap
import warnings

import numpy as np

import pybulletX as px  # noqa: F401
import pybullet as p
from .robot_interface_mixin import RobotInterfaceMixin

log = logging.getLogger(__name__)


# convert any list in input arguments to tuple before calling the function
def list_args_to_tuple(f):
    def wrapper(*args, **kwargs):
        args = [tuple(x) if type(x) == list else x for x in args]
        return f(*args, **kwargs)

    return wrapper


class Robot(px.Body, RobotInterfaceMixin):
    # TODO(poweic): maximum force applied when we lock the motor.
    MAX_FORCE = 1e4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._torque_control = False

        self.free_joint_indices = self._get_free_joint_indices()

        self.zero_pose = self._get_zero_joint_position()

        self.set_joint_force_torque_sensor(True)

    def _set_velocity_control(self, max_forces):
        p.setJointMotorControlArray(
            self.id,
            self.free_joint_indices,
            p.VELOCITY_CONTROL,
            forces=max_forces,
            **self._client_kwargs,
        )

    @property
    def torque_control(self):
        return self._torque_control

    @torque_control.setter
    def torque_control(self, enable):
        if self._torque_control == enable:
            return

        self._torque_control = enable
        if enable:
            self._enable_torque_control()
        else:
            self._disable_torque_control()

    def _enable_torque_control(self):
        """
        Please refer to the official pybullet's QuickStart Guide on Google Drive.
        By setting control mode to VELOCITY_CONTROL and max forces to zero, this
        will enable torque control.
        """
        self._set_velocity_control(np.zeros(self.num_dofs))

    def _disable_torque_control(self):
        """
        Restore pybullet's default control mode: "VELOCITY_CONTROL" and zero
        target velocity, and set max force to a huge number (MAX_FORCE). If
        the motor is strong enough (i.e. has large enough torque upper limit),
        this is essentially locking all the motors.
        """
        self._set_velocity_control(np.ones(self.num_dofs) * self.MAX_FORCE)

    @property
    def num_dofs(self):
        return len(self.free_joint_indices)

    @property
    def free_joint_indices(self):
        return self._free_joint_indices

    @free_joint_indices.setter
    def free_joint_indices(self, new_free_joint_indices):
        self._free_joint_indices = new_free_joint_indices

    @functools.lru_cache(maxsize=None)
    def _get_free_joint_indices(self):
        """
        Exclude all fixed joints and return a list of free joint indices
        """
        joint_infos = [self.get_joint_info(i) for i in range(self.num_joints)]
        return [
            info.joint_index for info in joint_infos if info.joint_type != p.JOINT_FIXED
        ]

    @property
    def zero_pose(self):
        return self._zero_pose

    @zero_pose.setter
    def zero_pose(self, new_zero_pose):
        self._zero_pose = new_zero_pose

    def _get_zero_joint_position(self):
        if not self.free_joint_indices:
            return []

        joint_infos = self.get_joint_infos()
        return np.zeros(self.num_dofs).clip(
            min=joint_infos.joint_lower_limit, max=joint_infos.joint_upper_limit,
        )

    def joints_within_limits(self):
        if not self.free_joint_indices:
            return True
        curr = self.get_joint_states().joint_position
        lower = self.get_joint_infos().joint_lower_limit
        upper = self.get_joint_infos().joint_upper_limit
        return np.all(curr >= lower) and np.all(curr <= upper)

    def get_joint_by_name(self, joint_name):
        joints = [self.get_joint_info(_) for _ in range(self.num_joints)]
        joints = {j.joint_name.decode(): j for j in joints}
        return joints[joint_name]

    @list_args_to_tuple
    @functools.lru_cache(maxsize=None)
    def joint_effort_limits(self, joint_indices):
        return self.get_joint_infos(joint_indices).joint_max_force

    def get_joint_infos(self, joint_indices=None):
        """
        Get the joint informations of all controllable joints (`self.free_joint_indices`)
        and return JointInfo, which is a structure of arrays (SoA).
        """
        if joint_indices is None:
            joint_indices = self.free_joint_indices
        return super().get_joint_infos(joint_indices)

    def get_joint_states(self, joint_indices=None):
        """
        Get the states of all controllable joints (`self.free_joint_indices`) and
        return JointState, which is a structure of arrays (SoA).
        """
        if joint_indices is None:
            joint_indices = self.free_joint_indices
        return super().get_joint_states(joint_indices)

    def get_link_states(self, joint_indices=None, **kwargs):
        """
        Get the states of all movable links (`self.free_joint_indices`) and return
        LinkState, which is a structure of arrays (SoA).
        """
        if joint_indices is None:
            joint_indices = self.free_joint_indices
        return super().get_link_states(joint_indices, **kwargs)

    def get_dynamics_infos(self, link_indices=None):
        if link_indices is None:
            link_indices = self.free_joint_indices
        return super().get_dynamics_infos(link_indices)

    def set_joint_force_torque_sensor(self, on_off: bool):
        """
        Enable/Disable joint force torque sensor
        """
        for joint_index in self.free_joint_indices:
            p.enableJointForceTorqueSensor(
                self.id, joint_index, on_off, **self._client_kwargs
            )

    def attach(
        self, new_robot, link_name, position=(0, 0, 0), orientation=(0, 0, 0, 1)
    ):
        """
        Attach a new robot (`new_robot`) to self by creating a fixed joint between
        a specific link (`link_name`) and the base of the new robot.
        """
        assert isinstance(new_robot, Robot)
        link_idx = self.get_joint_index_by_name(link_name)

        link_pos = self.get_link_state(link_idx).link_world_position
        link_pos = np.array(link_pos) + np.array(position)

        new_robot.set_base_pose(link_pos)

        p.createConstraint(
            parentBodyUniqueId=self.id,
            parentLinkIndex=link_idx,
            childBodyUniqueId=new_robot.id,
            childLinkIndex=-1,
            jointType=p.JOINT_FIXED,
            jointAxis=[0, 0, 0],  # ignored for JOINT_FIXED
            parentFramePosition=position,
            childFramePosition=[0, 0, 0],
            parentFrameOrientation=orientation,
            childFrameOrientation=[0, 0, 0, 1],
            **self._client_kwargs,
        )

    def reset(self):
        super().reset()

        for joint_index, joint_angle in zip(self.free_joint_indices, self.zero_pose):
            p.resetJointState(self.id, joint_index, joint_angle, **self._client_kwargs)

        if not self.joints_within_limits():
            log.warning("joint set to positions outside the limits")

    def summarize(self):
        for index in self.free_joint_indices:
            info = self.get_joint_info(index)
            log.info(f"\33[33mJoint #{index}:\33[0m")
            log.info(textwrap.indent(str(info), "  "))
        log.info(f"\33[33m# of DOFs = {self.num_dofs}\33[0m")

    def reset_joint_state(self, *args, **kwargs):
        p.resetJointState(self.id, *args, **kwargs, **self._client_kwargs)

    def set_joint_position(
        self, joint_position, max_forces=None, use_joint_effort_limits=True
    ):
        self.torque_control = False

        """
        Maximum forces applied when mode set to p.POSITION_CONTROL or p.VELOCITY_CONTROL
        can be one of the followings (M for max_forces, U for use_joint_effort_limits)
        1) [M == None, U == True ] use joint effort limit defined in URDF.
           (if not provided in URDF, i.e. joint_max_force all zeros, set I to True and reduce to case 2)
        2) [M == None, U == False] infinite joint effort, which is the default if
           "forces" is not passed as argument to p.setJointMotorControlArray
        3) [M != None, U == True ] custom joint efforts (list of floats), clip
           by the joint effort limits defined in URDF.
        4) [M != None, U == False] same as 3, but ignore joint effort limits in URDF.
        """
        assert not np.all(np.array(max_forces) == 0), "max_forces can't be all zero"

        limits = self.joint_effort_limits(self.free_joint_indices)
        if max_forces is None and np.all(limits == 0):
            warnings.warn(
                "Joint maximum efforts provided by URDF are zeros. "
                "Set use_joint_effort_limits to False"
            )
            use_joint_effort_limits = False

        opts = {}
        if max_forces is None:
            if use_joint_effort_limits:
                # Case 1
                opts["forces"] = limits
            else:
                # Case 2: do nothing
                pass
        else:
            if use_joint_effort_limits:
                # Case 3
                opts["forces"] = np.minimum(max_forces, limits)
            else:
                # Case 4
                opts["forces"] = max_forces

        assert len(self.free_joint_indices) == len(joint_position), (
            f"number of target positions ({len(joint_position)}) should match "
            f"the number of joint indices ({len(self.free_joint_indices)})"
        )

        # If not provided, the default value of targetVelocities, positionGains
        # and velocityGains are 0., 0.1, 1.0, respectively.
        p.setJointMotorControlArray(
            bodyIndex=self.id,
            jointIndices=self.free_joint_indices,
            controlMode=p.POSITION_CONTROL,
            targetPositions=joint_position,
            targetVelocities=np.zeros_like(joint_position),  # default = 0.0
            # positionGains=np.ones_like(joint_position) * 0.1, # default = 0.1
            # velocityGains=np.ones_like(joint_position) * 1.0, # default = 1.0
            **opts,
            **self._client_kwargs,
        )

    def set_joint_torque(self, torque):
        self.torque_control = True

        p.setJointMotorControlArray(
            bodyIndex=self.id,
            jointIndices=self.free_joint_indices,
            controlMode=p.TORQUE_CONTROL,
            forces=torque,
            **self._client_kwargs,
        )
