
import cv2
import numpy as np
import pyfirmata
import time

board = pyfirmata.Arduino('/dev/ttyUSB0')

# start an iterator thread so
# serial buffer doesn't overflow
iter8 = pyfirmata.util.Iterator(board)
iter8.start()


# set up pin D8 & D9 as Servo Output
# D8 = pan
pan_pin = board.get_pin('d:8:s')
# D9 = tilt
tilt_pin = board.get_pin('d:9:s')

def move_servo_tilt(angle):
    tilt_pin.write(angle)

def move_servo_pan(angle):
    pan_pin.write(angle)


def nothing(x):
    pass
cv2.namedWindow('image')
cv2.createTrackbar('pan','image',0,180,nothing)
cv2.createTrackbar('tilt','image',0,180,nothing)

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)

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

camera.release()
cv2.destroyAllWindows()
