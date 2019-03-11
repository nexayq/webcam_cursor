#!/usr/bin/env python2

from __future__ import print_function, division
import time
import pyautogui
import cv2
import numpy as np
#  import gtk # python-gtk2
import PyQt4.QtGui # python-qt4

def get_pixel_colour(i_x, i_y):
        app = PyQt4.QtGui.QApplication([])
        long_qdesktop_id = PyQt4.QtGui.QApplication.desktop().winId()
        long_colour = PyQt4.QtGui.QPixmap.grabWindow(long_qdesktop_id, i_x, i_y, 1, 1).toImage().pixel(0, 0)
        i_colour = int(long_colour)
        return ((i_colour >> 16) & 0xff), ((i_colour >> 8) & 0xff), (i_colour & 0xff)

#  print get_pixel_colour(0, 0)

while(1):
    x, y = pyautogui.position()
    #  print get_pixel_colour(100, 100)
    print("Cursor:", x, y)
    rgb = get_pixel_colour(x, y)
    bgr = rgb[2], rgb[1], rgb[0]
    #  hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(np.uint8([[bgr]]),cv2.COLOR_BGR2HSV)[0][0]
    print("BGR:", bgr)
    print("HSV:", hsv)
    time.sleep(1)
