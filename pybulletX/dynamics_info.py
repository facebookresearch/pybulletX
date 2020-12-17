# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import typing
import textwrap
import collections
from dataclasses import dataclass

from .mapping_mixin import MappingMixin

_BODY_TYPES = {
    1: "rigid body",
    2: "multi body",
    3: "soft body",
}


def GetBodyType(body_type_ids):
    if isinstance(body_type_ids, collections.abc.Iterable):
        return [_BODY_TYPES[_] for _ in body_type_ids]
    else:
        return _BODY_TYPES[body_type_ids]


@dataclass
class DynamicsInfo(MappingMixin):
    """
    A struct wrapper around dynamics info returned by pybullet.getJointInfo that
    provides dot access (ex: .lateral_friction) to all the attributes.
    """

    mass: float
    lateral_friction: float
    local_inertia_diagonal: typing.Tuple[float]
    local_inertial_pos: typing.Tuple[float]
    local_inertial_orn: typing.Tuple[float]
    restitution: float
    rolling_friction: float
    spinning_friction: float
    contact_damping: float
    contact_stiffness: float
    body_type: int
    collision_margin: float

    _plural: bool = False

    def __repr__(self):
        return textwrap.dedent(
            f"""\
            mass                  : {self.mass}
            lateral_friction      : {self.lateral_friction}
            local_inertia_diagonal: {self.local_inertia_diagonal}
            local_inertial_pos    : {self.local_inertial_pos}
            local_inertial_orn    : {self.local_inertial_orn}
            restitution           : {self.restitution}
            rolling_friction      : {self.rolling_friction}
            spinning_friction     : {self.spinning_friction}
            contact_damping       : {self.contact_damping}
            contact_stiffness     : {self.contact_stiffness}
            body_type             : {GetBodyType(self.body_type)} (= {self.body_type})
            collision_margin      : {self.collision_margin}
        """
        )
