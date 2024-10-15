#!/bin/bash

# Ubuntu 20.04 - Python 3.8.10
# Ubuntu 22.04 - Python 3.10.12
# Ubuntu 24.04 - Python 3.12.3

# install venv
sudo apt install python3-venv

# install python3-pyqt5 - must!
sudo apt install python3-pyqt5

# Change directory to source dir
cd ../../../source/

python3 -m venv .venv
source .venv/bin/activate

# python3 -m pip install --upgrade pip==24.2
python3 -m pip install pip==24.2
pip3 list

# PyQt - python3-pyqt5 is a must!
pip3 install PyQt5==5.15.11

# Xlib
pip3 install xlib==0.21

# NumPy
# pip3 install numpy==1.24.4 # Ubuntu 20.04 - Python 3.8.10
pip3 install numpy==2.1.2

# OpenCV
pip3 install opencv_python_headless==4.10.0.84

# PyAutoGUI
pip3 install PyAutoGUI==0.9.41

# Filtering
# pip3 install scipy==1.10.1 # Ubuntu 20.04 - Python 3.8.10
pip3 install scipy==1.14.1
