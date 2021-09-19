import time

class Pomodoro:
    def __init__(self, scheduler, display, speaker):
        self.name = "Pomodoro"
        self.display = display
        self.speaker = speaker
        self.scheduler = scheduler
        self.enabled = False
        self.started = False
        self.start_time = None
        scheduler.schedule("pomodoro-second", 1000, self.secs_callback)
        scheduler.add_app(self)
        self.pomodoro_duration=25*60 # 25 mins

    def enable(self):
        self.enabled = True
        t = "%02d:%02d" % (self.pomodoro_duration // 60, self.pomodoro_duration % 60)
        self.display.show_text(t)
        
    def disable(self):
        self.enabled = False
        self.started = False
        self.start_time = None
        
    def start(self):
        self.started = True
        if not self.start_time:
            self.start_time = time.ticks_ms()

    def stop(self):
        self.started = False

    def secs_callback(self, t):
        if self.enabled and self.started:
            now = int(self.pomodoro_duration - (time.ticks_diff(time.ticks_ms(), self.start_time)/1000))
            t = "%02d:%02d" % (now // 60, now % 60)
            self.display.show_text(t)
            if now <=0:
                self.speaker.beep(1000)
                self.started = False
                self.start_time = None

    def start_callback(self, t):
        if not self.enabled:
            print("ENABLE POMODORO")
            self.scheduler.enable_app(self.name)
        elif self.enabled and self.started:
            self.stop()
        else:
            print("START POMODORO")
            self.start()

    def stop_callback(self, t):
        self.scheduler.disable_app(self.name)
