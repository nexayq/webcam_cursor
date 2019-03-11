#!/bin/bash

# stop script if exit occurs
set -e

# pyton3 pip
sudo apt install python3-pip

# OpenCV
sudo apt install python3-numpy
# sudo apt install python-opencv
pip3 install opencv-python --user

# PyQt
# sudo apt install python-qt4
sudo apt install python3-pyqt4

# PyAutoGUI
# sudo apt install python-xlib
pip3 install xlib --user
pip3 install pyautogui --user

# ArUco
sudo apt install libeigen3-dev
# pip2 install aruco --user
pip3 install opencv-contrib-python --user

# Filtering
sudo apt install python3-scipy
