# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import copy

import pytest

from gym import spaces
from pybulletX.utils.space_dict import SpaceDict


@pytest.fixture()
def car():
    return SpaceDict(
        {
            "sensors": SpaceDict(
                {
                    "position": spaces.Box(low=-100, high=100, shape=(3,)),
                    "velocity": spaces.Box(low=-1, high=1, shape=(3,)),
                    "front_cam": spaces.Tuple(
                        (
                            spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                            spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                        )
                    ),
                    "rear_cam": spaces.Box(low=0, high=1, shape=(10, 10, 3)),
                }
            ),
            "ext_controller": spaces.MultiDiscrete((5, 2, 2)),
            "inner_state": {
                "charge": spaces.Discrete(100),
                "system_checks": spaces.MultiBinary(10),
                "job_status": SpaceDict(
                    {
                        "task": spaces.Discrete(5),
                        "progress": spaces.Box(low=0, high=100, shape=()),
                    }
                ),
            },
        }
    )


def test_space_dict(car):
    print(car)
    print(car.sensors)
    print(car.sensors.position)
    print(car.sensors.velocity)
    print(car.sensors.front_cam)
    print(car.sensors.front_cam[0])
    print(car.sensors.front_cam[1])
    print(car.sensors.rear_cam)
    print(car.inner_state)
    print(car.inner_state.charge)
    print(car.inner_state.system_checks)
    print(car.inner_state.job_status)
    print(car.inner_state.job_status.task)
    print(car.inner_state.job_status.progress)


def test_deepcopy_space_dict(car):
    dc = copy.deepcopy(car)
    print(dc)
