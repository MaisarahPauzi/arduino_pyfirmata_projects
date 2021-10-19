import cv2
import numpy as np
import face_recognition
import pyfirmata

board = pyfirmata.Arduino('COM13')
relay = board.digital[8]

camera = cv2.VideoCapture(1)
open_relay = False

while True:
    _, frame = camera.read()

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(image)
    
    face_encodings = face_recognition.face_encodings(image, face_locations)

    known_image = face_recognition.load_image_file("dp.jpg")
    known_image_encoding = face_recognition.face_encodings(known_image) 

    name = "Unknown"

    for face_location, face_encoding in zip(face_locations, face_encodings):
        top, right, bottom, left  = face_location

        matches = face_recognition.compare_faces(known_image_encoding,face_encoding)

        if True in matches:
            name = "Verified"
            open_relay = True
        
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,name,(left, top), font, 1 ,(0,255,0),2)
        cv2.rectangle(frame,(left, top),(right, bottom),(0,255,0),2)

    if len(face_locations) == 0 and name == "Unknown":
        open_relay = False
    
    if open_relay:
        relay.write(0)
    else:
        relay.write(1)
    # show window frame contain live camera video
    cv2.imshow("frame", frame)

    # wait for key every 1 millisecond
    key = cv2.waitKey(1)

    # if keyboard key "q" pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
board.exit()
camera.release()
cv2.destroyAllWindows()
exit()
