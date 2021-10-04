from buttons import Buttons
from display import Display


class App:
    def __init__(self, name, label):
        self.name = name
        self.label = label
        self.active = False
        self.grab_top_button = False

    def top_button(self, t):
        print("top_button not implemented for " + self.name)


class Apps:
    def __init__(self, scheduler):
        self.display = Display(scheduler)
        self.buttons = Buttons(scheduler)
        self.apps = []
        self.current_app = 0
        self.buttons.add_callback(1, self.next, max=500)
        self.buttons.add_callback(1, self.previous, min=500)
        self.buttons.add_callback(1, self.exit, min=500)

    def add(self, app):
        if len(self.apps) == 0:
            app.enable()
        self.apps.append(app)

    def next(self, t):
        print("NEXT")
        if len(self.apps) == 0:
            return

        app = self.apps[self.current_app]
        if app.active and app.grab_top_button:
            app.top_button(t)
            return

        self.apps[self.current_app].disable()
        self.buttons.clear_callbacks(2)
        self.buttons.clear_callbacks(3)
        self.display.clear()
        self.current_app = (self.current_app + 1) % len(self.apps)
        print("SWITCHING TO", self.apps[self.current_app].name)
        self.apps[self.current_app].enable()

    def previous(self, t):
        print("PREVIOUS")
        if len(self.apps) > 0:
            self.apps[self.current_app].disable()
            self.current_app = (self.current_app - 1) % len(self.apps)
            self.apps[self.current_app].enable()

    def exit(self, t):
        if len(self.apps) > 0:
            self.apps[self.current_app].disable()
            self.current_app = 0
            self.apps[self.current_app].enable()
