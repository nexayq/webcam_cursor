#!/usr/bin/env python2

from __future__ import print_function, division
import cv2
#  from cv2 import aruco
import apriltag
import numpy as np
import time

frames = [None]*5
#  frames = []

image_data = np.zeros([480, 640])


# get video input from web camera
cap = cv2.VideoCapture(0)
#  cap.set(cv2.CAP_PROP_FPS, 60)
#  print(cap.get(cv2.CAP_PROP_FPS))

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
idx = 0

while True:
        _,frame = cap.read()
        #  print(frame)
        #  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = frame[:,:,0].astype(np.uint8)
        #  aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        #  parameters =  aruco.DetectorParameters_create()
        #  corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        #  frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        #  gray_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids)
        #  frames[idx%2] = gray
        #  frames[int(idx%2)] = gray
        #  frames[0] = gray
        #  frames[1] = gray
        #  frames[idx%5] = gray
        #  print(idx%2)
        #  frames[idx%2] = gray
        #  if idx % 5 == 0 and idx != 0:
            #  #  frames.append(gray)
            #  del frames[0]
        #  if idx == 0:
            #  frames[1] = gray
            #  frames[2] = gray
            #  frames[3] = gray
            #  frames[4] = gray
        #  idx = idx + 1

        #  print(frames)
        #  median = np.median(frames, axis=0).astype(dtype=np.uint8)

        detector = apriltag.Detector()
        #  result = detector.detect(median)
        result = detector.detect(gray)
        #  print(result)

        if result:
            tf = result[0].tag_family
            cx = result[0].center[0]
            cy = result[0].center[1]
            print(tf)
            print(cx)
            print(cy)
            x1 = int(round(cx))
            y1 = int(round(cy))
            x2 = x1 + 10
            y2 = y1 + 10
            #  frame_markers = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
            #  frame_markers = cv2.rectangle(median,(x1,y1),(x2,y2),(0,255,0),3)
            frame_markers = cv2.rectangle(gray,(x1,y1),(x2,y2),(0,255,0),3)
        else:
            #  frame_markers = frame
            #  frame_markers = median
            frame_markers = gray

        #  if ids is not None:
            #  for i in range(len(ids)):
                #  c = corners[i]
                #  #  print("c[" + str(i) + "] = " + str(c[i]))
                #  #  print("c[" + str(i) + "] = " + str(c[i]))
                #  print("x = " + str(c[i][0][0]))
                #  print("y = " + str(c[i][0][1]))
                #  print("")


        cv2.imshow("Web cam input", frame_markers)
        #  cv2.imshow("Web cam input", median)
        #  cv2.imshow("Gray input", gray_markers)

        # save frames
        #  image_path = "images/image" + str(idx) + ".jpg"
        #  cv2.imwrite(image_path, frame_markers)
        #  idx = idx + 1
        #  prev_frame = frame
        time.sleep(0.03)

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break

        #  time.sleep(0.1)
