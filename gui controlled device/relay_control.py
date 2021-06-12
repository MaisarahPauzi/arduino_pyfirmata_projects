
import pyfirmata
from guizero import App, PushButton

board = pyfirmata.Arduino('COM3')
board.digital[8].write(0)

def on():
    board.digital[8].write(1)
    on_button.disable()
    off_button.enable()

def off():
    board.digital[8].write(0)
    on_button.enable()
    off_button.disable()

app = App()
on_button = PushButton(app, command=on, text="TURN ON LAMP")
off_button = PushButton(app, command=off, text="TURN OFF LAMP", enabled=False)
app.display()
