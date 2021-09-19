from machine import Pin
import time



STATE_UNPRESSED=1
STATE_PRESSED=2

class Buttons:
    PINS = {
    1: 2,
    2: 17,
    3: 15,
}
    class Button:

        class Callback:
            def __init__(self, callback, min=0, max=-1):
                self.callback = callback
                self.min = min
                self.max = max

        def __init__(self, number):
            self.pin = Pin(Buttons.PINS[number], Pin.IN, Pin.PULL_UP)
            self.number = number
            self.state = STATE_UNPRESSED
            self.callbacks = []
            self.pressed_time = None

        def add_callback(self, callback, min=0, max=-1):
            callback_obj = self.Callback(callback, min, max)
            self.callbacks.append(callback_obj)
            return callback_obj

    def __init__(self, scheduler):
        self.buttons = []
        scheduler.schedule("button-press", 1, self.millis_callback)

    def add_button(self, number):
        button = Buttons.Button(number)
        self.buttons.append(button)
        return button

    def millis_callback(self, t):
        for button in self.buttons:
            if len(button.callbacks)>0:
                if button.state == STATE_UNPRESSED and button.pin.value() == 0:
                    button.state = STATE_PRESSED
                    button.pressed = time.ticks_ms()
                elif button.state == STATE_PRESSED and button.pin.value() == 1:
                    button.state = STATE_UNPRESSED
                    tm = time.ticks_ms()
                    press_duration = time.ticks_diff(tm, button.pressed)
                    print("Button %d pressed for %dms" %(button.number, press_duration))
                    for callback in button.callbacks:
                        if callback.min < press_duration and (callback.max==-1 or press_duration <= callback.max):
                            callback.callback(t)
                    button.pressed = None
