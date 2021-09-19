from machine import Timer
import time
import _thread

class Scheduler:

    class Schedule:
        def __init__(self, name, duration, callback):
            self.name = name
            self.duration = duration
            self.callback = callback
            self.lastrun = time.ticks_ms()

    count=0
    def __init__(self):
        self.schedules = []
        self.apps = {}
        self.app_stack = []

    def start(self):
        self.start = time.ticks_ms()
        self.timer = Timer(period=1, callback=self.event_callback)

    def schedule(self, name, duration, callback):
        self.schedules.append(self.Schedule(name, duration, callback))

    def event_callback(self, t):
        for schedule in self.schedules:
            if schedule.duration == 1:
                schedule.callback(t)
            else:
                tm = time.ticks_ms()
                if time.ticks_diff(tm, schedule.lastrun) > schedule.duration:
                    schedule.callback(t)
                    schedule.lastrun = tm

    def add_app(self, app):
        self.apps[app.name] = app

    def enable_app(self, name):
        for n in self.app_stack:
            app = self.apps[n]
            app.disable()
        app = self.apps[name]
        self.app_stack.append(name)
        app.enable()

    def disable_app(self, name):
        for n in self.app_stack:
            if n == name:
                app = self.apps[n]
                app.disable()
        self.app_stack.remove(name)

        if len(self.app_stack)>0:
            n = self.app_stack[-1]
            app = self.apps[n]
            app.enable()
