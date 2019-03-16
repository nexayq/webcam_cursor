#!/usr/bin/env python2

from __future__ import print_function, division
import cv2
from cv2 import aruco
import numpy as np
import time


image_data = np.zeros([480, 640])

# get video input from web camera
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_CONVERT_RGB, False)
print( cap.get(cv2.CAP_PROP_CONVERT_RGB) )
#  print(cap.get(3))
#  cap.set(3,1280)
#  cap.set(4,720)

#  ret = cap.set(3,320)
#  print(ret)
#  cap.set(4,240)
#  print(cap.get(3))
#  print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#  print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#  cap.set(cv2.CV_CAP_PROP_FOURCC, cv2.CV_FOURCC('M', 'J', 'P', 'G') );
#  cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
#  cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

#  print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#  print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
        _,frame = cap.read()
        #  print(frame)
        #  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = frame[:,:,0].astype(np.uint8)

        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        #  frame_markers = gray
        #  frame_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids)
        #  gray_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids)

        #  if ids is not None:
            #  for i in range(len(ids)):
                #  c = corners[i]
                #  #  print("c[" + str(i) + "] = " + str(c[i]))
                #  #  print("c[" + str(i) + "] = " + str(c[i]))
                #  print("x = " + str(c[i][0][0]))
                #  print("y = " + str(c[i][0][1]))
                #  print("")

        #  frame_markers = frame
        #  if rejectedImgPoints:
            #  print(rejectedImgPoints)
            #  print(rejectedImgPoints[0][0][0])
            #  print(int(rejectedImgPoints[0][0][0][0]))
            #  print()

            #  x1 = int(rejectedImgPoints[0][0][0][0])
            #  y1 = int(rejectedImgPoints[0][0][0][1])

            #  x2 = x1 + 30
            #  y2 = y1 + 30

            #  #  frame_markers = cv2.rectangle(frame,(384,0),(510,128),(0,255,0),3)
            #  frame_markers = cv2.rectangle(frame_markers,(x1,y1),(x2,y2),(0,255,0),3)
        #  else:
            #  frame_markers = frame

        cv2.imshow("Web cam input", gray)
        #  cv2.imshow("Gray input", gray_markers)

        time.sleep(0.03)
        #  time.sleep(1)

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break

        #  time.sleep(0.1)
