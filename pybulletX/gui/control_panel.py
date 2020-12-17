# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import collections

import numpy as np
import pybullet as p

from ..robot_interface import IRobot
from ..utils.loop_thread import LoopThread
from ..helper import flatten_nested_dict, to_nested_dict

# TODO(poweic): pybullet is good at physics simulation, but sucks at GUI.
# We should use pybullet for simulation only and use URDFLoader & THREE.js
# for visualization (GUI).

log = logging.getLogger(__name__)


class Slider:
    def __init__(self, name, low, high, init_value):
        self.name = name
        self.low = low
        self.high = high
        log.info(f"name: {name}, low: {low}, high: {high}, init_value: {init_value}")
        self.handle_id = p.addUserDebugParameter(name, low, high, init_value)

    @property
    def value(self):
        return p.readUserDebugParameter(self.handle_id)


class Sliders:
    def __init__(self, names, lows, highs, init_values):
        self.names = names

        if not isinstance(lows, collections.abc.Iterable):
            lows = [lows for _ in names]
        if not isinstance(highs, collections.abc.Iterable):
            highs = [highs for _ in names]

        self.lows = lows
        self.highs = highs
        self.sliders = [Slider(*args) for args in zip(names, lows, highs, init_values)]

    @property
    def value(self):
        return np.array([s.value for s in self.sliders])


class PoseSlider:
    def __init__(
        self,
        name,
        position,
        orientation,
        position_low=[-0.1, -0.1, -0.1],
        position_high=[0.1, 0.1, 0.1],
    ):
        self.name = name

        euler_xyz = p.getEulerFromQuaternion(orientation)

        self.pos_sliders = Sliders(
            [f"{name}_{axis}" for axis in "xyz"], position_low, position_high, position
        )

        self.ori_sliders = Sliders(
            [f"{name}_euler_{axis}" for axis in "xyz"], -np.pi, np.pi, euler_xyz
        )

    @property
    def value(self):
        pos = self.pos_sliders.value
        ori = self.ori_sliders.value
        ori_q = p.getQuaternionFromEuler(ori)
        return pos, ori_q


class RobotControlWidget:
    def __init__(self, robot):
        self.robot = robot

        self.sliders = collections.defaultdict(list)

        # get states and action_space
        states = self.robot.get_states()
        action_space = self.robot.action_space

        # turn states and action_space to flattend dictionary
        states = flatten_nested_dict(states)
        action_space = flatten_nested_dict(action_space)

        for key, space in action_space.items():
            if key not in states:
                continue
            state = states[key]
            if isinstance(state, collections.abc.Iterable):
                names = [f"{key}[{i}]" for i in range(len(state))]
                self.sliders[key] = Sliders(names, space.low, space.high, state)
            else:
                self.sliders[key] = Slider(key, space.low[0], space.high[0], state)

    @property
    def value(self):
        actions = {k: s.value for k, s in self.sliders.items()}
        actions = to_nested_dict(actions)
        return actions


class ControlPanel:
    def __init__(self, interval=0.05):
        self._loop_thread = LoopThread(interval, self.update)

    def start(self):
        self._loop_thread.start()


class PoseControlPanel(ControlPanel):
    def __init__(self, robot, max_force=10, slider_params={}):
        super().__init__()
        self.robot = robot
        self.max_force = max_force

        pos, ori = self.robot.get_base_pose()
        self.pose_slider = PoseSlider(f"base_{id(robot)}", pos, ori, **slider_params)

        self.cid = p.createConstraint(
            self.robot.id,
            -1,
            -1,
            -1,
            p.JOINT_FIXED,
            [0, 0, 0],
            [0, 0, 0],
            childFramePosition=pos,
            childFrameOrientation=ori,
        )

    def update(self):
        pos, ori = self.pose_slider.value
        p.changeConstraint(self.cid, pos, ori, maxForce=self.max_force)


class RobotControlPanel(ControlPanel):
    def __init__(self, robot):
        super().__init__()
        assert isinstance(robot, IRobot)
        self.robot = robot
        self._widget = RobotControlWidget(self.robot)

    def update(self):
        self.robot.set_actions(self._widget.value)
