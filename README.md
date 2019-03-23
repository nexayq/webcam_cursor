# Webcam Cursor
Move mouse cursor by moving your head - place ArUco tag somewhere (glasses, forehead, ...)

Mouse cursor is following ArUco symbol 43(4x4) or specific color from your webcam.

Mainly intended for people with disabilities to use the computer (Multiple sclerosis, ALS, ...)

Made with love for my neighbour Bilja


# Demo Video
Demo Video that shows control of mouse cursor with head movement: [Video](https://www.youtube.com/watch?v=dbJvwXaWFdY)


# Screenshots
<p align="center">
    ArUco symbol 43 tracking
</p>

![Screenshot - Aruco symbol 43 tracking][aruco_screenshot]

<p align="center">
    Custom Color tracking
</p>

![Screenshot - Custom Color tracking][color_screenshot]


# ArUco algorithm
In order to use ArUco algorithm you need to download and print ArUco 4x4 symbol 43 (looks like "IF")

PDF file with ArUco 4x4 symbol 43 various sizes can be downloaded and printed from [PDF_Aruco_43](https://github.com/nexayq/webcam_cursor/blob/master/data/aruco_markers/aruco_43_4x4/aruco_all_dimensions.pdf)

You can get custom sizes from link: [ArUco Symbols](http://chev.me/arucogen/)

Specify Dictionary: 4x4

Specify Marker ID: 43

Use wanted marker size

![Screenshot - Aruco 43 4x4][aruco_symbol]

# Color algorithm
Specify color you want to track in HSV domain.

H value specifies color (blue, yellow, green, ...)

H range is 0-360


# Install

## Linux
Download archive from Releases:  [webcam_cursor.tar.gz](https://github.com/nexayq/webcam_cursor/releases/download/webcam_cursor_v2.5/webcam_cursor.tar.gz)

Extract **webcam_cursor.tar.gz** archive to some directory

Execute **webcam_cursor.run** from file manager or terminal

Tested on:
**Ubuntu 16.04**, **Linux Mint 18.3**, **Ubuntu 18.04**, **MX Linux 18.1**, **Antergos 19.2**


## Windows
Download archive from Releases:  [webcam_cursor.zip](https://github.com/nexayq/webcam_cursor/releases/download/webcam_cursor_v2.5/webcam_cursor.zip)

Extract **webcam_cursor.zip** to some directory

Run **webcam_cursor** (webcam_cursor.vbs) from File Explorer

Tested on:
**Windows 7**, **Windows 10**

# Development

## Ubuntu - install dependencies for development
    $ cd development/ubuntu/

    # for python2
    $ ./install_dependencies_python2.sh

    # or for python3
    $ ./install_dependencies_python3.sh


## Run
    $ cd source/

    # for python2
    $ python2 webcam_cursor.py

    # for python3
    $ python3 webcam_cursor.py


# Web Camera

Standard built in laptop cameras can be used with this application.

If built in camera quality is exceptionally low (10 FPS at 640x480) then cursor movement will be choppy.

In that case it is better to use some cheap USB camera (25€-40€).

My recommendation is [**Logitech C270**](https://www.amazon.com/Logitech-Widescreen-designed-Calling-Recording/dp/B004FHO5Y6) - it works perfectly out of the box on Linux and Windows with this application.

Easiest way to test if camera performance is fine - just run **Webcam Cursor** and see if cursor movement is continuous.

If cursor movement is not continuous read text bellow.

Camera FPS (Frames Per Second) performance is the most important spec for **Webcam Cursor**.

Webcam Cursor uses 640x480 resolution so it is important to know camera FPS at 640x480.

Camera used in [video demo](https://www.youtube.com/watch?v=dbJvwXaWFdY&t=5m25s) (0.92 MegaPixels) generates 30 FPS at 640x480 - built in webcam in laptop Toshiba Satellite L50-B (Toshiba Web Camera - HD)

App performance was good even with 15 FPS (640x480) during tests but it is recommended to have higher FPS.

You can check camera quality and read reviews online:
    https://webcamtests.com/

To test FPS online (for some resolution which is probably different than 640x480) you can go to:
    https://www.onlinemictest.com/webcam-test/

On Linux you can use **v4l2-utils** to test your camera quality:

    $ sudo apt-get install v4l-utils    # for apt package manager (Debian/Ubuntu/Mint)
    $ v4l2-ctl --list-formats-ext       # show FPS for camera supported resolutions
        ...
        Size: Discrete 640x480
            Interval: Discrete 0.033s (30.000 fps)
        ...

You can also use application **guvcview** to detect your FPS at custom resolution on Linux:

    $ sudo apt-get install guvcview                         # for apt package manager (Debian/Ubuntu/Mint)
    $ guvcview --device=/dev/video0 --resolution=640x480    # use /dev/video1 for second camera


Some cameras increase exposure and reduce FPS in low light conditions (dark). Disabling such features can increase your FPS in low light conditions.

On Linux you can use **guvcview** and uncheck **Exposure, Auto Priority**

On Windows you can use camera software and turn off such features.

For example uncheck **DirectLight** feature for some of the Logitech cameras (no need for this on C270) - [Turn off DirectLight feature](https://www.youtube.com/watch?v=v5H7x21apyE)


# License

GPL-2.0


[aruco_screenshot]:       https://github.com/nexayq/webcam_cursor/blob/master/data/screenshots/aruco_screenshot.png
[color_screenshot]:       https://github.com/nexayq/webcam_cursor/blob/master/data/screenshots/color_screenshot.png

[aruco_symbol]:           https://github.com/nexayq/webcam_cursor/blob/master/source/aruco_43.png
