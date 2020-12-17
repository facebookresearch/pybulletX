# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybulletX  # noqa: F401


def test_get_joint_state(helpers, kuka_arm):
    # get the joint state of joint index 0
    joint_state = p.getJointState(bodyUniqueId=kuka_arm, jointIndex=0)

    """
    check_getitem_method will check the following:
    assert joint_state[0] == joint_state.joint_position
    assert joint_state[1] == joint_state.joint_velocity
    assert joint_state[2] == joint_state.joint_reaction_forces
    assert joint_state[3] == joint_state.applied_joint_motor_torque
    """
    helpers.check_getitem_method(joint_state)


def test_get_joint_states(helpers, kuka_arm):
    num_dof = 7
    joint_states = p.getJointStates(kuka_arm, jointIndices=range(num_dof))
    assert len(joint_states) == num_dof

    for i, joint_state in enumerate(joint_states):
        assert joint_states[i] == joint_state
        helpers.check_getitem_method(joint_state)
