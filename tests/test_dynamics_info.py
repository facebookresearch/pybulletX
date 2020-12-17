# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybulletX  # noqa: F401


def test_get_dynamics_info(helpers, kuka_arm):
    # get the dynamics info of link index 0
    dynamics_info = p.getDynamicsInfo(bodyUniqueId=kuka_arm, linkIndex=0)

    helpers.check_getitem_method(dynamics_info)


def test_get_joint_infos(helpers, kuka_arm):
    num_dof = 7
    dynamics_infos = p.getDynamicsInfos(
        bodyUniqueId=kuka_arm, linkIndices=range(num_dof)
    )

    assert len(dynamics_infos) == num_dof

    for i, dynamics_info in enumerate(dynamics_infos):
        assert dynamics_infos[i] == dynamics_info
        helpers.check_getitem_method(dynamics_info)
