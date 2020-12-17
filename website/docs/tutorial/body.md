---
id: pybulletx_body
title: Creating a Body
---

Every model or object you load in PyBullet has a unique id (starting from 0).
For most of the PyBullet functions, you need to pass this id as the first argument for querying information.
Instead of using the unique id directly with `p.SOME_FUNCTION(id, ...)` every time, pybulletX provides
a helper class `pybulletX.Body`.

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
import pybullet as p
import pybullet_data

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
kuka_id = p.loadURDF("kuka_iiwa/model.urdf")

print (kuka_id, type(kuka_id)) # 0, int
print (p.getBasePositionAndOrientation(kuka_id)) # ((0., 0., 0.), (0., 0., 0., 1.))
print (p.getNumJoints(kuka_id)) # 7 joints
```

</TabItem>
<TabItem value="px">

```python
import pybulletX as px

px.init()
body = px.Body("kuka_iiwa/model.urdf")

print (body.id) # 0 <= unique id returned by p.loadURDF
print (body.get_base_pose()) # p.getBasePositionAndOrientation(self.id)
print (body.num_joints()) # p.getNumJoints(self.id)
```

</TabItem>
</Tabs>

Here's the list of helper functions:
* `Body.num_joints`
* `Body.get_joint_index_by_name(joint_name)`
* `Body.get_joint_indices_by_names(joint_names)`
* `Body.get_joint_info(joint_index)`
* `Body.get_joint_info_by_name(joint_name)`
* `Body.get_joint_infos(joint_indices)`
* `Body.get_joint_state(joint_index)`
* `Body.get_joint_state_by_name(joint_name)`
* `Body.get_joint_states(joint_indices)`
* `Body.get_link_state(joint_index)`
* `Body.get_link_state_by_name(joint_name)`
* `Body.get_link_states(joint_indices)`
* `Body.get_base_pose()`
* `Body.set_base_pose(position, orientation)`
* `Body.get_base_velocity()`
* `Body.set_base_velocity(linear_velocity, angular_velocity)`
