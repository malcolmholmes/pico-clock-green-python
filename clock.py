import time
from apps import App
from display import Display
from rtc import RTC
from buttons import Buttons


class Clock(App):
    def __init__(self, scheduler):
        App.__init__(self, "Clock", "clock")
        self.display = Display(scheduler)
        self.rtc = RTC()
        self.enabled = True
        self.buttons = Buttons(scheduler)
        scheduler.schedule("clock-second", 1000, self.secs_callback)
        scheduler.schedule("clock-minute", 60000, self.mins_callback)

    def enable(self):
        self.enabled = True
        self.update_time()
        self.buttons.add_callback(3, self.backlight_callback, max=500)

    def disable(self):
        self.enabled = False

    def secs_callback(self, t):
        if self.enabled:
            t = time.time()
            if t % 2 == 0:
                self.display.show_char(":", pos=10)
            else:
                self.display.show_char(" :", pos=10)

    def mins_callback(self, t):
        if self.enabled:
            self.update_time()

    def update_time(self):
        t = self.rtc.get_time()
        now = "%02d:%02d" % (t[3], t[4])
        self.display.show_day(t[6])
        self.display.show_text(now)

    def backlight_callback(self, t):
        self.display.switch_backlight()

