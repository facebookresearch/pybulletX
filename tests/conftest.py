# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import dataclasses

import pybullet as p
import pybullet_data

import pytest


class Helpers:
    @staticmethod
    def get_fields(inst):
        fields = dataclasses.asdict(inst).keys()
        # TODO(poweic): create classes for JointStates, JointInfos, and LinkStates,
        # and remove _plural
        return [f for f in fields if f != "_plural"]

    @staticmethod
    def check_getitem_method(inst):
        # only check field up to the length of the tuple returned by pybullet
        fields = Helpers.get_fields(inst)[: len(inst)]

        for i, field in enumerate(fields):
            assert inst[i] == getattr(inst, field)


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture
def kuka_arm(helpers):
    p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # Load kuka_iiwa robotics arm for pybullet_data
    kukaId = p.loadURDF("kuka_iiwa/model.urdf", [0, 0, 0], useFixedBase=True)
    return kukaId
