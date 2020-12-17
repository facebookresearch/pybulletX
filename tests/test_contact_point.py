# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybulletX as px  # noqa: F401


def test_contact_points(helpers):
    with px.Client(mode=p.DIRECT) as c:
        body = px.Body("teddy_vhacd.urdf")
        body.set_base_pose([0.0, 0.0, -0.02])
        c.stepSimulation()

        contact_points = c.getContactPoints(body.id)

        """
        check_getitem_method will check the following:
        assert contact_point[0] == contact_point.contact_flag
        assert contact_point[1] == contact_point.body_unique_id_a
        assert contact_point[2] == contact_point.body_unique_id_b
        assert contact_point[3] == contact_point.link_index_a
        assert contact_point[4] == contact_point.link_index_b
        assert contact_point[5] == contact_point.position_on_a
        assert contact_point[6] == contact_point.position_on_b
        assert contact_point[7] == contact_point.contact_normal_on_b
        assert contact_point[8] == contact_point.contact_distance
        assert contact_point[9] == contact_point.normal_force
        assert contact_point[10] == contact_point.lateral_friction_1
        assert contact_point[11] == contact_point.lateral_friction_dir_1
        assert contact_point[12] == contact_point.lateral_friction_2
        assert contact_point[13] == contact_point.lateral_friction_dir_2
        """
        for contact_point in contact_points:
            helpers.check_getitem_method(contact_point)
