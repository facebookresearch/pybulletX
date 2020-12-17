# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import numpy as np
from gym.spaces import Box
from attrdict import AttrMap
import functools

from .robot_interface import IRobot, router, SpaceDict


class RobotInterfaceMixin(IRobot):
    @property
    @router
    def action_space(self):
        info = self.get_joint_infos()
        if self.torque_control:
            return SpaceDict(
                joint_torque=Box(
                    low=-info.joint_max_force,
                    high=info.joint_max_force,
                    shape=[self.num_dofs],
                    dtype=np.float64,
                ),
            )
        else:
            return SpaceDict(
                joint_position=Box(
                    low=info.joint_lower_limit,
                    high=info.joint_upper_limit,
                    shape=[self.num_dofs],
                    dtype=np.float64,
                ),
            )

    @property
    def _use_state_space(self):
        if not hasattr(self, "_use_state_space_dict"):
            self._use_state_space_dict = {
                "joint_position": True,
                "joint_velocity": True,
                "joint_reaction_forces": True,
                "applied_joint_motor_torque": True,
            }
        return self._use_state_space_dict

    def configure_state_space(
        self,
        joint_position=None,
        joint_velocity=None,
        joint_reaction_forces=None,
        applied_joint_motor_torque=None,
    ):
        if joint_position is not None:
            self._use_state_space["joint_position"] = joint_position
        if joint_velocity is not None:
            self._use_state_space["joint_velocity"] = joint_velocity
        if joint_reaction_forces is not None:
            self._use_state_space["joint_reaction_forces"] = joint_reaction_forces
        if applied_joint_motor_torque is not None:
            self._use_state_space[
                "applied_joint_motor_torque"
            ] = applied_joint_motor_torque

    @property
    @functools.lru_cache(maxsize=None)
    def full_state_space(self):
        info = self.get_joint_infos()
        return SpaceDict(
            joint_position=Box(
                low=info.joint_lower_limit,
                high=info.joint_upper_limit,
                shape=[self.num_dofs],
                dtype=np.float64,
            ),
            joint_velocity=Box(
                low=-info.joint_max_velocity,
                high=info.joint_max_velocity,
                shape=[self.num_dofs],
                dtype=np.float64,
            ),
            joint_reaction_forces=Box(
                low=-np.inf, high=np.inf, shape=[self.num_dofs, 6], dtype=np.float64
            ),
            applied_joint_motor_torque=Box(
                low=-np.inf, high=np.inf, shape=[self.num_dofs], dtype=np.float64
            ),
        )

    @property
    @router
    def state_space(self):
        full_state_space = self.full_state_space
        return SpaceDict(
            {k: v for k, v in full_state_space.items() if self._use_state_space[k]}
        )

    @router
    def set_actions(self, actions):
        if self.torque_control:
            self.set_joint_torque(actions["joint_torque"])
        else:
            self.set_joint_position(actions["joint_position"])

    @router
    def get_states(self):
        states = self.get_joint_states()
        return AttrMap({k: v for k, v in states.items() if self._use_state_space[k]})
