# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybullet_data
import pybulletX as px  # noqa: F401


def test_add_additional_search_path():
    p.connect(p.DIRECT)

    # since pybullet.getDataPath() is already in px.path, this should work
    # just fine
    px.helper.loadURDF("plane.urdf")

    # After adding an additional search path, this will success
    px.path.append(pybullet_data.getDataPath())
    px.helper.loadURDF("plane.urdf")
