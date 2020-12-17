---
id: simulation_thread
title: Simulation Thread
---

By default, the physics server in PyBullet will not step the simulation, unless you explicitly call `p.stepSimulation()`
(see [here](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA) for more information).

You can use `p.setRealTimeSimulation(1)` to let the physics server step the simulation automatically. However, it does **NOT** work in `DIRECT` mode.
Besides that, sometimes you might want to slow down (or speed up) the simulation by changing the real-time factor.

This can be done by `px.utils.SimulationThread`, which inherits from Python `threading.Thread`.
```python
import pybulletX as px

px.init()
robot = px.Robot("kuka_iiwa/model.urdf")

t = px.utils.SimulationThread(real_time_factor=1.0)
t.start()
```
