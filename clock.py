import time

class Clock:
    def __init__(self, scheduler, display, rtc):
        self.display = display
        self.rtc = rtc
        scheduler.schedule("clock-second", 1000, self.secs_callback)
        scheduler.schedule("clock-minute", 60000, self.mins_callback)

    def secs_callback(self, t):
        t = time.time()
        if t%2==0:
            self.display.show_char(":", pos=10)
        else:
            self.display.show_char(" :", pos=10)

    def mins_callback(self, t):
        t = self.rtc.get_time()
        now = "%02d:%02d" % (t[3], t[4])
        self.display.show_text(now)
