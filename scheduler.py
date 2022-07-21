from machine import Timer
import time


class Scheduler:
    class Schedule:
        def __init__(self, name, duration, callback):
            self.name = name
            self.duration = duration
            self.callback = callback
            self.lastrun = time.ticks_ms()

    count = 0

    def __init__(self):
        self.schedules = []

    def start(self):
        self.start = time.ticks_ms()
        self.timer = Timer(period=1, callback=self.event_callback)

    def schedule(self, name, duration, callback):
        self.schedules.append(self.Schedule(name, duration, callback))

    def remove(self, name):
        for schedule in self.schedules:
            if schedule.name == name:
                self.schedules.remove(schedule)

    def event_callback(self, t):
        for schedule in self.schedules:
            if schedule.duration == 1:
                schedule.callback(t)
            else:
                tm = time.ticks_ms()
                if time.ticks_diff(tm, schedule.lastrun) > schedule.duration:
                    schedule.callback(t)
                    schedule.lastrun = tm
