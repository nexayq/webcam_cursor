#!/bin/bash

ffmpeg -f video4linux2 -list_formats all -i /dev/video0
