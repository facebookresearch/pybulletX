# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybulletX as px


def test_free_joint_indices():
    free_joint_indices = [1, 2, 4, 5]
    with px.Client(mode=p.DIRECT):
        robot = px.Robot("kuka_iiwa/model.urdf")
        robot.free_joint_indices = free_joint_indices

        states = robot.get_states()
        assert robot.num_dofs == len(free_joint_indices)

        assert states.joint_position.shape == (robot.num_dofs,)
        assert states.joint_velocity.shape == (robot.num_dofs,)
        assert states.joint_reaction_forces.shape == (robot.num_dofs, 6)
        assert states.applied_joint_motor_torque.shape == (robot.num_dofs,)

        S = robot.state_space
        assert S.joint_position.shape == states.joint_position.shape
        assert S.joint_velocity.shape == states.joint_velocity.shape
        assert S.joint_reaction_forces.shape == states.joint_reaction_forces.shape
        assert (
            S.applied_joint_motor_torque.shape
            == states.applied_joint_motor_torque.shape
        )

        A = robot.action_space
        assert A.joint_position.shape == (robot.num_dofs,)
