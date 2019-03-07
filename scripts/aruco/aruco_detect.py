#!/usr/bin/env python2

import cv2
from cv2 import aruco
import numpy as np


# get video input from web camera
cap = cv2.VideoCapture(0)
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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        #  gray_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids)

        if ids is not None:
            for i in range(len(ids)):
                c = corners[i]
                #  print("c[" + str(i) + "] = " + str(c[i]))
                #  print("c[" + str(i) + "] = " + str(c[i]))
                print("x = " + str(c[i][0][0]))
                print("y = " + str(c[i][0][1]))
                print("")


        cv2.imshow("Web cam input", frame_markers)
        #  cv2.imshow("Gray input", gray_markers)

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break

        #  time.sleep(0.1)
