# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import collections

_JOINT_TYPES = {
    p.JOINT_FIXED: "JOINT_FIXED",
    p.JOINT_GEAR: "JOINT_GEAR",
    p.JOINT_PLANAR: "JOINT_PLANAR",
    p.JOINT_POINT2POINT: "JOINT_POINT2POINT",
    p.JOINT_PRISMATIC: "JOINT_PRISMATIC",
    p.JOINT_REVOLUTE: "JOINT_REVOLUTE",
    p.JOINT_SPHERICAL: "JOINT_SPHERICAL",
}


def GetJointTypeName(joint_type_ids):
    if isinstance(joint_type_ids, collections.abc.Iterable):
        return [_JOINT_TYPES[_] for _ in joint_type_ids]
    else:
        return _JOINT_TYPES[joint_type_ids]
