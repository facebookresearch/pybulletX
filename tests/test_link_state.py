# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import pybullet as p
import pybulletX  # noqa: F401


def test_get_link_state(helpers, kuka_arm):
    # get the joint state of joint index 0
    link_state = p.getLinkState(bodyUniqueId=kuka_arm, linkIndex=0)

    helpers.check_getitem_method(link_state)


def test_get_link_states(helpers, kuka_arm):
    num_links = 7
    link_states = p.getLinkStates(bodyUniqueId=kuka_arm, linkIndices=range(num_links))

    assert len(link_states) == num_links

    for i, link_state in enumerate(link_states):
        assert link_states[i] == link_state
        helpers.check_getitem_method(link_state)
