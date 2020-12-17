# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pytest
import pybullet as p
import pybulletX as px


@pytest.mark.parametrize("joint_position", [True, False])
@pytest.mark.parametrize("joint_velocity", [True, False])
@pytest.mark.parametrize("joint_reaction_forces", [True, False])
@pytest.mark.parametrize("applied_joint_motor_torque", [True, False])
def test_robot_state_space_configuration(
    joint_position, joint_velocity, joint_reaction_forces, applied_joint_motor_torque
):
    with px.Client(mode=p.DIRECT):
        robot = px.Robot("kuka_iiwa/model.urdf")

        robot.configure_state_space(
            joint_position,
            joint_velocity,
            joint_reaction_forces,
            applied_joint_motor_torque,
        )

        for S in [robot.state_space, robot.get_states()]:
            assert joint_position == hasattr(S, "joint_position")
            assert joint_velocity == hasattr(S, "joint_velocity")
            assert joint_reaction_forces == hasattr(S, "joint_reaction_forces")
            assert applied_joint_motor_torque == hasattr(
                S, "applied_joint_motor_torque"
            )
