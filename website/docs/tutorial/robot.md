---
id: pybulletx_robot
title: Creating a Robot
---

Class `pybulletX.Robot` inherits from a `pybulletX.Body` and provides even more functionalities.  
Here's an example:
```python
import pybulletX as px

px.init()
robot = px.Robot("kuka_iiwa/model.urdf")

# helpers inherits from px.Body
print (robot.id)
print (robot.get_base_pose())
print (robot.num_joints())

# helpers overwritten by px.Robot
print (robot.get_joint_infos())  # joint info of all free joints
print (robot.get_joint_states()) # joint state of all free joints
print (robot.get_link_states())  # link state of all free joints

# new helpers exclusive to px.Robot
print (robot.num_dofs) # returns number of Degree of Freedom
print (robot.free_joint_indices)

# Get the joint_position (np.array) of all free joints
joint_position = robot.get_joint_states().joint_position

# Move to new joint position
joint_position += 0.01
robot.set_joint_position(joint_position)
```

You can also use enable/disable torque control by setting `.torque_control` to `True`/`False`:
```python
robot.torque_control = True
joint_torque = np.zeros(7)

# the arm will now fall to the ground
robot.set_joint_torque(joint_torque)
```
