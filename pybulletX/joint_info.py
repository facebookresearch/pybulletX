# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import typing
import textwrap
from dataclasses import dataclass

from .mapping_mixin import MappingMixin
from .joint_type import GetJointTypeName


@dataclass
class JointInfo(MappingMixin):
    """
    A struct wrapper around joint info returned by pybullet.getJointInfo that provides
    dot access (ex: .joint_upper_limit) to all the attributes.
    """

    joint_index: int
    joint_name: bytes
    joint_type: int
    q_index: int
    u_index: int
    flags: int
    joint_dampling: float
    joint_friction: float
    joint_lower_limit: float
    joint_upper_limit: float
    joint_max_force: float
    joint_max_velocity: float
    link_name: bytes
    joint_axis: typing.Tuple[float]
    parent_frame_pos: typing.Tuple[float]
    parent_frame_orn: typing.Tuple[float]
    parent_index: int

    # used to determine whether this is a joint_state or joint states
    _plural: bool = False

    def __repr__(self):
        return textwrap.dedent(
            f"""\
            joint_index            : {self.joint_index}
            joint_name             : {self.joint_name}
            joint_type             : {GetJointTypeName(self.joint_type)} (= {self.joint_type})
            q_index                : {self.q_index}
            u_index                : {self.u_index}
            flags                  : {self.flags}
            joint_dampling         : {self.joint_dampling}
            joint_friction         : {self.joint_friction}
            joint_lower_limit      : {self.joint_lower_limit}
            joint_upper_limit      : {self.joint_upper_limit}
            joint_max_force        : {self.joint_max_force}
            joint_max_velocity     : {self.joint_max_velocity}
            link_name              : {self.link_name}
            joint_axis             : {self.joint_axis}
            parent_frame_pos       : {self.parent_frame_pos}
            parent_frame_orn       : {self.parent_frame_orn}
            parent_index           : {self.parent_index}
        """
        )
