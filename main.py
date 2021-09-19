import time
from display import Display
from speaker import Speaker
from buttons import Buttons
from scheduler import Scheduler
from clock import Clock
from rtc import RTC
from pomodoro import Pomodoro

scheduler = Scheduler()

display = Display(scheduler)

#display.show_icon("°C")
#display.show_icon("MoveOn")
#display.show_text("05:12")

speaker = Speaker(scheduler)
buttons = Buttons(scheduler)
button1 = buttons.add_button(1)
button2 = buttons.add_button(2)

rtc = RTC()

clock = Clock(scheduler, display, rtc)

pomodoro = Pomodoro(scheduler, display, speaker)
button1.add_callback(pomodoro.start_callback, max=500)
button1.add_callback(pomodoro.stop_callback, min=500)

print("STARTING...")
scheduler.start()

while True:
    time.sleep(1)
    print(".", end="")
