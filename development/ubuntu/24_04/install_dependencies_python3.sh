#!/bin/bash

### NOT TESTED !!! ###

# numpy==1.21.5
# opencv_python_headless==4.10.0.84
# PyAutoGUI==0.9.41
# # PyQt5==5.15.11
# # PyQt5_sip==12.15.0
# scipy==1.8.0


# stop script if exit occurs
set -e
# print commands
set -x

# pyton3 pip
sudo apt install python3-pip

# NumPy
# sudo apt install python3-numpy
pip3 install numpy==1.21.5

# OpenCV
# sudo apt install python-opencv
# pip3 install opencv-python --user
# sudo apt install python3-opencv
pip3 install opencv_python_headless==4.10.0.84


# PyQt
# sudo apt install python-qt4
# sudo apt install python3-pyqt4
sudo apt install python3-pyqt5
# Tk
# sudo apt install python3-tk
# sudo apt install python3-dev

# PyAutoGUI
# sudo apt install python-xlib
# pip3 install xlib --user
sudo apt install python3-xlib
# pip3 install pyautogui --user
# pip3 install pyautogui==0.9.41 --user
pip3 install PyAutoGUI==0.9.41


# ArUco - installed with OpenCV
# sudo apt install libeigen3-dev
# pip2 install aruco --user
# pip3 install opencv-contrib-python --user

# Filtering
# sudo apt install python3-scipy
pip3 install scipy==1.8.0

### NOT TESTED !!! ###
