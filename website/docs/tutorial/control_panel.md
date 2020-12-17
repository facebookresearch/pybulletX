---
id: control_panel
title: Control Panels
---

Sometimes you want to use a control panel to play around with the robot (e.g. moving the base around or changing joint positions).

There are two control panels provided in `px.gui`:
* PoseControlPanel - creates a panel that can control the base position of a `px.Body` with sliders.
* RobotControlPanel - creates a panel that can control the all free joint positions of a `px.Robot` with sliders.

This saves you the trouble of creating slider for each joint by using `p.addUserDebugParameter` and ...

The examples in this tutorial are available [here](https://github.com/facebookresearch/pybulletX/blob/master/examples/control_panel.py).

```python
import pybulletX as px

px.init()
robot = px.Robot("kuka_iiwa/model.urdf")

# Run the simulation in another thread
t = px.utils.SimulationThread(1.0)
t.start()

# ControlPanel also takes pybulletX.Body
panel = px.gui.RobotControlPanel(robot)
panel.start()
```
