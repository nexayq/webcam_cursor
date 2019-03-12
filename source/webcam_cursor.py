#!/usr/bin/env python2

#  https://www.pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/

from __future__ import print_function, division

import sys
import os

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QSettings

import cv2
import numpy as np
import pyautogui

# aruco
from cv2 import aruco
NK_ARUCO_ID = 43

# apriltag - comment to reduce binary size
#  import apriltag

# temp for calculating FIR coefficients
from scipy import signal

# Constants
NK_DWELL_MOVE_THRESH = 10
NK_VERSION = '2.3'


# disable closing of app when upper left corner is reached
pyautogui.FAILSAFE = False
# improve speed drastically
pyautogui.PAUSE = 0


# pyinstaller workaround
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Enter GUI filename
qtCreatorFile = resource_path("main.ui")

# Pictures
aruco_pic = resource_path("aruco_43.png")

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

        # load GUI settings from config file
        self.load_gui()

        self.cap = cv2.VideoCapture(0)
        if self.cap is None or not self.cap.isOpened():
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText("Unable to open Camera!")
            msg.exec_()

        #  print(cv2.__version__[0])
        if int(cv2.__version__[0]) < 3:
            pass
            #  print("1280x720")
            #  self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
            #  self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)
        #  self.get_frame()
        self.run_timer()
        # call custom function "CalculateTax" when button is clicked
        #  self.calc_tax_button.clicked.connect(self.CalculateTax)

        #  self.label_2.setGeometry(10, 10, 400, 100)
        self.labelArUco.setScaledContents(True)
        #  self.label_2.setPixmap(QtGui.QPixmap.scaled(70, 50, Qt.KeepAspectRatio))
        self.labelArUco.setPixmap(QtGui.QPixmap(aruco_pic))
        self.labelArUco.show()

        # init variables
        #  self.noise_X = 1
        #  self.noise_Y = 1
        self.cX_prev = 0
        self.cY_prev = 0
        self.time_dwell_elapsed = 10000
        self.move_detected = 0
        #  self.move_array_X = np.zeros(4)
        #  self.i = 0
        self.state_X = 0
        self.state_Y = 0
        self.first_data = 0

        # filter cursor array inputs - max size
        self.filter_cursor_X = np.zeros(100)
        self.filter_cursor_Y = np.zeros(100)

        self.fine_control_X = np.zeros(2)
        self.fine_control_Y = np.zeros(2)
        #  self.fine_control_X = np.zeros(4)
        #  self.fine_control_Y = np.zeros(4)

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
        self.timer_dwell.start(1800)

    # check mouse movement
    def check_move(self):
        checkbox_check = self.moveCursorCheckBox.checkState() and self.dwellClickCheckBox.checkState()
        if checkbox_check and (self.move_detected == 0):
            #  print("mouse click")
            pyautogui.click()  # click the mouse
            #  self.timer_dwell.start(1600)
        self.move_detected = 0

    # start webcam
    def get_frame(self):
        #  cap = cv2.VideoCapture(0)
        #  while True:
        _,frame = self.cap.read()
        #  cv2.imshow("Frame", frame)

        # get user selected algorithm
        algorithm = self.algorithmComboBox.currentText()
        #  index     = self.algorithmComboBox.currentIndex()
        #  print(index)
        #  print("Combo box: " + algorithm)

        # change to be suitable for QImage
        #  filtered_frame = self.follow_color(frame, color)
        #  filtered_frame = frame
        #  filtered_frame = filtered_frame.astype(np.uint8)
        #  filtered_frame = filtered_frame.astype(np.uint8)
        #  image = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
        #  image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #  print(type(filtered_frame))
        #  print(filtered_frame.shape)
        #  print(filtered_frame)
        #  image = cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2RGB)
        #  gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if(algorithm == "ArUco"):
            aruco_frame = self.detect_aruco(frame)
            #  aruco_frame = self.detect_apriltag(frame)
            image = cv2.cvtColor(aruco_frame, cv2.COLOR_BGR2RGB)
        elif(algorithm == "Color"):
            # range for OpenCV H is 0-180, range for Qt H is 0-360
            color = self.GetColor()/2
            #  color = int(color)
            #  print(color)
            filtered_frame = self.follow_color(frame, color)
            image = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #  filtered_frame = self.detect_object(gray_image)
        #  image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
        #  image = cv2.cvtColor(filtered_frame, cv2.COLOR_GRAY2RGB)
        #  image = filtered_frame
        #  image = cv2.cvtColor(filtered_frame, cv2.COLOR_HSV2RGB)
    #  if image is not None:
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        self.display_image(qimage)


    # display image
    def display_image(self, image):
        self.imageFrame.setPixmap(QtGui.QPixmap.fromImage(image))
        self.imageFrame.setScaledContents(True)
        #  self.imageFrame.show()


    # detect aruco
    def detect_aruco(self, frame):
        # dictionary - 4x4 aruco images
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        #  aruco_dict = aruco.generateCustomDictionary(43,4)
        #  print(aruco_dict)

        # get gray picture
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        parameters =  aruco.DetectorParameters_create()

        # get aruco frames
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        #  print(ids)

        # append aruco detected markers on color frame
        #  frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        # get (x,y) of top left aruco corner
        if ids is not None:
            # get number of matched IDs
            count_matches = 0
            for i in range(len(ids)):
                if ids[i][0] == NK_ARUCO_ID:
                    count_matches = count_matches + 1
                    match_idx = i

            # move cursor only if exactly one valid ArUco symbol is detected
            if count_matches == 1:

                c = corners[match_idx][0]
                #  print(c)
                # detect one point only
                #  x = c[0][0]
                #  y = c[0][1]
                x = c[:, 0].mean()
                y = c[:, 1].mean()

                # draw center point
                draw_x1 = int(round(x))-5
                draw_y1 = int(round(y))-5
                draw_x2 = int(round(x))+5
                draw_y2 = int(round(y))+5
                frame_markers = cv2.rectangle(frame_markers,(draw_x1,draw_y1),(draw_x2,draw_y2),(0,255,0),3)
                #  frame_markers = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
                #  frame_markers = cv2.rectangle(median,(x1,y1),(x2,y2),(0,255,0),3)
                #  print("c[" + str(i) + "] = " + str(c[i]))
                #  print("x = " + str(x))
                #  print("y = " + str(y))
                #  print("")

                # move cursor if checkbox is checked
                move = 0
                if self.moveCursorCheckBox.checkState():
                    move = 1
                # move cursor
                self.move_cursor(move, x, y)

        return frame_markers

    # detect apriltag
    # uncomment "import apriltag" in order to use this method
    def detect_apriltag(self, frame):

        # get gray picture
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detector = apriltag.Detector()
        #  result = detector.detect(median)
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
            frame_markers = cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)

            # move cursor if checkbox is checked
            move = 0
            if self.moveCursorCheckBox.checkState():
                move = 1
            # move cursor
            self.move_cursor(move, cx, cy)
        else:
            frame_markers = frame

        return frame_markers


    # detect object
    def detect_object(self, gray_image):
        # by default return original image
        detect_image = gray_image

        #  mod_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        mod_image = gray_image
        #  thresh = cv2.threshold(mod_image, 60, 255, cv2.THRESH_BINARY)[1]
        #  edges = cv2.Canny(gray_image, 60, 150, apertureSize = 3)
        #  lines = cv2.HoughLines(edges,1,np.pi/180,200)
        #  cv2.imshow('hough',

        # convert image to binary image
        ret,thresh = cv2.threshold(mod_image,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        for cntur in contours:
            M = cv2.moments(cntur)

            # filter small objects and large objects
            if((M["m00"] > 2) and (M["m00"]<200000)):

                # detect objects
                # 0.01 - 0.05
                approx = cv2.approxPolyDP(cntur, 0.09*cv2.arcLength(cntur,True),True)

                # rectangle
                if(len(approx)) == 4:
                    print("Rectangle detected!")
                    print(M["m00"])

                    # w - width of the contour
                    # h - height of the contour
                    # x, y - contour location
                    (x, y, w, h) = cv2.boundingRect(approx)
                    cv2.drawContours(mod_image,[cntur],0,255,-1)
                    detect_image = mod_image


        return detect_image


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
            area = cv2.contourArea(max_contour)
            #  print(area)

            #  print(type(M))
            #  print(len(M))
            #  print(M)

            # calculate x,y coordinate of center
            #  if(M["m00"] != 0):
            # filter small objects
            #  if(area > 80):
            if(M["m00"] > 300):
                #  print(M["m00"])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #  print(cX, cY)
                #  print(green[cY,cX])

                # move cursor if checkbox is checked
                move = 0
                if self.moveCursorCheckBox.checkState():
                    move = 1


                # move cursor
                self.move_cursor(move, cX, cY)
            else:
                pass
                # false move
                #  self.move_detected = 1

        return green_mask


    # move cursor
    def move_cursor(self, move, cX, cY):
        filter_move = self.filterSpinBox.value()
        speed_X = self.speedSpinBox_X.value()
        speed_Y = self.speedSpinBox_Y.value()
        noise_X = filter_move
        noise_Y = filter_move
        #  noise_Y = (filter_move-1) if (filter_move>0) else 0
        #  noise_X = 0
        #  noise_Y = 0

        delta_X = cX - self.cX_prev
        delta_Y = cY - self.cY_prev

        self.cX_prev = cX
        self.cY_prev = cY

        #  move_X = None
        #  move_Y = None
        move_X = 0
        move_Y = 0

        # there is no delta for first input data
        if(self.first_data == 0):
            self.first_data = 1
            return move_X, move_Y

        #  print(delta_X)

        #  print(delta_X)
        if (delta_X > noise_X):
            #  pyautogui.moveRel(-move_X, None)
            #  move_X = -delta_X*4
            #  move_X = (-delta_X*2) if delta_X < 5 else -delta_X*4
            #  self.move_detected = 1
            #  move_X = -delta_X*speed
            move_X = -(delta_X-noise_X)
            #  pyautogui.moveRel(move_X, None)
            #  print("move_left: ", 1)
            #  pass
        elif (delta_X < -noise_X):
            #  pyautogui.moveRel(move_X, None)
            #  move_X = -delta_X*4
            #  move_X = (-delta_X*2) if delta_X < 5 else -delta_X*4
            #  self.move_detected = 1
            #  move_X = -delta_X*speed
            move_X = -(delta_X-noise_X)
            #  pyautogui.moveRel(move_X, None)
            #  print("move_right: ", 1)

        # Y-axis
        #  print(delta_Y)
        #  print
        if (delta_Y > noise_Y):
            #  #  pyautogui.moveRel(-move_X, None)
            #  self.move_detected = 1
            #  move_Y = delta_Y*speed
            move_Y = delta_Y-noise_Y
            #  pyautogui.moveRel(None, move_Y)
            #  print("move_down: ", move_Y)
            #  #  pass
        elif (delta_Y < -noise_Y):
            #  #  pyautogui.moveRel(move_X, None)
            #  self.move_detected = 1
            #  move_Y = delta_Y*speed
            move_Y = delta_Y-noise_Y
            #  pyautogui.moveRel(None, move_Y)
            #  print("move_up: ", move_Y)

        #  move_array_X = np.zeros((4,1))
        #  self.move_array_X = np.zeros((4,1))
        #  print(self.move_array_X.shape)
        #  self.move_array_X[1:] = self.move_array_X[0:-1]
        #  self.move_array_X[0] = move_X
        #  print(self.move_array_X.shape)
        #  final_move_X = int(round(sum(self.move_array_X)))
        #  self.move_array_X[self.i] = move_X
        #  self.i = (self.i + 1)%4

        if (move == 1 ) :
            #  final_move_X = int(round(sum(self.move_array_X)/4))
            #  pyautogui.moveRel(move_X, None)
            #  pyautogui.moveRel(None, move_Y)

            # debug to file
            #  f_move_X = open( 'log/move_X.txt', 'a' )
            #  f_move_X.write( 'move_X = ' + repr(int(move_X/speed)) + '\n' )

            #  f_move_Y = open( 'log/move_Y.txt', 'a' )
            #  f_move_Y.write( 'move_Y = ' + repr(int(move_Y/speed)) + '\n' )
            #  f_move_Y.close()


            #  print("move X:", int(move_X/speed))
            #  print("move Y:", move_Y)

            # filter X noise
            #  if(noise_X == 0):
                #  move_X_final = self.filter_fsm_X(move_X)
                #  pyautogui.moveRel(move_X_final*speed_X, None)
            #  else:
                #  pyautogui.moveRel(move_X*speed_X, None)
            #  pyautogui.moveRel(move_X*speed_X, None)

            move_X_final, move_x = self.digital_filter_cursor_X(move_X, speed_X)
            pyautogui.moveRel(int(round(move_X_final)), None)

            #  print(noise_Y)
            #  if(noise_Y == 0):
                #  #  self.filter_fsm(move_Y, speed)
                #  move_Y_final = self.filter_fsm_Y(move_Y)
                #  pyautogui.moveRel(None, move_Y_final*speed_Y)
            #  else:
                #  pyautogui.moveRel(None, move_Y*speed_Y)

            move_Y_final, move_y = self.digital_filter_cursor_Y(move_Y, speed_Y)
            pyautogui.moveRel(None, int(round(move_Y_final)))

            if move_x or move_y:
                self.move_detected = 1

        #  object_detected = 1

        return move_X, move_Y

    # FSM for filtering dihtering moves - Y
    def filter_fsm_Y(self, move):
        move_final = 0
        print(self.state_Y)

        # 0 self.state_Y
        if(self.state_Y == 0):
            if(abs(move) > 1):
                #  pyautogui.moveRel(None, move*speed)
                move_final = move
            elif(move == 1):
                self.state_Y = 1
            elif(move == -1):
                self.state_Y = -1

        # 0 1
        elif(self.state_Y == 1):
            if(move == -1):
                # 0 1 -1
                #  f_move_Y = open( 'log/move_Y.txt', 'a' )
                #  f_move_Y.write( 'filtered 0 1 -1' + '\n' )
                print( 'Y filtered 0 -1 1' )
                #  f_move_Y.close()
                #  self.state_Y = 255
                self.state_Y = 0
                pass
            else:
                #  pyautogui.moveRel(None, (1+move)*speed)
                move_final = 1 + move
                self.state_Y = 0

        # 0 -1
        elif(self.state_Y == -1):
            if(move == 1):
                # 0 -1 1
                #  f_move_Y = open( 'log/move_Y.txt', 'a' )
                #  f_move_Y.write( 'filtered 0 -1 1' + '\n' )
                print( 'Y filtered 0 -1 1' )
                #  self.state_Y = 255
                self.state_Y = 0
                #  f_move_Y.close()
                pass
            else:
                #  pyautogui.moveRel(None, (-1+move)*speed)
                move_final = -1 + move
                self.state_Y = 0

        # 0 -1/1 1/-1 X - filter next input
        elif(self.state_Y == 255):
            self.state_Y = 0

        #  print("FSM entered")
        #  print(self.state_Y)
        return move_final


    # FSM for filtering dihtering moves - X
    def filter_fsm_X(self, move):
        move_final = 0
        print(self.state_X)

        # 0 self.state_X
        if(self.state_X == 0):
            if(abs(move) > 1):
                #  pyautogui.moveRel(None, move*speed)
                move_final = move
            elif(move == 1):
                self.state_X = 1
            elif(move == -1):
                self.state_X = -1

        # 0 1
        elif(self.state_X == 1):
            if(move == -1):
                # 0 1 -1
                #  f_move_X = open( 'log/move_X.txt', 'a' )
                #  f_move_X.write( 'filtered 0 1 -1' + '\n' )
                print( 'X filtered 0 -1 1' )
                #  f_move_X.close()
                #  self.state_X = 255
                self.state_X = 0
                pass
            else:
                #  pyautogui.moveRel(None, (1+move)*speed)
                move_final = 1 + move
                self.state_X = 0

        # 0 -1
        elif(self.state_X == -1):
            if(move == 1):
                # 0 -1 1
                #  f_move_X = open( 'log/move_X.txt', 'a' )
                #  f_move_X.write( 'filtered 0 -1 1' + '\n' )
                print( 'X filtered 0 -1 1' )
                #  self.state_X = 255
                self.state_X = 0
                #  f_move_X.close()
                pass
            else:
                #  pyautogui.moveRel(None, (-1+move)*speed)
                move_final = -1 + move
                self.state_X = 0

        # 0 -1/1 1/-1 X - filter next input
        elif(self.state_X == 255):
            self.state_X = 0

        #  print("FSM entered")
        #  print(self.state_X)
        return move_final


    # Digital filter for cursor movement X
    def digital_filter_cursor_X(self, dx, speed):
        # filter coefficients
        #  c = np.array([0.25, 0.25, 0.25, 0.25])
        #  c = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        #  numtaps = 20
        numtaps = self.filterSpinBox_X.value()

        # no filter
        if(numtaps == 0):
            x_out = dx
        # FIR filter
        else:
            #  f = 0.2
            f = 0.1
            c = signal.firwin(numtaps, f)
            filter_size = len(c)

            # shift in first element
            self.filter_cursor_X = np.append([dx], self.filter_cursor_X)
            # delete last element
            #  self.filter_cursor_X = self.filter_cursor_X[:-1]

            # calculate output value
            x_out = 0
            for i in range(0, filter_size):
                x_out = x_out + self.filter_cursor_X[i] * c[i]
            #  print(x_out)
            #  print(abs(x_out)*1000)

        # scale for easier analysis
        x_out = x_out*1000

        # analyze
        #  if(abs(x_out) > 400):
            #  print("X: " + str(abs(x_out)))

        # shift in first element
        self.fine_control_X = np.append([abs(x_out)], self.fine_control_X)
        # delete last element
        self.fine_control_X = self.fine_control_X[:-1]
        sum_X = sum(self.fine_control_X)
        #  print("X: "+str(sum_X))

        # small movements

        #  print(np.size(self.fine_control_X))
        #  if(sum_X/np.size(self.fine_control_X) < 200):
        if(sum_X < 1500/5*2):
            x_out = x_out/2
            # use some OK default speed
            x_out = 15*x_out/1000
        elif(sum_X > 4000/5*2):
            #  y_out = 20*y_out/1000
            x_out = 2*speed*x_out/1000
        else:
            # speed scale
            x_out = speed*x_out/1000

        #  if(abs(x_out) > 1 and abs(x_out) < 5):
        #  if(abs(x_out) < 400):
            #  x_out = x_out/3.5
        #  elif(abs(x_out) > 1000):
            #  x_out = x_out*2.5
        # fine movement
        #  elif(abs(x_out) < 8):
            #  x_out = x_out/2.5
        # coarse movement speed up
        #  elif(abs(x_out) > 12):
        #  elif(abs(x_out) > 8):
            #  x_out = x_out*2.5

        # dwell click
        move = 0
        if(abs(x_out) > NK_DWELL_MOVE_THRESH):
            move = 1

        return x_out, move


    # Digital filter for cursor movement Y
    def digital_filter_cursor_Y(self, dy, speed):
        # filter coefficients
        #  c = np.array([0.25, 0.25, 0.25, 0.25])
        #  c = 2*np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        #  numtaps = 20
        numtaps = self.filterSpinBox_Y.value()

        # no filter
        if(numtaps == 0):
            y_out = dy
        # FIR filter
        else:
            #  f = 0.2
            f = 0.1
            c = signal.firwin(numtaps, f)
            #  print(c)
            filter_size = len(c)

            # shift in first element
            self.filter_cursor_Y = np.append([dy], self.filter_cursor_Y)
            # delete last element
            #  self.filter_cursor_Y = self.filter_cursor_Y[:-1]

            # calculate output value
            y_out = 0
            for i in range(0, filter_size):
                y_out = y_out + self.filter_cursor_Y[i] * c[i]
            #  print(y_out)
            #  print(abs(y_out)*1000)
            #  print()

        # scale for easier analysis
        y_out = y_out*1000

        # analyze
        #  if(abs(y_out) > 400):
            #  print("Y: "+str(abs(y_out)))

        # shift in first element
        self.fine_control_Y = np.append([abs(y_out)], self.fine_control_Y)
        # delete last element
        self.fine_control_Y = self.fine_control_Y[:-1]
        sum_Y = sum(self.fine_control_Y)
        #  print("Y: "+str(sum_Y))

        # small movements

        if(sum_Y < 1000/5*2):
            y_out = y_out/2
            # use some OK default speed
            y_out = 25*y_out/1000
        elif(sum_Y > 2000/5*2):
            #  y_out = 20*y_out/1000
            y_out = 2*speed*y_out/1000
        else:
            # speed scale
            y_out = speed*y_out/1000

        # small movements
        #  if(abs(y_out) > 1 and abs(y_out) < 6):
        #  if(abs(y_out) < 600):
            #  y_out = y_out/3.5
        #  elif(abs(y_out) > 1000):
            #  y_out = y_out*2.5
        # fine movement
        #  elif(abs(y_out) < 8):
            #  y_out = y_out/2.5
        # coarse movement speed up
        #  elif(abs(y_out) > 10):
            #  y_out = y_out*2.5


        # speed scale
        #  y_out = speed*y_out/1000

        # dwell click
        move = 0
        if(abs(y_out) > NK_DWELL_MOVE_THRESH):
            move = 1

        return y_out, move


    # save GUI state
    def save_gui(self):
        print("save_gui")
        # located at "~/.config/webcam_cursor/config.cfg"
        # directory and filename for config file
        config = QSettings('webcam_cursor', 'webcam_cursor')
        #  config.beginGroup("./config.cfg")
        config.setValue('number', 55)
        config.setValue('version', NK_VERSION)
        #  config.endGroup()

        # GUI settings
        config.setValue('algorithm', self.algorithmComboBox.currentIndex())
        #  print(self.algorithmComboBox.currentIndex())

        # color
        config.setValue('color_H', self.colorSpinBox.value())
        config.setValue('color_min_S', self.minS_SpinBox.value())
        config.setValue('color_min_V', self.minV_SpinBox.value())

        # cursor
        config.setValue('cursor_move',  self.moveCursorCheckBox.checkState())
        config.setValue('cursor_dwell',  self.dwellClickCheckBox.checkState())
        # speed
        config.setValue('cursor_speed_X', self.speedSpinBox_X.value())
        config.setValue('cursor_speed_Y', self.speedSpinBox_Y.value())
        # filter cursor
        config.setValue('filter_pixels', self.filterSpinBox.value())
        config.setValue('filter_X', self.filterSpinBox_X.value())
        config.setValue('filter_Y', self.filterSpinBox_Y.value())


    # when application closes save settings
    def closeEvent(self, event):
        #  print "closing PyQtTest"
        self.save_gui()
        # report_session()

    # load GUI state
    def load_gui(self):
        print("load_gui")
        # located at "~/.config/webcam_cursor/config.cfg"
        # directory and filename for config file
        config = QSettings('webcam_cursor', 'webcam_cursor')
        #  config.beginGroup("./config.cfg")
        version = config.value('version', type=str)
        number = config.value('number', type=int)
        #  print(version)
        #  config.endGroup()

        # check if config file exists
        if number != 55:
            print("NK: Using default GUI values")
            return -1

        # GUI settings
        self.algorithmComboBox.setCurrentIndex( config.value('algorithm', type=int) )

        # color
        self.colorSpinBox.setValue( config.value('color_H', type=int) )
        self.minS_SpinBox.setValue( config.value('color_min_S', type=int) )
        self.minV_SpinBox.setValue( config.value('color_min_V', type=int) )

        # cursor
        self.moveCursorCheckBox.setChecked( config.value('cursor_move', type=int) )
        self.dwellClickCheckBox.setChecked( config.value('cursor_dwell', type=int) )
        # speed
        self.speedSpinBox_X.setValue( config.value('cursor_speed_X', type=int) )
        self.speedSpinBox_Y.setValue( config.value('cursor_speed_Y', type=int) )
        # filter cursor
        self.filterSpinBox.setValue( config.value('filter_pixels', type=int) )
        self.filterSpinBox_X.setValue( config.value('filter_X', type=int) )
        self.filterSpinBox_Y.setValue( config.value('filter_Y', type=int) )


# run app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    #  window.save_gui()
    sys.exit(app.exec_())
