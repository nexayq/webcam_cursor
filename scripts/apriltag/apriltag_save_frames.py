#!/usr/bin/env python2

from __future__ import print_function, division
import cv2
#  from cv2 import aruco
import apriltag
import numpy as np


# get video input from web camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
print(cap.get(cv2.CAP_PROP_FPS))
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
idx = 0

while True:
        _,frame = cap.read()
        #  print(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #  aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        #  parameters =  aruco.DetectorParameters_create()
        #  corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        #  frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        #  gray_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids)

        detector = apriltag.Detector()
        result = detector.detect(gray)
        #  print(result)

        if result:
            tf = result[0].tag_family
            cx = result[0].center[0]
            print(tf)
            print(cx)


        frame_markers = frame

        #  if ids is not None:
            #  for i in range(len(ids)):
                #  c = corners[i]
                #  #  print("c[" + str(i) + "] = " + str(c[i]))
                #  #  print("c[" + str(i) + "] = " + str(c[i]))
                #  print("x = " + str(c[i][0][0]))
                #  print("y = " + str(c[i][0][1]))
                #  print("")


        cv2.imshow("Web cam input", frame_markers)
        #  cv2.imshow("Gray input", gray_markers)

        # save frames
        image_path = "images/image_0" + str(idx) + ".jpg"
        cv2.imwrite(image_path, frame_markers)
        idx = idx + 1

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break

        #  time.sleep(0.1)
