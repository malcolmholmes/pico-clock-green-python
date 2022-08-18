from scheduler import Scheduler
scheduler = Scheduler()
from display import Display
dis= Display(scheduler)
scheduler.start()
from rtc import RTC
clock=RTC()