# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import numpy as np

import pybullet as p
import pybulletX as px  # noqa: F401


def test_pybullet_body(helpers):
    with px.Client(mode=p.DIRECT):
        init_position = (0, 0, 1)
        init_orientation = (0, 0, 0, 1)
        body = px.Body("kuka_iiwa/model.urdf", init_position, init_orientation)

        assert body.num_joints == 7

        # Move the robot to a target position/orientation
        position, orientation = (0, 1, 4), (0.03427, 0.10602, 0.14357, 0.98334)

        body.set_base_pose(position, orientation)
        position_, orientation_ = body.get_base_pose()
        assert np.allclose(position_, position)
        assert np.allclose(orientation_, orientation)

        # Reset the robot back to init position/orientation
        body.reset()
        position_, orientation_ = body.get_base_pose()
        assert np.allclose(position_, init_position)
        assert np.allclose(orientation_, init_orientation)

        print(body)
