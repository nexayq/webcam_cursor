#!/bin/bash

### NOT TESTED !!! ###

# stop script if exit occurs
set -e

# pyton3 pip
sudo apt install python3-pip

# OpenCV
sudo apt install python3-numpy
# sudo apt install python-opencv
# pip3 install opencv-python --user
sudo apt install python3-opencv

# PyQt
# sudo apt install python-qt4
# sudo apt install python3-pyqt4
sudo apt install python3-pyqt5
# Tk
sudo apt install python3-tk
sudo apt install python3-dev

# PyAutoGUI
# sudo apt install python-xlib
# pip3 install xlib --user
sudo apt install python3-xlib
# pip3 install pyautogui --user
pip3 install pyautogui==0.9.41 --user

# ArUco
sudo apt install libeigen3-dev
# pip2 install aruco --user
pip3 install opencv-contrib-python --user

# Filtering
sudo apt install python3-scipy

### NOT TESTED !!! ###
