#!/bin/bash

# stop script if exit occurs
set -e

# OpenCV
sudo apt install python-numpy
sudo apt install python-opencv

# PyQt
sudo apt install python-qt4

# PyAutoGUI
sudo apt install python-pip
sudo apt install python-xlib
pip2 install pyautogui --user

# ArUco
sudo apt install libeigen3-dev
# pip2 install aruco --user
pip2 install opencv-contrib-python --user

# Filtering
sudo apt install python-scipy
