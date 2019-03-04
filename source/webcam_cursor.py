#!/usr/bin/env python2

#  https://www.pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTimer

import cv2
import numpy as np
import pyautogui

# disable closing of app when upper left corner is reached
pyautogui.FAILSAFE = False
# improve speed drastically
pyautogui.PAUSE = 0

# Enter GUI filename
qtCreatorFile = "main.ui"

# load GUI file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# inherit GUI classes
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # paint selected color to widget
        self.colorSpinBox.valueChanged.connect(self.GetColor)
        color = self.colorSpinBox.value()

        # set init color
        p = QtGui.QPalette()
        #  p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 178, 164))
        p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 255, 255))
        self.colorWidget.setAutoFillBackground(True)
        self.colorWidget.setPalette(p)

        self.cap = cv2.VideoCapture(0)
        if self.cap is None or not self.cap.isOpened():
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText("Unable to open Camera!")
            msg.exec_()

        #  print(cv2.__version__[0])
        if int(cv2.__version__[0]) < 3:
            print("1280x720")
            self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
            self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)
        #  self.get_frame()
        self.run_timer()
        # call custom function "CalculateTax" when button is clicked
        #  self.calc_tax_button.clicked.connect(self.CalculateTax)

        # init variables
        #  self.noise_X = 1
        #  self.noise_Y = 1
        self.cX_prev = 10000
        self.cY_prev = 10000
        self.time_dwell_elapsed = 10000
        self.move_happened = 0

    # Custom function
    def GetColor(self):
        color = self.colorSpinBox.value()
        #  print(color)
        #  w = QtGui.QWidget()
        p = QtGui.QPalette()
        #  p.setColor(QtGui.QPalette.Window, Qt.black)
        #  p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(120, 178, 164))
        #  p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 178, 164))
        p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 255, 255))
        self.colorWidget.setAutoFillBackground(True)
        self.colorWidget.setPalette(p)
        #  p = QtGui.QPallete()
        #  p.setColor(
        #  p = w.palette()
        #  p.setColor(w.backgroundRole(), QtGui.Qt.red())
        #  w.setPallete(p)

        #  price = int(self.price_box.toPlainText())
        #  tax = (self.tax_rate.value())
        #  total_price = price + ((tax/100)*price)
        #  total_price_string = "The total price with tax is: " + str(total_price)
        #  self.results_window.setText(total_price_string)
        return color

    # run timer
    def run_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_frame)
        self.timer.start(0.1)

        self.timer_dwell = QTimer(self)
        self.timer_dwell.timeout.connect(self.check_move)
        #  self.timer_dwell.start(2000)
        self.timer_dwell.start(1600)

    # check mouse movement
    def check_move(self):
        checkbox_check = self.moveCursorCheckBox.checkState() and self.dwellClickCheckBox.checkState()
        if checkbox_check and (self.move_happened == 0):
            print("mouse click")
            pyautogui.click()  # click the mouse
        self.move_happened = 0


    # start webcam
    def get_frame(self):
        #  cap = cv2.VideoCapture(0)
        #  while True:
        _,frame = self.cap.read()
        #  cv2.imshow("Frame", frame)

        # range for OpenCV H is 0-180, range for Qt H is 0-360
        color = self.GetColor()/2
        #  color = int(color)
        #  print(color)
        # change to be suitable for QImage
        filtered_frame = self.follow_color(frame, color)
        #  filtered_frame = filtered_frame.astype(np.uint8)
        #  filtered_frame = filtered_frame.astype(np.uint8)
        #  image = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
        #  image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #  print(type(filtered_frame))
        #  print(filtered_frame.shape)
        #  print(filtered_frame)
        image = cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2RGB)
        #  image = cv2.cvtColor(filtered_frame, cv2.COLOR_HSV2RGB)
        #  if image is not None:
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        self.display_image(qimage)

    # display image
    def display_image(self, image):
        self.imageFrame.setPixmap(QtGui.QPixmap.fromImage(image))
        self.imageFrame.setScaledContents(True)
        #  self.imageFrame.show()

    # follow specific color
    def follow_color(self, frame, color):
        # convert frame from BGR (RGB) format to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        min_S = self.minS_SpinBox.value()
        min_V = self.minV_SpinBox.value()

        # Color mask
        #  low_green  = np.array([25, 52, 72])
        #  high_green = np.array([102, 255, 255])
        #  low_green  = np.array([color-10, 100, 72])
        #  high_green = np.array([color+10, 255, 255])
        #  print(min_S, min_V)
        low_green  = np.array([color-10, min_S, min_V])
        high_green = np.array([color+10, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)

        # convert image to binary image
        ret,thresh = cv2.threshold(green_mask,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        #  print(len(contours))
        #find the biggest area
        if(len(contours) > 0):
            max_contour = max(contours, key = cv2.contourArea)
            #  print(max_contour)

            # calculate moments of binary image
            #  M = cv2.moments(thresh)
            M = cv2.moments(max_contour)
            #  print(M["m00"])

            #  print(type(M))
            #  print(len(M))
            #  print(M)

            # calculate x,y coordinate of center
            #  if(M["m00"] != 0):
            # filter small objects
            if(M["m00"] > 500):
                #  print(M["m00"])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #  print(cX, cY)
                #  print(green[cY,cX])

                # move cursor if checkbox is checked
                move = 0
                if self.moveCursorCheckBox.checkState():
                    move = 1


                filter_move = self.filterSpinBox.value()
                speed       = self.speedSpinBox.value()
                # move cursor
                self.move_cursor(move, cX, cY, filter_move, speed)
            else:
                # false move
                self.move_happened = 1

        return green_mask

    # move cursor
    def move_cursor(self, move, cX, cY, filter_move, speed):
        noise_X = filter_move
        noise_Y = filter_move

        delta_X = cX - self.cX_prev
        delta_Y = cY - self.cY_prev
        move_X = None
        move_Y = None

        #  print(delta_X)
        if (delta_X > noise_X and self.cX_prev != 10000):
            #  pyautogui.moveRel(-move_X, None)
            #  move_X = -delta_X*4
            #  move_X = (-delta_X*2) if delta_X < 5 else -delta_X*4
            self.move_happened = 1
            move_X = -delta_X*speed
            #  pyautogui.moveRel(move_X, None)
            #  print("move_left: ", move_X)
            #  pass
        elif (delta_X < -noise_X):
            #  pyautogui.moveRel(move_X, None)
            #  move_X = -delta_X*4
            #  move_X = (-delta_X*2) if delta_X < 5 else -delta_X*4
            self.move_happened = 1
            move_X = -delta_X*speed
            #  pyautogui.moveRel(move_X, None)
            #  print("move_right: ", move_X)

        # Y-axis
        #  print(delta_Y)
        if (delta_Y > noise_Y and self.cY_prev != 10000):
            #  #  pyautogui.moveRel(-move_X, None)
            self.move_happened = 1
            move_Y = delta_Y*speed
            #  pyautogui.moveRel(None, move_Y)
            #  print("move_down: ", move_Y)
            #  #  pass
        elif (delta_Y < -noise_Y):
            #  #  pyautogui.moveRel(move_X, None)
            self.move_happened = 1
            move_Y = delta_Y*speed
            #  pyautogui.moveRel(None, move_Y)
            #  print("move_up: ", move_Y)

        if (move == 1) :
            pyautogui.moveRel(move_X, None)
            pyautogui.moveRel(None, move_Y)

        #  object_detected = 1
        self.cX_prev = cX
        self.cY_prev = cY

        return move_X, move_Y

# run app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
