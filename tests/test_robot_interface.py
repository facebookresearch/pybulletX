# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import numpy as np

# See https://github.com/openai/gym/blob/master/gym/spaces/box.py for more detail
from gym import spaces

from pybulletX.utils.space_dict import SpaceDict
from pybulletX.robot_interface import IRobot, router
from pybulletX.helper import pprint


class Digit(IRobot):
    @property
    @router
    def state_space(self):
        return SpaceDict(
            {"image": spaces.Box(low=0, high=255, shape=(3, 4), dtype=np.uint8)}
        )

    @router
    def get_states(self):
        return {"image": np.zeros([2, 3], dtype=np.uint8)}


class AllegroHand(IRobot):
    num_dof = 16

    @property
    @router
    def action_space(self):
        return SpaceDict(
            {
                "joint_torque": spaces.Box(
                    low=0, high=1, shape=(AllegroHand.num_dof,), dtype=np.float32
                )
            }
        )

    @property
    @router
    def state_space(self):
        return SpaceDict(
            {
                "joint_position": spaces.Box(
                    low=0, high=1, shape=(AllegroHand.num_dof,), dtype=np.float32
                )
            }
        )

    @router
    def get_states(self):
        return {"joint_position": np.zeros([AllegroHand.num_dof])}

    @router
    def set_actions(self, actions):
        for k, v in actions.items():
            print(f"\33[33mIn AllegroHand's set_actions\33[0m: {k} -> {v}")


class Gripper(IRobot):
    @property
    @router
    def action_space(self):
        return SpaceDict(
            {"force": spaces.Box(low=0, high=1, shape=(), dtype=np.float32)}
        )

    @property
    @router
    def state_space(self):
        return SpaceDict(
            {"position": spaces.Box(low=0, high=1, shape=(), dtype=np.float32)}
        )

    @router
    def get_states(self):
        return {"position": np.zeros([7])}

    @router
    def set_actions(self, actions):
        for k, v in actions.items():
            print(f"\33[33mIn Gripper's set_actions\33[0m: {k} -> {v}")


class Sawyer(IRobot):
    @property
    @router
    def action_space(self):
        return SpaceDict(
            {"joint_torque": spaces.Box(low=0, high=1, shape=(7,), dtype=np.float32)}
        )

    @property
    @router
    def state_space(self):
        return SpaceDict(
            {"joint_position": spaces.Box(low=0, high=1, shape=(7,), dtype=np.float32)}
        )

    @router
    def get_states(self):
        return {"joint_position": np.zeros([7])}

    @router
    def set_actions(self, actions):
        for k, v in actions.items():
            print(f"\33[33mIn Sawyer's set_actions\33[0m: {k} -> {v}")


# This is just a demonstration
Kuka = Sawyer


def my_simple_policy(states, action_space):
    # new actions from the action space
    actions = action_space.new()
    actions.left_arm.joint_torque = np.zeros(7)
    actions.right_arm.hand.joint_torque = np.zeros(16)
    return actions


class MyRobot(IRobot):
    @router
    def set_actions(self, actions):
        print(f"\33[33mIn MyRobot's set_actions\33[0m: {actions}")


def test_all():
    # Create a robot
    robot = MyRobot()

    # Create a Sawyer, a Gripper, 2 Digits. Put them together as left arm
    robot.left_arm = Sawyer()
    robot.left_arm.gripper = Gripper()
    robot.left_arm.gripper.digits1 = Digit()
    robot.left_arm.gripper.digits2 = Digit()

    # Create a Kuka arm, AllegroHand, and 5 Digits. Put them together as right arm
    robot.right_arm = Kuka()
    robot.right_arm.hand = AllegroHand()

    # TODO(poweic): create class ModuleList like torch.nn.ModuleList
    robot.right_arm.hand.digits1 = Digit()
    robot.right_arm.hand.digits2 = Digit()
    robot.right_arm.hand.digits3 = Digit()
    robot.right_arm.hand.digits4 = Digit()

    # Print the robot by summarizing all states/actions space and get the current states
    print(robot)

    # Print the action_space and state_space
    print(robot.right_arm.action_space)
    print(robot.action_space)
    print(robot.state_space)

    # get the states of my robot
    states = robot.get_states()

    # states can be accessed like attributes
    print(states.left_arm.joint_position.shape)
    print(states.left_arm.gripper.position.shape)
    print(states.left_arm.gripper.digits1.image.shape)
    print(states.left_arm.gripper.digits2.image.shape)

    print(states.right_arm.joint_position.shape)
    print(states.right_arm.hand.joint_position.shape)
    print(states.right_arm.hand.digits1.image.shape)
    print(states.right_arm.hand.digits2.image.shape)

    # states -> actions
    actions = my_simple_policy(states, robot.action_space)
    pprint(actions)

    robot.set_actions(actions)
