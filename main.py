import time
from display import Display
from speaker import Speaker
from buttons import Buttons
from scheduler import Scheduler
from clock import Clock
from rtc import RTC

scheduler = Scheduler()

display = Display(scheduler)

#display.show_icon("°C")
#display.show_icon("MoveOn")
#display.show_text("05:12")

speaker = Speaker(scheduler)

def short_button_action(t):
    print("BUTTON!")
    speaker.beep(100)

def long_button_action(t):
    print("LOOOOOONG BUTTON!")

buttons = Buttons(scheduler)
button1 = buttons.add_button(1)
button2 = buttons.add_button(2)

button1.add_callback(short_button_action, max=500)
button1.add_callback(long_button_action, min=500)

rtc = RTC()

clock = Clock(scheduler, display, rtc)

print("STARTING...")
scheduler.start()

while True:
    time.sleep(1)
    print(".", end="")
