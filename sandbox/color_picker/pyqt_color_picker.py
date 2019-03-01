#!/usr/bin/env python2

#  https://www.pythonforengineers.com/your-first-gui-app-with-python-and-pyqt/

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTimer

import cv2

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
        #  self.get_frame()
        self.run_timer()
        # call custom function "CalculateTax" when button is clicked
        #  self.calc_tax_button.clicked.connect(self.CalculateTax)

    # Custom function
    def GetColor(self):
        color = self.colorSpinBox.value()
        print(color)
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

    def run_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_frame)
        self.timer.start(2)


    # start webcam
    def get_frame(self):
        #  cap = cv2.VideoCapture(0)
        #  while True:
        _,frame = self.cap.read()
        #  cv2.imshow("Frame", frame)
        # change to be suitable for QImage
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)
        self.display_image(qimage)

    # display image
    def display_image(self, image):
        self.imageFrame.setPixmap(QtGui.QPixmap.fromImage(image))
        #  self.imageFrame.setScaledContents(True)
        #  self.imageFrame.show()

# run app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
