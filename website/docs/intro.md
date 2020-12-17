---
id: intro
title: Introduction
sidebar_label: Introduction
slug: /
---
Building robot simulation in PyBullet is like writing C code - not OOP and could
get messy very quickly.
PyBulletX is a **Pythonic** lightweight PyBullet wrapper that helps researchers to do more with less code. No more boilerplate.

```python
import pybulletX as px
px.init()

robot = px.Robot("kuka_iiwa/model.urdf")
```
