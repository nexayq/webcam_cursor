#!/bin/bash

# stop script when exit occurs
set -e

# OpenCV
sudo apt install python-numpy
sudo apt install python-opencv

# PyQt
sudo apt install python-qt4

# PyAutoGUI
sudo apt install python-pip
pip install pyautogui --user


# run application
../../color_picker/run.sh
