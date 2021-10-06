from apps import App
from buttons import Buttons
from display import Display
from rtc import RTC

month_max = {
    1: 31, # January
    2: 29, # February
    3: 31, # March
    4: 30, # April
    5: 31, # May
    6: 30, # June
    7: 31, # July
    8: 31, # August
    9: 30, # September
    10: 31, # October
    11: 30, # November
    12: 31, # December
}

class TimeSet(App):
    class State:
        def __init__(self, name, position, panel, index, max, length=2, offset=0):
            self.name = name
            self.position = position
            self.panel = panel
            self.index = index
            self.max = max
            self.length = length
            self.offset = offset

    def __init__(self, scheduler):
        App.__init__(self, "Time Set", "timeset")

        self.display = Display(scheduler)
        self.scheduler = scheduler
        self.buttons = Buttons(scheduler)
        self.rtc = RTC()
        self.grab_top_button = True
        self.enabled = False
        self.state = None
        self.state_index = -1
        self.flash_count = 0
        self.flash_state = False
        scheduler.schedule("time-set-half-second", 500, self.half_secs_callback)
        scheduler.schedule("time-set-minute", 60000, self.mins_callback)
        self.initialise_states()

    def initialise_states(self):
        self.states = [
            TimeSet.State("hours", 0, "time", 3, 24),
            TimeSet.State("minutes", 13, "time", 4, 60),
            TimeSet.State("year", 0, "year", 0, 3000, length=4),
            TimeSet.State("month", 0, "date", 1, 12, offset=1),
            TimeSet.State("day", 13, "date", 2, -1, offset=1),
        ]

    def enable(self):
        self.enabled = True
        self.state_index = 0
        self.state = self.states[self.state_index]
        self.update_display()
        self.buttons.add_callback(2, self.up_callback, max=500)
        self.buttons.add_callback(3, self.down_callback, max=500)

    def disable(self):
        self.active = False
        self.enabled = False
        self.state = None

    def half_secs_callback(self, t):
        if self.enabled:
            self.flash_count = (self.flash_count+1)%3
            if self.flash_count == 2:
                if self.state.length == 2:
                    self.display.show_text("  ", pos=self.state.position)
                elif self.state.length == 4:
                    self.display.show_text("    ", pos=self.state.position)
                self.flash_state = False
            else:
                if not self.flash_state:
                    self.flash_state = True
                    if self.state.length == 2:
                        self.display.show_text("%02d" % self.time[self.state.index], pos=self.state.position)
                    elif self.state.length == 4:
                        self.display.show_text("%04d" % self.time[self.state.index], pos=self.state.position)

    def mins_callback(self, t):
        if self.enabled:
            self.update_display()

    def update_display(self):
        self.time = self.rtc.get_time()
        self.display.clear()
        if self.state.panel == "time":
            t = self.rtc.get_time()
            now = "%02d:%02d" % (t[3], t[4])
            self.display.show_text(now)

        elif self.state.panel == "year":
            t = self.rtc.get_time()
            now = "%04d" % (t[0])
            self.display.show_text(now)

        elif self.state.panel == "date":
            t = self.rtc.get_time()
            now = "%02d/%02d" % (t[1], t[2])
            self.display.show_text(now)

    def up_callback(self, t):
        self.active = True
        t = list(self.rtc.get_time())
        max = self.state.max
        if max ==-1:
            # This is "day of month", which varies
            month = t[1]
            max = month_max[month]

        t[self.state.index] = (t[self.state.index]+1-self.state.offset) % max + self.state.offset
        self.rtc.save_time(tuple(t))
        self.flash_count = 0
        self.update_display()

    def down_callback(self, t):
        self.active = True
        t = list(self.rtc.get_time())
        max = self.state.max
        if max ==-1:
            # This is "day of month", which varies
            month = t[1]
            max = month_max[month]

        t[self.state.index] = (t[self.state.index]-1-self.state.offset) % max + self.state.offset
        self.rtc.save_time(tuple(t))
        self.flash_count = 0
        self.update_display()

    def stop_callback(self, t):
        self.scheduler.disable_app(self.name)

    def top_button(self, t):
        self.flash_count = 0
        self.state_index = (self.state_index + 1) % len(self.states)
        self.state = self.states[self.state_index]
        self.display.clear()
        self.update_display()
