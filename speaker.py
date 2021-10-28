from machine import Pin, Timer
import time

from util import singleton


@singleton
class Speaker:
    def __init__(self, scheduler):
        self.buzz = Pin(14, Pin.OUT)
        self.buzz.value(0)
        self.buzz_start = 0
        self.duration = 0
        scheduler.schedule("beeps", 1, self.beep_callback)

    def beep(self, duration):
        self.buzz.value(1)
        self.buzz_start = time.ticks_ms()
        self.duration = duration

    def beep_off(self, t):
        self.buzz.value(0)
        self.duration = 0
        self.buzz_start = 0

    def beep_callback(self, t):
        if self.buzz_start != 0:
            tm = time.ticks_ms()
            if time.ticks_diff(tm, self.buzz_start) > self.duration:
                self.beep_off(t)
