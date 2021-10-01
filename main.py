import time
from display import Display
from speaker import Speaker
from buttons import Buttons
from scheduler import Scheduler
from clock import Clock
from rtc import RTC
from apps import Apps
from pomodoro import Pomodoro

scheduler = Scheduler()
display = Display(scheduler)
speaker = Speaker(scheduler)
buttons = Buttons(scheduler)
rtc = RTC()

apps = Apps(display, buttons)
apps.add(Clock(scheduler, display, rtc))
apps.add(Pomodoro(scheduler, display, speaker, buttons))

print("STARTING...")
scheduler.start()

while True:
    time.sleep(1)
    print(".", end="")
