#!/usr/bin/env python2

import cv2
import numpy as np
import pyautogui

# init
object_detected = 0
noise_X = 1
move_X_const  = 2

# get video input from web camera
cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)

while True:
        _,frame = cap.read()
        #  print(frame)

        # convert frame from BGR (RGB) format to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red color mask
        low_red = np.array([161, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        red = cv2.bitwise_and(frame, frame, mask=red_mask)

        # Blue color mask
        low_blue  = np.array([94, 80, 2])
        high_blue = np.array([126, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
        blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

        # Green color mask
        #  low_green  = np.array([25, 52, 72])
        low_green  = np.array([25, 100, 72])
        #  high_green = np.array([102, 255, 255])
        high_green = np.array([42, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)

        #  gray_image = cv2.cvtColor(green, cv2.COLOR_HSV2GRAY)
        #  print(green)
        #  print(green.shape)
        #  (480, 640, 3)
        #  print(green[0,0])

        #  for i in range(0,480):
            #  for j in range(0,640):
                #  if np.sum(green[i,j]) > 0:
                    #  print(green[i,j])

        #  for i in range(0,480):
            #  for j in range(0,640):
                #  if np.sum(green_mask[i,j]) > 0:
                    #  print(green_mask[i,j])

        # convert image to binary image
        ret,thresh = cv2.threshold(green_mask,127,255,0)

        # calculate moments of binary image
        M = cv2.moments(thresh)

        # calculate x,y coordinate of center
        if(M["m00"] != 0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            print(cX, cY)
            print(green[cY,cX])

            # move cursor
            if object_detected == 1:
                delta_X = cX - cX_prev
                #  print(delta_X)
                if (delta_X > noise_X):
                    #  pyautogui.moveRel(-move_X, None)
                    move_X = -delta_X*4
                    pyautogui.moveRel(move_X, None)
                    print("move_left: ", move_X)
                    #  pass
                elif (delta_X < -noise_X):
                    #  pyautogui.moveRel(move_X, None)
                    move_X = -delta_X*4
                    pyautogui.moveRel(move_X, None)
                    print("move_right: ", move_X)

            object_detected = 1
            cX_prev = cX
            cY_prev = cY

        # save matrix to file
        #  np.savetxt('out.txt', green, fmt='%s')

        #  cv2.imshow("Web cam input", frame)
        #  cv2.imshow("Red mask", red_mask)
        #  cv2.imshow("Red", red)
        #  cv2.imshow("Blue", blue)
        #  cv2.imshow("Green", green)
        #  cv2.imshow("Green", green[0])

        cv2.imshow("Green", green_mask)

        key = cv2.waitKey(1)
        #  if key == 27:
            #  break
