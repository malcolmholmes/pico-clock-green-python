import time
from apps import App
from buttons import Buttons
from display import Display
from speaker import Speaker


class Pomodoro:
    def __init__(self, scheduler):
        App.__init__(self, "Pomodoro", "pomod")
        self.display = Display(scheduler)
        self.speaker = Speaker(scheduler)
        self.scheduler = scheduler
        self.buttons = Buttons()
        self.enabled = False
        self.started = False
        self.start_time = None
        self.time_left = None
        scheduler.schedule("pomodoro-second", 1000, self.secs_callback)
        self.pomodoro_duration = 25 * 60  # 25 mins

    def enable(self):
        self.enabled = True
        t = "%02d:%02d" % (self.pomodoro_duration // 60, self.pomodoro_duration % 60)
        self.display.show_text(t)
        self.buttons.add_callback(2, self.start_callback, max=500)
        self.buttons.add_callback(2, self.clear_callback, min=500)

    def disable(self):
        self.enabled = False
        self.started = False
        self.start_time = None

    def start(self):
        self.started = True
        self.start_time = time.ticks_ms()
        if not self.time_left:
            self.time_left = self.pomodoro_duration

    def _time_left(self):
        return self.time_left - (
            time.ticks_diff(time.ticks_ms(), self.start_time) / 1000
        )

    def stop(self):
        self.started = False
        self.time_left = self._time_left()

    def secs_callback(self, t):
        if self.enabled and self.started:
            now = int(self._time_left())
            t = "%02d:%02d" % (now // 60, now % 60)
            self.display.show_text(t)
            if now <= 0:
                self.speaker.beep(1000)
                self.started = False
                self.start_time = None
                self.time_left = None

    def start_callback(self, t):
        if self.enabled and self.started:
            self.stop()
        else:
            print("START POMODORO")
            self.start()

    def clear_callback(self, t):
        self.stop()
        self.enable()
