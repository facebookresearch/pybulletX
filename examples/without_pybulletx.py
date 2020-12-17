# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import time

import numpy as np
import pybullet as p
import pybullet_data

P_GAIN = 50
desired_joint_positions = np.array([1.218, 0.507, -0.187, 1.235, 0.999, 1.279, 0])


def main():
    p.connect(p.GUI)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf")

    robot_id = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)

    num_dofs = 7
    joint_indices = range(num_dofs)

    # The magic that enables torque control
    p.setJointMotorControlArray(
        bodyIndex=robot_id,
        jointIndices=joint_indices,
        controlMode=p.VELOCITY_CONTROL,
        forces=np.zeros(num_dofs),
    )

    while True:
        time.sleep(0.01)

        joint_states = p.getJointStates(robot_id, joint_indices)
        joint_positions = np.array([j[0] for j in joint_states])
        error = desired_joint_positions - joint_positions
        torque = error * P_GAIN

        p.setJointMotorControlArray(
            bodyIndex=robot_id,
            jointIndices=joint_indices,
            controlMode=p.TORQUE_CONTROL,
            forces=torque,
        )

        p.stepSimulation()


if __name__ == "__main__":
    main()
