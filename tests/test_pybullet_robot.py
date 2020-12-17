# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybulletX as px


def test_pybullet_body():
    with px.Client(mode=p.DIRECT):
        init_position = (0, 0, 1)
        init_orientation = (0, 0, 0, 1)
        robot = px.Robot("kuka_iiwa/model.urdf", init_position, init_orientation)

        print(robot.free_joint_indices)
