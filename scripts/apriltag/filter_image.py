#!/usr/bin/env python2

from __future__ import print_function, division
import cv2
import numpy as np
import apriltag

#  img = cv2.imread('image_012.jpg')
img = cv2.imread('image_00.jpg')

# moving average
kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(img,-1,kernel)

# blur
#  blurred = cv2.blur(img,(5,5))
#  blurred = cv2.GaussianBlur(img,(5,5),0)
#  blurred = cv2.medianBlur(img,5)
blurred = cv2.bilateralFilter(img,9,75,75)

final = blurred

# aruco
gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
detector = apriltag.Detector()
result = detector.detect(gray)

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
    frame_markers = cv2.rectangle(final,(x1,y1),(x2,y2),(0,255,0),3)
else:
    frame_markers = final

#  while True:
cv2.imshow('img', img)
#  cv2.imshow('dst', dst)
cv2.imshow('filtered', frame_markers)

cv2.waitKey(0)
cv2.destroyAllWindows()
#  cv2.imshow('blurred', blurred)
