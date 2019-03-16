#!/bin/bash

cython --embed -o webcam_cursor.c webcam_cursor.py
gcc -Os -I /usr/include/python3.5m webcam_cursor.c -lpython3.5m -o webcam_cursor
