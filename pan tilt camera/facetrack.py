import cv2
import numpy as np
import pyfirmata
import time


face_clsfr=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
p_angle = 50
t_angle = 35

GREEN = (0,255,0)
WHITE = (255,255,255)
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
    global t_angle
    t_angle += angle
    if(t_angle > 0 and t_angle <= 180):
        tilt_pin.write(t_angle)

def move_servo_pan(angle):
    global p_angle
    p_angle += angle
    if(p_angle > 0 and p_angle <= 180):
        pan_pin.write(p_angle)

camera = cv2.VideoCapture(0)


cv2.namedWindow('image')


while True:
    ret, frame = camera.read()

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_clsfr.detectMultiScale(gray,1.3,5)
    # detect faces
    for (x,y,w,h) in faces:
        # draw rectangle to detected face
        cv2.rectangle(frame,(x,y),(x+w,y+h),GREEN,2)
        
        # draw rectange for background of text
        cv2.rectangle(frame,(x,y-40),(x+w,y),GREEN,-1)
        
        # coordinate text
        centre_x = x+int(w/2)
        centre_y = y+int(h/2)
        
        # check x-axis coordinate to move pan servo
        if (centre_x > 0 and centre_x < 250):
            x_direction = 'left'
            move_servo_pan(-1)

        elif (centre_x >=250 and centre_x < 400):
            x_direction = 'center'
            move_servo_pan(0)
        else:
            x_direction = 'right'
            move_servo_pan(1)
            
        coord_text = f'X direction = {x_direction}'
        
        
        # put dot in the middle of face
        cv2.circle(frame, (centre_x, centre_y), 7, GREEN, -1)
        
        # draw text of detected face (wear mask or not)
        cv2.putText(frame, coord_text, (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,WHITE,2)
    # show window frame contain live camera video
    cv2.imshow("image", frame)

    # wait for key every 1 millisecond
    key = cv2.waitKey(2)

    # if keyboard key "q" pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # tilt stay at default angle.
    move_servo_tilt(0)

board.exit()    
camera.release()
cv2.destroyAllWindows()
