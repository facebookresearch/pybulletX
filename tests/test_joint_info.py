# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybulletX  # noqa: F401


def test_get_joint_info(helpers, kuka_arm):
    # get the joint state of joint index 0
    joint_info = p.getJointInfo(bodyUniqueId=kuka_arm, jointIndex=0)

    helpers.check_getitem_method(joint_info)


def test_get_joint_infos(helpers, kuka_arm):
    num_dof = 7
    joint_infos = p.getJointInfos(bodyUniqueId=kuka_arm, jointIndices=range(num_dof))

    assert len(joint_infos) == num_dof

    for i, joint_info in enumerate(joint_infos):
        assert joint_infos[i] == joint_info
        helpers.check_getitem_method(joint_info)
