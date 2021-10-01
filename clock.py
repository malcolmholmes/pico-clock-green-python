import time
from apps import App

class Clock(App):
    def __init__(self, scheduler, display, rtc):
        App.__init__(self, "Clock", "clock")
        self.display = display
        self.rtc = rtc
        self.enabled = True
        self.scheduler = scheduler
        scheduler.schedule("clock-second", 1000, self.secs_callback)
        scheduler.schedule("clock-minute", 60000, self.mins_callback)

    def enable(self):
        self.enabled = True
        self.update_time()

    def disable(self):
        self.enabled = False

    def secs_callback(self, t):
        if self.enabled:
            t = time.time()
            if t%2==0:
                self.display.show_char(":", pos=10)
            else:
                self.display.show_char(" :", pos=10)

    def mins_callback(self, t):
        if self.enabled:
            self.update_time()
    
    def update_time(self):
        t = self.rtc.get_time()
        now = "%02d:%02d" % (t[3], t[4])
        self.display.show_text(now)
