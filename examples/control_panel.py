# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybulletX as px


def main():
    px.init()

    robot = px.Robot("kuka_iiwa/model.urdf")

    # Run the simulation in another thread
    t = px.utils.SimulationThread(1.0)
    t.start()

    # ControlPanel also takes pybulletX.Body
    panel = px.gui.RobotControlPanel(robot)
    panel.start()

    input("Press any key to continue...")


if __name__ == "__main__":
    main()
