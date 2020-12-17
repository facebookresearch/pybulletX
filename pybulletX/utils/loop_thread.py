# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import threading

from .soft_real_time_clock import SoftRealTimeClock


class LoopThread(threading.Thread):
    def __init__(self, interval, callback):
        super().__init__()
        self.interval = interval
        self._callback = callback

    def run(self):
        """
        Use a soft real-time clock (Soft RTC) to call callback periodically.
        """
        clock = SoftRealTimeClock(period=self.interval)
        while threading.main_thread().is_alive():
            self._callback()
            clock.sleep()
