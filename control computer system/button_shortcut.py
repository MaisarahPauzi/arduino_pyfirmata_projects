import pyfirmata
import time
import pyautogui

board = pyfirmata.Arduino('COM3')

it = pyfirmata.util.Iterator(board)
it.start()

board.digital[7].mode = pyfirmata.INPUT
board.digital[8].mode = pyfirmata.INPUT


while True:
    red = board.digital[7].read()
    blue = board.digital[8].read()
    if red:
        pyautogui.hotkey('ctrl', 'c')
    if blue:
        pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)