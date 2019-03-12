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

# apriltag - comment to reduce binary size
#  import apriltag

# for calculating FIR coefficients
from scipy import signal

# Constants
NK_ARUCO_ID = 43
NK_DWELL_MOVE_THRESH = 10
NK_VERSION = '2.3'


# disable closing of app when upper left corner is reached
pyautogui.FAILSAFE = False
# improve speed drastically
pyautogui.PAUSE = 0


# pyinstaller workaround for file paths
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
        self.colorSpinBox.valueChanged.connect(self.get_color)
        color = self.colorSpinBox.value()

        # set init HSV color
        p = QtGui.QPalette()
        #  p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 178, 164))
        p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 255, 255))
        self.colorWidget.setAutoFillBackground(True)
        self.colorWidget.setPalette(p)

        # try to open camera if present on system
        self.cap = cv2.VideoCapture(0)
        if self.cap is None or not self.cap.isOpened():
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText("Unable to open Camera!")
            print("Unable to open Camera!")
            msg.exec_()

        # track what camera user wants to use
        self.cameraSelectComboBox.currentIndexChanged.connect(self.select_camera)

        # load GUI settings from config file
        self.load_gui()

        #  print(cv2.__version__[0])
        if int(cv2.__version__[0]) < 3:
            pass
            #  print("1280x720")
            #  self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
            #  self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)

        # run timers for capturing new frames and processing dwell time
        self.frame_timer()

        # show aruco picture from file in label
        self.labelArUco.setScaledContents(True)
        self.labelArUco.setPixmap(QtGui.QPixmap(aruco_pic))
        self.labelArUco.show()

        # init variables
        # cursor movement
        self.cX_prev = 0
        self.cY_prev = 0
        self.move_detected = 0
        # there is no delta_X/Y for first cursor movement
        self.first_data = 0

        # filter cursor array inputs - max size=100
        self.filter_cursor_X = np.zeros(100)
        self.filter_cursor_Y = np.zeros(100)

        # reduce movement speed for small cursor movements, analyze speed
        self.fine_control_X = np.zeros(2)
        self.fine_control_Y = np.zeros(2)
        #  self.fine_control_X = np.zeros(4)
        #  self.fine_control_Y = np.zeros(4)

        # connect "Dwell Click" checkbox checked and dwell timer reset
        self.dwellClickCheckBox.stateChanged.connect(self.reset_dwell_timer)


    # select camera
    def select_camera(self):
        camera = self.cameraSelectComboBox.currentText()
        self.cap = cv2.VideoCapture(int(camera))
        return self.cap


    # get color from spinbox and apply it to widget
    def get_color(self):
        color = self.colorSpinBox.value()
        #  print(color)
        p = QtGui.QPalette()
        #  p.setColor(QtGui.QPalette.Window, Qt.black)
        #  p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(120, 178, 164))
        #  p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 178, 164))
        p.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsv(color, 255, 255))
        self.colorWidget.setAutoFillBackground(True)
        self.colorWidget.setPalette(p)
        return color


    # run frame and dwell timer
    def frame_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_frame)
        self.timer.start(0.1)

        # dwell timer
        self.timer_dwell = QTimer(self)
        self.timer_dwell.timeout.connect(self.check_move)
        #  self.timer_dwell.start(2000)
        self.timer_dwell.start(1800)

    # reset dwell timer
    def reset_dwell_timer(self):
        self.timer_dwell.start(1800)


    # check for mouse movement and click if there is no movement
    def check_move(self):
        checkbox_check = self.moveCursorCheckBox.checkState() and self.dwellClickCheckBox.checkState()
        if checkbox_check and (self.move_detected == 0):
            #  print("mouse click")
            pyautogui.click()  # click the mouse
            #  self.timer_dwell.start(1600)
        self.move_detected = 0


    # main - capture frame and process them
    def get_frame(self):

        # if camera is unavailable return error
        if self.cap is None or not self.cap.isOpened():
            return -1

        # get frame from camera
        _,frame = self.cap.read()
        #  cv2.imshow("Frame", frame)

        # get user selected algorithm
        algorithm = self.algorithmComboBox.currentText()
        #  index     = self.algorithmComboBox.currentIndex()
        #  print(index)
        #  print("Combo box: " + algorithm)

        # depending on algorithm selected do different processings
        # track ArUco markers
        if(algorithm == "ArUco"):
            aruco_frame = self.detect_aruco(frame)
            #  aruco_frame = self.detect_apriltag(frame)
            image = cv2.cvtColor(aruco_frame, cv2.COLOR_BGR2RGB)
        # track color
        elif(algorithm == "Color"):
            # range for OpenCV H is 0-180, range for Qt H is 0-360
            color = self.get_color()/2
            #  color = int(color)
            #  print(color)
            filtered_frame = self.follow_color(frame, color)
            image = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
        # just show frame
        else:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # if image is not None:
        # show frame from webcam in big Qlabel
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        self.display_image(qimage)


    # show frame from webcam
    def display_image(self, image):
        self.imageFrame.setPixmap(QtGui.QPixmap.fromImage(image))
        self.imageFrame.setScaledContents(True)
        #  self.imageFrame.show()


    # detect aruco markers
    def detect_aruco(self, frame):
        # dictionary - 4x4 aruco images
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
        #  aruco_dict = aruco.generateCustomDictionary(43,4)
        #  print(aruco_dict)

        # get gray picture
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # get aruco frames
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        #  print(ids)

        # put aruco detected markers on top of colored frame (webcam input)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

        # get (x,y) center coordinates of aruco marker
        # if only one marker is present
        if ids is not None:
            # get number of matched IDs
            count_matches = 0

            # get number of aruco tags
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
                #  print("c[" + str(i) + "] = " + str(c[i]))
                #  print("x = " + str(x))
                #  print("y = " + str(y))
                #  print("")

                # move cursor if checkbox is checked
                move = 0
                if self.moveCursorCheckBox.checkState():
                    move = 1

                # move cursor if needed
                self.move_cursor(move, x, y)

        return frame_markers


    # detect apriltag - keep this function if you switch to apriltags
    # uncomment "import apriltag" in order to use this method
    def detect_apriltag(self, frame):

        # get gray picture
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # get apriltags if present in frame (webcam input)
        detector = apriltag.Detector()
        result = detector.detect(gray)

        # get center of apriltag
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

            # move cursor if needed
            self.move_cursor(move, cx, cy)
        # when tag is not present return regular frame (webcam input)
        else:
            frame_markers = frame

        return frame_markers


    # detect object - keep function if you want to track specific object (rectangular, circle)
    def detect_object(self, gray_image):
        # by default return original image
        detect_image = gray_image

        #  mod_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

        mod_image = gray_image
        #  thresh = cv2.threshold(mod_image, 60, 255, cv2.THRESH_BINARY)[1]
        #  edges = cv2.Canny(gray_image, 60, 150, apertureSize = 3)
        #  lines = cv2.HoughLines(edges,1,np.pi/180,200)

        # convert image to binary image
        ret,thresh = cv2.threshold(mod_image,127,255,0)
        contours,hierarchy = cv2.findContours(thresh, 1, 2)

        # detect specific contours
        for cntur in contours:
            M = cv2.moments(cntur)

            # filter small objects and large objects
            if((M["m00"] > 2) and (M["m00"]<200000)):

                # detect objects
                # 0.01 - 0.05
                approx = cv2.approxPolyDP(cntur, 0.09*cv2.arcLength(cntur,True),True)

                # rectangle - not working so great, shows various objects
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

        # get user defined Saturation(S) and Value(V) for color
        min_S = self.minS_SpinBox.value()
        min_V = self.minV_SpinBox.value()

        # Color mask - for user defined color
        #  low_green  = np.array([25, 52, 72])
        #  high_green = np.array([102, 255, 255])
        #  low_green  = np.array([color-10, 100, 72])
        #  high_green = np.array([color+10, 255, 255])
        #  print(min_S, min_V)
        low_color  = np.array([color-10, min_S, min_V])
        high_color = np.array([color+10, 255, 255])
        color_mask = cv2.inRange(hsv_frame, low_color, high_color)
        colored_image = cv2.bitwise_and(frame, frame, mask=color_mask)

        # convert image to binary image based on user defined color
        ret,thresh = cv2.threshold(color_mask,127,255,0)

        # find contours from black and white image
        contours,hierarchy = cv2.findContours(thresh, 1, 2)
        #  print(len(contours))
        # find biggest contour
        if(len(contours) > 0):
            # find biggest contour
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

            # calculate x,y coordinate of contour center
            #  if(M["m00"] != 0):
            #  if(area > 80):
            # filter small objects
            if(M["m00"] > 300):
                #  print(M["m00"])
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #  print(cX, cY)
                #  print(colored_image[cY,cX])

                # move cursor if checkbox is checked
                move = 0
                if self.moveCursorCheckBox.checkState():
                    move = 1

                # move cursor if needed
                self.move_cursor(move, cX, cY)
            else:
                #  pass
                # false move
                self.move_detected = 1

        return color_mask


    # move cursor
    def move_cursor(self, move, cX, cY):
        # get values from GUI
        filter_move = self.filterSpinBox.value()
        speed_X = self.speedSpinBox_X.value()
        speed_Y = self.speedSpinBox_Y.value()

        noise_X = filter_move
        noise_Y = filter_move
        #  noise_Y = (filter_move-1) if (filter_move>0) else 0
        #  noise_X = 0
        #  noise_Y = 0

        # calculate delta_X and delta_Y
        delta_X = cX - self.cX_prev
        delta_Y = cY - self.cY_prev

        # store coordinates for next iteration
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

        # X-axis
        #  print(delta_X)
        # if X movement is greater than user defined noise (Filter Pix)
        if (abs(delta_X) > abs(noise_X)):
            move_X = -(delta_X-noise_X)

        # Y-axis
        #  print(delta_Y)
        #  print()
        # if Y movement is greater than user defined noise (Filter Pix)
        if (abs(delta_Y) > abs(noise_Y)):
            move_Y = delta_Y-noise_Y

        # if "Move Cursor" checkbox is checked
        if (move == 1 ) :
            # move cursor on X axis
            move_X_final, move_x = self.digital_filter_cursor_X(move_X, speed_X)
            pyautogui.moveRel(int(round(move_X_final)), None)

            # move cursor on Y axis
            move_Y_final, move_y = self.digital_filter_cursor_Y(move_Y, speed_Y)
            pyautogui.moveRel(None, int(round(move_Y_final)))

            # move detection for dwell click
            if move_x or move_y:
                self.move_detected = 1

            ### CURSOR MOVEMENT ANALYSIS
            # debug to file - slow and doesn't show all iterations
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

            #  print(noise_Y)
            #  if(noise_Y == 0):
                #  #  self.filter_fsm(move_Y, speed)
                #  move_Y_final = self.filter_fsm_Y(move_Y)
                #  pyautogui.moveRel(None, move_Y_final*speed_Y)
            #  else:
                #  pyautogui.moveRel(None, move_Y*speed_Y)

        #  object_detected = 1

        return move_X, move_Y


    # digital filter for cursor movement X
    def digital_filter_cursor_X(self, dx, speed):
        # filter coefficients
        #  c = np.array([0.25, 0.25, 0.25, 0.25])
        #  c = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        #  numtaps = 20
        # get number of taps from GUI (Filter X)
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
            self.filter_cursor_X = self.filter_cursor_X[:-1]

            # calculate output value - filter MAC (multiply-accumulate)
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

        #  print(np.size(self.fine_control_X))
        #  if(sum_X/np.size(self.fine_control_X) < 200):
        # small cursor movements
        if(sum_X < 1500/5*2):
            x_out = x_out/2
            # use some OK default speed
            x_out = 15*x_out/1000
        # fast cursor movements
        elif(sum_X > 4000/5*2):
            x_out = 2*speed*x_out/1000
        # normal speed cursor movements
        else:
            # speed scale
            x_out = speed*x_out/1000

        # check if movement is greater than dwell threshold
        move = 0
        if(abs(x_out) > NK_DWELL_MOVE_THRESH):
            move = 1

        return x_out, move


    # digital filter for cursor movement Y
    def digital_filter_cursor_Y(self, dy, speed):
        # filter coefficients
        #  c = np.array([0.25, 0.25, 0.25, 0.25])
        #  c = 2*np.array([0.2, 0.2, 0.2, 0.2, 0.2])
        #  numtaps = 20
        # get number of taps from GUI (Filter Y)
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
            self.filter_cursor_Y = self.filter_cursor_Y[:-1]

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
        # fast cursor movements
        elif(sum_Y > 2000/5*2):
            y_out = 2*speed*y_out/1000
        # normal speed cursor movements
        else:
            # speed scale
            y_out = speed*y_out/1000

        # check if movement is greater than dwell threshold
        move = 0
        if(abs(y_out) > NK_DWELL_MOVE_THRESH):
            move = 1

        return y_out, move


    # save GUI state
    def save_gui(self):
        print("save_gui")

        # linux   - located at "~/.config/webcam_cursor/config.cfg"
        # windows - located at "regedit -> HKEY_CURRENT_USER\Software\webcam_cursor\webcam_cursor"
        # windows - located in binary file "%USERPROFILE%\NTUSER.DAT"

        # directory and filename for config file
        config = QSettings('webcam_cursor', 'webcam_cursor')
        #  config.beginGroup("./config.cfg")
        # variable to check if config file exists
        config.setValue('number', 55)
        # app version
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

        # camera
        config.setValue('camera', self.cameraSelectComboBox.currentIndex())


    # when application closes save settings
    def closeEvent(self, event):
        #  print "closing PyQtTest"
        self.save_gui()
        # report_session()


    # load GUI state
    def load_gui(self):
        print("load_gui")

        # linux   - located at "~/.config/webcam_cursor/config.cfg"
        # windows - located at "regedit -> HKEY_CURRENT_USER\Software\webcam_cursor\webcam_cursor"
        # windows - located in binary file "%USERPROFILE%\NTUSER.DAT"

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

        # camera
        self.cameraSelectComboBox.setCurrentIndex( config.value('camera', type=int) )


# run main GUI app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    #  window.save_gui()
    sys.exit(app.exec_())
