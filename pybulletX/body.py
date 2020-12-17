# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import warnings
import functools

import pybulletX as px  # noqa: F401
import pybullet as p

log = logging.getLogger(__name__)


def _snake_to_camel(name):
    return "".join(
        word.title() if i > 0 else word for i, word in enumerate(name.split("_"))
    )


class Body:
    def __init__(
        self,
        urdf_path,
        base_position=(0, 0, 0),
        base_orientation=(0, 0, 0, 1),
        use_maximal_coordinates=None,
        use_fixed_base=False,
        flags=0,
        global_scaling=None,
        physics_client: px.Client = None,
    ):
        self.urdf_path = px.helper.find_file(urdf_path)
        self.init_base_position = list(base_position)
        self.init_base_orientation = list(base_orientation)

        self.use_maximal_coordinates = use_maximal_coordinates
        self.use_fixed_base = use_fixed_base
        self.flags = flags
        self.global_scaling = global_scaling

        if physics_client is None:
            physics_client = px.current_client()
        self._physics_client = physics_client

        opts = {
            "file_name": urdf_path,
            "base_position": base_position,
            "base_orientation": base_orientation,
            "use_maximal_coordinates": use_maximal_coordinates,
            "use_fixed_base": use_fixed_base,
            "flags": flags,
            "global_scaling": global_scaling,
        }

        # Turn all keys into camel case
        opts = {_snake_to_camel(k): v for k, v in opts.items() if v is not None}

        if opts["flags"] == 0:
            warnings.warn(
                "By default, Bullet recompute the inertia tensor based on mass "
                "and volume of the collision shape. If you want to use inertia "
                "from file, set flags to p.URDF_USE_INERTIA_FROM_FILE."
            )

        self._id = px.helper.loadURDF(**opts, **self._client_kwargs)

        # getBasePositionAndOrientation != base_position passed to p.loadURDF.
        # See issue https://github.com/bulletphysics/bullet3/issues/2411
        # Call resetBasePositionAndOrientation to fix it.
        self.set_base_pose(self.init_base_position, self.init_base_orientation)

    @property
    def id(self):
        return self._id

    @property
    def physics_client(self):
        return self._physics_client

    @property
    def _client_kwargs(self):
        return {"physicsClientId": self.physics_client.id}

    @property
    def num_joints(self):
        return p.getNumJoints(self.id, **self._client_kwargs)

    @property
    @functools.lru_cache(maxsize=None)
    def _joint_name_to_index(self):
        return {
            j.joint_name.decode(): j.joint_index
            for j in self.get_joint_infos(range(self.num_joints))
        }

    def get_joint_index_by_name(self, joint_name):
        return self._joint_name_to_index[joint_name]

    def get_joint_indices_by_names(self, joint_names):
        return [self._joint_name_to_index[joint_name] for joint_name in joint_names]

    def get_joint_info(self, joint_index):
        """
        Get joint information and return as JointInfo, which is a structure.
        """
        return p.getJointInfo(self.id, joint_index, **self._client_kwargs)

    def get_joint_info_by_name(self, joint_name):
        return self.get_joint_info(self.get_joint_index_by_name(joint_name))

    def get_joint_infos(self, joint_indices):
        """
        Get the joint informations and return JointInfo, which is a structure of arrays (SoA).
        """
        return p.getJointInfos(self.id, joint_indices, **self._client_kwargs)

    def get_joint_state(self, joint_index):
        """
        Get the state of a specific joint and return JointState, which is a structure.
        """
        return p.getJointState(self.id, joint_index, **self._client_kwargs)

    def get_joint_state_by_name(self, joint_name):
        return self.get_joint_state(self.get_joint_index_by_name(joint_name))

    def get_joint_states(self, joint_indices):
        """
        Get the states of all controllable joints and return JointState, which is a structure of arrays (SoA).
        """
        return p.getJointStates(self.id, joint_indices, **self._client_kwargs)

    def get_link_state(self, link_index, **kwargs):
        """
        Get the state of a specific link and return LinkState, which is a structure.
        """
        return p.getLinkState(self.id, link_index, **self._client_kwargs, **kwargs)

    def get_link_state_by_name(self, link_name, **kwargs):
        return self.get_link_state(self.get_joint_index_by_name(link_name), **kwargs)

    def get_link_states(self, joint_indices, **kwargs):
        """
        Get the states of all movable links and return LinkState, which is a structure of arrays (SoA).
        """
        return p.getLinkStates(self.id, joint_indices, **self._client_kwargs, **kwargs)

    def get_dynamics_info(self, link_index):
        """
        Get dynamics information and return as DynamicsInfo, which is a structure.
        """
        return p.getDynamicsInfo(self.id, link_index, **self._client_kwargs)

    def get_dynamics_infos(self, link_indices):
        """
        Get dynamics informations and return as DynamicsInfo, which is a structure.
        """
        return p.getDynamicsInfos(self.id, link_indices, **self._client_kwargs)

    def set_base_pose(self, position, orientation=(0, 0, 0, 1)):
        """
        Set the position and orientation of robot base (link)
        """
        p.resetBasePositionAndOrientation(
            self.id, position, orientation, **self._client_kwargs
        )

    def get_base_pose(self):
        """
        Get the position and orientation of robot base (link)
        """
        return p.getBasePositionAndOrientation(self.id, **self._client_kwargs)

    def get_base_velocity(self):
        """
        Get the linear and angular velocity of the base of a body
        """
        return p.getBaseVelocity(self.id, **self._client_kwargs)

    def set_base_velocity(self, linear_velocity, angular_velocity):
        """
        Set the linear and angular velocity of the base of a body
        """
        p.resetBaseVelocity(
            self.id, linear_velocity, angular_velocity, **self._client_kwargs
        )

    def reset(self):
        self.set_base_pose(self.init_base_position, self.init_base_orientation)
