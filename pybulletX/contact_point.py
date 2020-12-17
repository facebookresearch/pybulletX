# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import functools
import typing
import textwrap
from dataclasses import dataclass

from .mapping_mixin import MappingMixin


@dataclass
class ContactPoint(MappingMixin):
    r"""
    A struct wrapper around contact points returned by p.getContactPoints that
    provides dot access (ex: .normal_force) to all the attributes.

    Examples
    --------
    >>> import pybullet as p
    >>> contact_points = p.getContactPoints(0)
    >>> print (contact_points[0])
    (0, 1, 3, -1, 19,
      (1.09734,  0.13729,  0.31835),
      (1.09729,  0.13730,  0.31837),
      (0.91382, -0.13049, -0.38456),
      4.56199e-05,
      8.20047,
      0.03797,
      (0.14136,  0.98995, 0.0),
      2.04976,
      (0.38070, -0.05436, 0.923098)
    )

    >>> contact_point = ContactPoint(contact_points[0])
    >>> print (contact_point)
    contact_flag           : 0
    body_unique_id_a       : 1
    body_unique_id_b       : 3
    link_index_a           : -1
    link_index_b           : 19
    position_on_a          : (1.09734, 0.13729, 0.31835)
    position_on_b          : (1.09729, 0.1373, 0.31837)
    contact_normal_on_b    : (0.91382, -0.13049, -0.38456)
    contact_distance       : 4.56199e-05
    normal_force           : 8.20047
    lateral_friction_1     : 0.03797
    lateral_friction_dir_1 : (0.14136, 0.98995, 0.0)
    lateral_friction_2     : 2.04976
    lateral_friction_dir_2 : (0.3807, -0.05436, 0.923098)

    """
    contact_flag: int
    body_unique_id_a: int
    body_unique_id_b: int
    link_index_a: int
    link_index_b: int
    position_on_a: typing.Tuple[float]
    position_on_b: typing.Tuple[float]
    contact_normal_on_b: typing.Tuple[float]
    contact_distance: float
    normal_force: float
    lateral_friction_1: float
    lateral_friction_dir_1: typing.Tuple[float]
    lateral_friction_2: float
    lateral_friction_dir_2: typing.Tuple[float]

    # used to determine whether this is plural (for API consistency)
    _plural: bool = False

    def __repr__(self):
        return textwrap.dedent(
            f"""\
            contact_flag           : {self.contact_flag}
            body_unique_id_a       : {self.body_unique_id_a}
            body_unique_id_b       : {self.body_unique_id_b}
            link_index_a           : {self.link_index_a}
            link_index_b           : {self.link_index_b}
            position_on_a          : {self.position_on_a}
            position_on_b          : {self.position_on_b}
            contact_normal_on_b    : {self.contact_normal_on_b}
            contact_distance       : {self.contact_distance}
            normal_force           : {self.normal_force}
            lateral_friction_1     : {self.lateral_friction_1}
            lateral_friction_dir_1 : {self.lateral_friction_dir_1}
            lateral_friction_2     : {self.lateral_friction_2}
            lateral_friction_dir_2 : {self.lateral_friction_dir_2}
        """
        )


def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        contact_points = func(*args, **kwargs)
        return [ContactPoint(*_) for _ in contact_points]

    return wrapper
