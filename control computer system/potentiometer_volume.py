import pyfirmata
import time

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

board = pyfirmata.Arduino('COM3')

it = pyfirmata.util.Iterator(board)
it.start()

analog_input = board.get_pin('a:0:i')

while True:
    analog_value = analog_input.read()
    if analog_value is not None:
        scalarVolume = int(analog_value*100) / 100
        print(scalarVolume)
        volume.SetMasterVolumeLevelScalar(scalarVolume, None)
    time.sleep(0.1)


