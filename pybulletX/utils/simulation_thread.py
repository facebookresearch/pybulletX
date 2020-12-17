# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import threading

import pybullet as p

from .soft_real_time_clock import SoftRealTimeClock


class SimulationThread(threading.Thread):
    def __init__(self, real_time_factor):
        super().__init__()
        self.real_time_factor = real_time_factor

    def run(self):
        """
        Use a soft real-time clock (Soft RTC) to step through the simulation.If
        the p.stepSimulation takes too long, slow down the clock by decreasing
        the real time factor.
        """
        time_step = p.getPhysicsEngineParameters()["fixedTimeStep"]
        clock = SoftRealTimeClock(period=time_step / self.real_time_factor)
        while threading.main_thread().is_alive():
            p.stepSimulation()
            clock.sleep()
