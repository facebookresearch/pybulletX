---
id: putting_it_all_together
title: Putting It All Together
---

Here are the examples of P controller with and without PyBulletX.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs
  defaultValue="px"
  values={[
    { label: 'With PyBulletX', value: 'px', },
    { label: 'Without PyBulletX', value: 'p', },
  ]
}>
<TabItem value="p">

```python
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
```

</TabItem>

<TabItem value="px">

```python
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
```

</TabItem>
</Tabs>
