import cv2
import numpy as np
import pyfirmata
import time

board = pyfirmata.Arduino('COM3')

# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()


# set up pin D8 & D9 as Servo Output
# D8 = pan
pan_pin = board.get_pin('d:8:s')
# D9 = tilt
tilt_pin = board.get_pin('d:9:s')

board.digital[13].write(1)

def move_servo_tilt(angle):
    tilt_pin.write(angle)

def move_servo_pan(angle):
    pan_pin.write(angle)

camera = cv2.VideoCapture(0)

def nothing(x):
    pass
cv2.namedWindow('image')
cv2.createTrackbar('pan','image',0,180,nothing)
cv2.createTrackbar('tilt','image',0,180,nothing)

while True:
    ret, frame = camera.read()
    
    # show window frame contain live camera video
    cv2.imshow("image", frame)

    # wait for key every 1 millisecond
    key = cv2.waitKey(1)

    # if keyboard key "q" pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # get current positions of  trackbar
    pan_angle = cv2.getTrackbarPos('pan','image')
    tilt_angle = cv2.getTrackbarPos('tilt','image')
    move_servo_pan(pan_angle)
    move_servo_tilt(tilt_angle)

board.exit()
camera.release()
cv2.destroyAllWindows()
