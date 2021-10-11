from machine import Pin, Timer

from util import singleton


@singleton
class Display:
    def __init__(self, scheduler):
        self.a0 = Pin(16, Pin.OUT)
        self.a1 = Pin(18, Pin.OUT)
        self.a2 = Pin(22, Pin.OUT)

        self.sdi = Pin(11, Pin.OUT)
        self.clk = Pin(10, Pin.OUT)
        self.le = Pin(12, Pin.OUT)

        self.row = 0
        self.count = 0
        self.leds = [[0] * 32 for i in range(0, 8)]
        self.leds_changed = False
        self.disp_offset = 2
        self.initialise_fonts()
        self.initialise_icons()
        scheduler.schedule("enable-leds", 1, self.enable_leds)

    def enable_leds(self, t):
        self.count += 1
        self.row = (self.row + 1) % 8
        led_row = self.leds[self.row]
        if True:
            for col in range(32):
                self.clk.value(0)
                self.sdi.value(led_row[col])
                self.clk.value(1)
            self.le.value(1)
            self.le.value(0)
            self.leds_changed = False

        self.a0.value(1 if self.row & 0x01 else 0)
        self.a1.value(1 if self.row & 0x02 else 0)
        self.a2.value(1 if self.row & 0x04 else 0)

    def clear(self, x=0, y=0, w=24, h=7):
        for yy in range(y, y + h + 1):
            for xx in range(x, x + w + 1):
                self.leds[yy][xx] = 0

    def show_char(self, character, pos):
        pos += self.disp_offset  # Plus the offset of the status indicator
        char = self.ziku[character]
        for row in range(1, 8):
            byte = char.rows[row - 1]
            for col in range(0, char.width):
                self.leds[row][pos + col] = (byte >> col) % 2
        self.leds_changed = True

    def show_text(self, text, pos=0):
        i = 0
        while i < len(text):
            if text[i:i + 2] in self.ziku:
                c = text[i:i + 2]
                i += 2
            else:
                c = text[i]
                i += 1
            char = self.ziku[c]
            self.show_char(c, pos)
            width = self.ziku[c].width
            pos += width + 1

    def show_icon(self, name):
        icon = self.Icons[name]
        for w in range(icon.width):
            self.leds[icon.y][icon.x + w] = 1
        self.leds_changed = True

    def hide_icon(self, name):
        icon = self.Icons[name]
        for w in range(icon.width):
            self.leds[icon.y][icon.x + w] = 0
        self.leds_changed = True

    def backlight_on(self):
        self.leds[0][2] = 1
        self.leds[0][5] = 1

    def backlight_off(self):
        self.leds[0][2] = 0
        self.leds[0][5] = 0

    def print(self):
        for row in range(0, 8):
            for pos in range(0, 24):
                print("X" if self.leds[row][pos] == 1 else " ", end="")
            print("")

    def square(self):
        '''
        Prints a crossed square. For debugging purposes.
        '''
        for row in range(1, 8):
            self.leds[row][2] = 1
            self.leds[row][23] = 1
        for col in range(2, 23):
            self.leds[1][col] = 1
            self.leds[7][col] = 1
            self.leds[int(col / 24 * 7) + 1][col] = 1
            self.leds[7 - int(col / 24 * 7)][col] = 1

    class Character:
        def __init__(self, width, rows, offset=2):
            self.width = width
            self.rows = rows
            self.offset = offset

    class Icon:
        def __init__(self, x, y, width=1):
            self.x = x
            self.y = y
            self.width = width

    def initialise_icons(self):
        self.Icons = {
            "MoveOn": self.Icon(0, 0, width=2),
            "AlarmOn": self.Icon(0, 1, width=2),
            "CountDown": self.Icon(0, 2, width=2),
            "°F": self.Icon(0, 3),
            "°C": self.Icon(1, 3),
            "AM": self.Icon(0, 4),
            "PM": self.Icon(1, 4),
            "CountUp": self.Icon(0, 5, width=2),
            "Hourly": self.Icon(0, 6, width=2),
            "AutoLight": self.Icon(0, 7, width=2),
            "Mon": self.Icon(3, 0, width=2),
            "Tue": self.Icon(6, 0, width=2),
            "Wed": self.Icon(9, 0, width=2),
            "Thur": self.Icon(12, 0, width=2),
            "Fri": self.Icon(15, 0, width=2),
            "Sat": self.Icon(18, 0, width=2),
            "Sun": self.Icon(21, 0, width=2),
        }
    day_of_week = {
        0: "Sun",
        1: "Mon",
        2: "Tue",
        3: "Wed",
        4: "Thur",
        5: "Fri",
        6: "Sat"      
        }
    def show_day(self, int):
        self.clear()
        self.show_icon(self.day_of_week[int])
        
    # Derived from c code created by yufu on 2021/1/23.
    # Modulus method: negative code, reverse, line by line, 4X7 font
    def initialise_fonts(self):
        self.ziku = {
            "all": self.Character(width=3, rows=[0x05,0x05,0x03,0x03,0x03,0x03,0x03]),
            "0": self.Character(width=4, rows=[0x06,0x09,0x09,0x09,0x09,0x09,0x06]),
            "1": self.Character(width=4, rows=[0x04,0x06,0x04,0x04,0x04,0x04,0x0E]),
            "2": self.Character(width=4, rows=[0x06,0x09,0x08,0x04,0x02,0x01,0x0F]),
            "3": self.Character(width=4, rows=[0x06,0x09,0x08,0x06,0x08,0x09,0x06]),
            "4": self.Character(width=4, rows=[0x08,0x0C,0x0A,0x09,0x0F,0x08,0x08]),
            "5": self.Character(width=4, rows=[0x0F,0x01,0x07,0x08,0x08,0x09,0x06]),
            "6": self.Character(width=4, rows=[0x04,0x02,0x01,0x07,0x09,0x09,0x06]),
            "7": self.Character(width=4, rows=[0x0F,0x09,0x04,0x04,0x04,0x04,0x04]),
            "8": self.Character(width=4, rows=[0x06,0x09,0x09,0x06,0x09,0x09,0x06]),
            "9": self.Character(width=4, rows=[0x06,0x09,0x09,0x0E,0x08,0x04,0x02]),
            "A": self.Character(width=4, rows=[0x06,0x09,0x09,0x0F,0x09,0x09,0x09]),
            "B": self.Character(width=4, rows=[0x07,0x09,0x09,0x07,0x09,0x09,0x07]),
            "C": self.Character(width=4, rows=[0x06,0x09,0x01,0x01,0x01,0x09,0x06]),
            "D": self.Character(width=4, rows=[0x07,0x09,0x09,0x09,0x09,0x09,0x07]),
            "E": self.Character(width=4, rows=[0x0F,0x01,0x01,0x0F,0x01,0x01,0x0F]),
            "F": self.Character(width=4, rows=[0x0F,0x01,0x01,0x0F,0x01,0x01,0x01]),
            "H": self.Character(width=4, rows=[0x09,0x09,0x09,0x0F,0x09,0x09,0x09]),
            "L": self.Character(width=4, rows=[0x01,0x01,0x01,0x01,0x01,0x01,0x0F]),
            "N": self.Character(width=4, rows=[0x09,0x09,0x0B,0x0D,0x09,0x09,0x09]),
            "O": self.Character(width=4, rows=[0x0F,0x09,0x09,0x09,0x09,0x09,0x0F]),
            "P": self.Character(width=4, rows=[0x07,0x09,0x09,0x07,0x01,0x01,0x01]),
            "U": self.Character(width=4, rows=[0x09,0x09,0x09,0x09,0x09,0x09,0x06]),
            ":": self.Character(width=2, rows=[0x00,0x03,0x03,0x00,0x03,0x03,0x00]),        #2×7
            " :": self.Character(width=2, rows=[0x00,0x00,0x00,0x00,0x00,0x00,0x00]),       # colon width space
            "°C": self.Character(width=4, rows=[0x01,0x0C,0x12,0x02,0x02,0x12,0x0C]),       # celcuis 5×7
            "°F": self.Character(width=4, rows=[0x01,0x1E,0x02,0x1E,0x02,0x02,0x02]),       # farenheit
            " ": self.Character(width=4, rows=[0x00,0x00,0x00,0x00,0x00,0x00,0x00]),        # space
            "Y": self.Character(width=4, rows=[0x1F,0x04,0x04,0x04,0x04,0x04,0x04]),        # 5*7
            ".": self.Character(width=1, rows=[0x00,0x00,0x00,0x00,0x00,0x00,0x01]),        # 1×7
            "-": self.Character(width=2, rows=[0x00,0x00,0x00,0x03,0x00,0x00,0x00]),        # 2×7
            "M": self.Character(width=4, rows=[0x00,0x11,0x1B,0x15,0x11,0x11,0x11,0x11]),   # 5×7
            "/": self.Character(width=2, rows=[0x02,0x02,0x02,0x01,0x01,0x01,0x01,0x01]),   # 3×7
            "°C2": self.Character(width=4, rows=[0x00,0x01,0x0C,0x12,0x02,0x02,0x12,0x0C]), # 5×7
            "°F2": self.Character(width=4, rows=[0x00,0x01,0x1E,0x02,0x1E,0x02,0x02,0x02]),
            "V": self.Character(width=5, rows=[0x11,0x11,0x11,0x11,0x11,0x0A,0x04]),        # 5×7
            "W": self.Character(width=5, rows=[0x11,0x11,0x11,0x15,0x15,0x1B,0x11]),        # 5×7
        }
        self.digital_tube = {
            "0": [0x0F, 0x09, 0x09, 0x09, 0x09, 0x09, 0x0F],
            "1": [0x08, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08],
            "2": [0x0F, 0x08, 0x08, 0x0F, 0x01, 0x01, 0x0F],
            "3": [0x0F, 0x08, 0x08, 0x0F, 0x08, 0x08, 0x0F],
            "4": [0x09, 0x09, 0x09, 0x0F, 0x08, 0x08, 0x08],
            "5": [0x0F, 0x01, 0x01, 0x0F, 0x08, 0x08, 0x0F],
            "5": [0x0F, 0x01, 0x01, 0x0F, 0x09, 0x09, 0x0F],
            "6": [0x0F, 0x08, 0x08, 0x08, 0x08, 0x08, 0x08],
            "7": [0x0F, 0x09, 0x09, 0x0F, 0x09, 0x09, 0x0F],
            "8": [0x0F, 0x09, 0x09, 0x0F, 0x08, 0x08, 0x0F],
            "A": [0x0F, 0x09, 0x09, 0x0F, 0x09, 0x09, 0x09],
            "B": [0x01, 0x01, 0x01, 0x0F, 0x09, 0x09, 0x0F],
            "C": [0x0F, 0x01, 0x01, 0x01, 0x01, 0x01, 0x0F],
            "D": [0x08, 0x08, 0x08, 0x0F, 0x09, 0x09, 0x0F],
            "E": [0x0F, 0x01, 0x01, 0x0F, 0x01, 0x01, 0x0F],
            "F": [0x0F, 0x01, 0x01, 0x0F, 0x01, 0x01, 0x01],
            "H": [0x09, 0x09, 0x09, 0x0F, 0x09, 0x09, 0x09],
            "L": [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x0F],
            "N": [0x0F, 0x09, 0x09, 0x09, 0x09, 0x09, 0x09],
            "P": [0x0F, 0x09, 0x09, 0x0F, 0x01, 0x01, 0x01],
            "U": [0x09, 0x09, 0x09, 0x09, 0x09, 0x09, 0x0F],
            ":": [0x00, 0x03, 0x03, 0x00, 0x03, 0x03, 0x00],  # 2×7
            "°C": [0x01, 0x1E, 0x02, 0x02, 0x02, 0x02, 0x1E],  # celcius 5×7
            "°F": [0x01, 0x1E, 0x02, 0x1E, 0x02, 0x02, 0x02],  # farenheit
            " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            "T": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],  # 5*7
            ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01],  # 2×7
            "-": [0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00],  # 2×7
            "M": [0x00, 0x11, 0x1B, 0x15, 0x11, 0x11, 0x11, 0x11],  # 5×7
            "/": [0x00, 0x04, 0x04, 0x02, 0x02, 0x02, 0x01, 0x01],  # 3×7
            "°C2": [0x00, 0x01, 0x0C, 0x12, 0x02, 0x02, 0x12, 0x0C],  # celcuis 5x7
            "°F2": [0x00, 0x01, 0x1E, 0x02, 0x1E, 0x02, 0x02, 0x02],  # farenheit
            "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F],  # 5×7
            "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],  # 5×7
        }
