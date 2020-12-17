# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import typing

# import textwrap
from dataclasses import dataclass

from .mapping_mixin import MappingMixin


@dataclass
class LinkState(MappingMixin):
    """
    A struct wrapper around link state returned by pybullet.getLinkState that provides
    dot access (ex: .link_world_position) to all the attributes.
    """

    link_world_position: typing.List[float]
    link_world_orientation: typing.List[float]

    local_inertial_frame_position: typing.List[float]
    local_inertial_frame_orientation: typing.List[float]

    world_link_frame_position: typing.List[float]
    world_link_frame_orientation: typing.List[float]

    world_link_linear_velocity: typing.List[float] = None
    world_link_angular_velocity: typing.List[float] = None

    # used to determine whether this is a joint_state or joint states
    _plural: bool = False

    def __repr__(self):
        attr_max_length = max(map(len, self.__dict__.keys()))
        fstr = "{{:{0}s}} : {{}}".format(attr_max_length)
        s = "\n".join([fstr.format(k, v) for k, v in self.__dict__.items()])
        return s

        # return textwrap.dedent(
        #     f"""\
        #     link_world_position              : {self.link_world_position}
        #     link_world_orientation           : {self.link_world_orientation}
        #     local_inertial_frame_position    : {self.local_inertial_frame_position}
        #     local_inertial_frame_orientation : {self.local_inertial_frame_orientation}
        #     world_link_frame_position        : {self.world_link_frame_position}
        #     world_link_frame_orientation     : {self.world_link_frame_orientation}
        #     world_link_linear_velocity       : {self.world_link_linear_velocity}
        #     world_link_angular_velocity      : {self.world_link_angular_velocity}
        # """
        # )
