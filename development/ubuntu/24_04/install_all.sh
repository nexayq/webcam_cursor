#!/bin/bash

# stop script if exit occurs
set -e
# print commands
set -x

# Install git
sudo add-apt-repository universe
sudo apt-get update
sudo apt install git
sleep 1

# Go to repos directory
cd $HOME
mkdir -p repos/
cd repos/

# Clone repo
git clone https://github.com/nexayq/webcam_cursor
sleep 1

# Install all dependencies
cd webcam_cursor/development/ubuntu/24_04/
source ./install_dependencies_python3.sh

# Go to source directory
cd ../../source/
# python3 webcam_cursor_pyqt5.py
