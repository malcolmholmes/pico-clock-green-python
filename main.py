import time
from display import Display

display = Display()

display.show_icon("°C")
display.show_icon("MoveOn")

display.start()
while True:
    for day in ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]:
        print("Displaying", day)
        display.show_icon(day)
        time.sleep(1)

    for day in ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]:
        print("Hiding", day)
        display.hide_icon(day)
        time.sleep(1)
    
