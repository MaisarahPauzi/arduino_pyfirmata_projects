import pyfirmata
import time

board = pyfirmata.Arduino('COM3')

# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()

# set up pin D9 as Servo Output
pin9 = board.get_pin('d:9:s')

def move_servo(angle):
    pin9.write(angle)

while True:
    move_servo(180)