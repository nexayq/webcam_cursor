#!/usr/bin/env python2

# Compatible only with python2, use "get_color_qt.py" instead!

from __future__ import print_function, division
import time
import pyautogui
import cv2
import numpy as np
import sys
#  if sys.version_info[0] < 3:
import gtk # python-gtk2
#  else:
    #  from gi.repository import Gtk
    #  from gi.repository import Gdk
    #  gtk = Gtk
    #  gdk = Gdk

def get_pixel_colour(i_x, i_y):
        o_gdk_pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, 1, 1)
        o_gdk_pixbuf.get_from_drawable(gtk.gdk.get_default_root_window(), gtk.gdk.colormap_get_system(), i_x, i_y, 0, 0, 1, 1)
        return tuple(o_gdk_pixbuf.get_pixels_array().tolist()[0][0])

while(1):
    x, y = pyautogui.position()
    #  print get_pixel_colour(100, 100)
    #  if sys.version_info[0] < 3:
        #  print "Cursor:", x, y
    #  else:
    print("Cursor:", x, y)
    rgb = get_pixel_colour(x, y)
    bgr = rgb[2], rgb[1], rgb[0]
    #  hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(np.uint8([[bgr]]),cv2.COLOR_BGR2HSV)[0][0]
    print("BGR:", bgr)
    print("HSV:", hsv)
    time.sleep(1)
