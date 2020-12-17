# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import numpy as np

import pybulletX as px

P_GAIN = 50
desired_joint_positions = np.array([1.218, 0.507, -0.187, 1.235, 0.999, 1.279, 0])


def main():
    px.init()

    robot = px.Robot("kuka_iiwa/model.urdf", use_fixed_base=True)
    robot.torque_control = True

    t = px.utils.SimulationThread(real_time_factor=1.0)
    t.start()

    while True:
        error = desired_joint_positions - robot.get_states().joint_position
        actions = robot.action_space.new()
        actions.joint_torque = error * P_GAIN
        robot.set_actions(actions)


if __name__ == "__main__":
    main()
