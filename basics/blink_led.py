import pyfirmata
import time

board = pyfirmata.Arduino('COM3')

def all_on():
    for i in range(2,13):
        board.digital[i].write(1)

def all_off():
    for i in range(2,13):
        board.digital[i].write(0)

while True:
    all_on()
    time.sleep(1)
    all_off()
    time.sleep(1)