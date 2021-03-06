#!/usr/bin/env python2

from __future__ import print_function, division
import cv2
import time

if __name__ == '__main__' :

    # Start default camera
    video = cv2.VideoCapture(0);
    video.set(cv2.CAP_PROP_FPS, 60)

while True:
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.

    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))


    # Number of frames to capture
    num_frames = 120;


    print("Capturing {0} frames".format(num_frames))

    # Start time
    start = time.time()

    # Grab a few frames
    for i in range(0, num_frames) :
        ret, frame = video.read()


    # End time
    end = time.time()

    # Time elapsed
    seconds = end - start
    print("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds;
    print("Estimated frames per second : {0}".format(fps))

    cv2.imshow("Web cam input", frame)
    key = cv2.waitKey(1)

    # Release video
    #  video.release()
