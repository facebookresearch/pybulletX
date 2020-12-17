---
id: joint_info
title: Getting the Joint Information
---

In pybullet, you can query the information for each joint using `p.getJointInfo()`.
However, it only returns a list of information in plain old data type (see below).
Going through [PyBullet's Getting Started guide on Google Doc](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdAvK3dsihxVUA/edit#heading=h.2ye70wns7io3)
and trying to figure out which one is which is not fun at all.
```python
>>> body_id = p.loadURDF("kuka_iiwa/model.urdf")
>>> joint_info = p.getJointInfo(body_id, 0)
>>> print (joint_info)
(0,
 b'lbr_iiwa_joint_1',
 0,
 7,
 6,
 1,
 0.5,
 0.0,
 -2.96705972839, # <== what's this?
 2.96705972839,
 300.0,
 10.0,
 b'lbr_iiwa_link_1',
 (0.0, 0.0, 1.0),
 (0.1, 0.0, 0.0875),
 (0.0, 0.0, 0.0, 1.0),
 -1)
```

In `pybulletX`, we provides a dataclass `JointInfo` for storing the joint information.
Once `pybulletX` is imported, all the subsequent `p.getJointInfo()` will return a `JointInfo` instance.
```python
>>> import pybullet as p
>>> import pybulletX as px
>>> px.init()
>>> body_id = p.loadURDF("kuka_iiwa/model.urdf")
>>> joint_info = p.getJointInfo(body_id, 0)
>>> print (joint_info)
joint_index            : 0
joint_name             : b'lbr_iiwa_joint_1'
joint_type             : JOINT_REVOLUTE (= 0)
q_index                : 7
u_index                : 6
flags                  : 1
joint_dampling         : 0.5
joint_friction         : 0.0
joint_lower_limit      : -2.96705972839
joint_upper_limit      : 2.96705972839
joint_max_force        : 300.0
joint_max_velocity     : 10.0
link_name              : b'lbr_iiwa_link_1'
joint_axis             : (0.0, 0.0, 1.0)
parent_frame_pos       : (0.1, 0.0, 0.0875)
parent_frame_orn       : (0.0, 0.0, 0.0, 1.0)
parent_index           : -1
```

With `JointInfo` dataclass, you can use dot `(.)` to access all the attributes (ex: `.joint_dampling`).  
For example:
```python
>>> print (joint_info.joint_dampling)
0.5
>>> print (joint_info.joint_lower_limit)
-2.96705972839
```

Here is what class `JointInfo` looks like:
```python title="joint_info.py"
@dataclass
class JointInfo(MappingMixin):
    """
    A struct wrapper around joint info returned by pybullet.getJointInfo that
    provides dot access (ex: .joint_upper_limit) to all the attributes.
    """

    joint_index: int
    joint_name: bytes
    joint_type: int
    q_index: int
    u_index: int
    flags: int
    joint_dampling: float
    joint_friction: float
    joint_lower_limit: float
    joint_upper_limit: float
    joint_max_force: float
    joint_max_velocity: float
    link_name: bytes
    joint_axis: typing.Tuple[float]
    parent_frame_pos: typing.Tuple[float]
    parent_frame_orn: typing.Tuple[float]
    parent_index: int

    # ...
```
