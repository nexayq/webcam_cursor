#!/usr/bin/env python2

import cv2
import numpy as np
import time

#  np.set_printoptions(threshold=np.inf)
data = np.zeros([480, 640])

# get video input from web camera
cap = cv2.VideoCapture(0)
#  cap.set(cv2.CAP_PROP_MODE, 2)
#  cap.set(cv2.CAP_PROP_MODE, cv2.CAP_MODE_YUYV)
cap.set(cv2.CAP_PROP_CONVERT_RGB, False)
print( cap.get(cv2.CAP_PROP_CONVERT_RGB) )
#  cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
#  cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)

while True:
        _,frame = cap.read()
        #  frame = cv2.GrabFrame(cap)
        #  frame = cv2.grab(cap)
        #  print(frame)

        #  print(frame)
        #  print(frame.shape)
        #  print(frame._)

        #  image = cv2.cvtColor(frame, cv2.COLOR_YUYV2GRAY)
        #  image = frame[0][0][0]
        #  image = frame(:,:,0)
        #  for i in range(0,480):
            #  for j in range(0,640):
                #  #  print(i,j,frame[i,j,0])
                #  data[i,j] = int(frame[i,j,0])
        image = frame[:,:,0].astype(np.uint8)
        print()
        print(frame.shape)
        #  print(image.shape)
        print(image)
        print()
        print()
        #  gray = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        cv2.imshow("Web cam input", image)
        #  cv2.imshow('im', cv2.imdecode(cap,-1))
        #  cv2.imshow('im', cv2.imdecode(image,-1))
        #  time.sleep(0.1)
        time.sleep(0.01)
        #  time.sleep(2)

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break

        #  time.sleep(0.1)
