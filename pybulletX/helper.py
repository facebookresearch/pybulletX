# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os
import sys
import warnings
import textwrap
import collections

import numpy as np
import pybullet as p
import pybullet_data

import pybulletX as px

DEFAULT_CONFIG = {
    "gravity": {"gravX": 0, "gravY": 0, "gravZ": -9.81},
}


def init_pybullet(cfg=DEFAULT_CONFIG, mode=p.GUI):
    warnings.warn("init_pybullet() is deprecated. Use init() instead.")
    return init(cfg, mode)


def init(cfg=DEFAULT_CONFIG, mode=p.GUI):
    """
    Initialize pybullet with p.GUI, call pybulletX's setParameters,
    and load the classic plane.
    """
    # Initialize pybullet
    client = p.connect(mode)

    # Use config to set pybullet simulation parameters
    p.setParameters(cfg, client)

    # Load the classic plane
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf", physicsClientId=client)

    return client


class Axes:
    def __init__(self, axes):
        self.axes = axes

    def remove(self):
        if not self.axes:
            return
        for axis in self.axes:
            p.removeUserDebugItem(axis)


def add_axes(
    object_id,
    link_id=None,
    size=0.1,
    lineWidth=3.0,
    position=(0, 0, 0),
    orientation=(0, 0, 0, 1),
):
    opts = dict(lineWidth=lineWidth, parentObjectUniqueId=object_id,)
    if link_id:
        opts["parentLinkIndex"] = link_id

    rotation_matrix = np.array(p.getMatrixFromQuaternion(orientation)).reshape(3, 3)
    position = np.array(position)
    x = rotation_matrix.dot([size, 0, 0])
    y = rotation_matrix.dot([0, size, 0])
    z = rotation_matrix.dot([0, 0, size])

    # add axis X (red), Y (green), and Z (blue)
    return Axes(
        [
            p.addUserDebugLine(position, position + x, [1, 0, 0], **opts),
            p.addUserDebugLine(position, position + y, [0, 1, 0], **opts),
            p.addUserDebugLine(position, position + z, [0, 0, 1], **opts),
        ]
    )


def flatten_nested_dict(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.Mapping):
            items.extend(flatten_nested_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def to_nested_dict(d, sep="."):
    root = {}
    for k, v in d.items():
        node = root
        keys = k.split(sep)
        for key in keys[:-1]:
            if key not in node:
                node[key] = {}
            node = node[key]
        node[keys[-1]] = v
    return root


def dump(obj, indent=2):
    def _dfs(obj):
        if not isinstance(obj, collections.abc.Mapping):
            return repr(obj)

        s = ",\n".join(['"{}": {}'.format(k, _dfs(v)) for k, v in obj.items()])

        if s == "":
            return "{}"

        return "{\n" + textwrap.indent(s, " " * indent) + "\n}"

    return _dfs(obj)


def pprint(obj, indent=2, stream=sys.stdout):
    stream.write(dump(obj, indent) + "\n")


def find_file(file_path):
    if os.path.isfile(file_path):
        return file_path

    # if file_path is relative path, then we will go through pybulletX.path,
    # see if file is in any directories.
    # if file_path is absolute path, nothing we can do :(
    if not os.path.isabs(file_path):
        for search_path in px.path:
            path = os.path.join(search_path, file_path)
            if os.path.isfile(path):
                return path

    raise FileNotFoundError(f"No such file: '{file_path}'")


def loadURDF(fileName, *args, **kwargs):
    fileName = find_file(fileName)
    return p.loadURDF(fileName, *args, **kwargs)
