#!/usr/bin/env python2

import cv2
import numpy as np

# get video input from web camera
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)

while True:
        _,frame = cap.read()
        #  print(frame)

        cv2.imshow("Web cam input", frame)

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break

        #  time.sleep(0.1)
