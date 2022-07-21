from scheduler import Scheduler
from clock import Clock
from apps import Apps
from pomodoro import Pomodoro
from time_set import TimeSet
import machine
machine.freq(250_000_000)

APP_CLASSES = [
    Clock,
    Pomodoro,
    TimeSet,
]

scheduler = Scheduler()
apps = Apps(scheduler)
for App in APP_CLASSES:
    apps.add(App(scheduler))

print("STARTING...")
scheduler.start()
