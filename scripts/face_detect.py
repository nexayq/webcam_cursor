#!/usr/bin/env python2

import cv2
import numpy as np
import dlib

# get video input from web camera
cap = cv2.VideoCapture(0)
#  cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
#  cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)
detector =  dlib.get_frontal_face_detector()

# download shape predictor
#   > wget https://github.com/AKSHAYUBHAT/TensorFace/raw/master/openface/models/dlib/shape_predictor_68_face_landmarks.dat
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
        _,frame = cap.read()
        #  print(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x,y), 4, (0, 255, 0), -1)

        cv2.imshow("Web cam input", frame)

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break

        #  time.sleep(0.1)
