# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import typing
import textwrap
from dataclasses import dataclass

from .mapping_mixin import MappingMixin


@dataclass
class JointState(MappingMixin):
    """
    A struct wrapper around joint state returned by pybullet.getJointState that provides
    dot access (ex: .joint_position) to all the attributes.
    """

    joint_position: float
    joint_velocity: float
    joint_reaction_forces: typing.List[float]
    applied_joint_motor_torque: float

    # used to determine whether this is a joint_state or joint states
    _plural: bool = False

    def __repr__(self):
        return textwrap.dedent(
            f"""\
           joint_position             : {self.joint_position}
           joint_velocity             : {self.joint_velocity}
           joint_reaction_forces      : {self.joint_reaction_forces}
           applied_joint_motor_torque : {self.applied_joint_motor_torque}
        """
        )
