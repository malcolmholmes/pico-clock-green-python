from machine import SoftI2C
from machine import Pin
from ds3231_port import DS3231
from util import singleton


@singleton
class RTC:
    def __init__(self):
        rtc_i2c = SoftI2C(scl=Pin(7), sda=Pin(6), freq=100000)
        self.ds = DS3231(rtc_i2c)
        pass

    def get_time(self):
        return self.ds.get_time()

    def save_time(self, t):
        return self.ds.save_time(t)
