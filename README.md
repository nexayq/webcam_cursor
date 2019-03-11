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

## Linux (tested on Ubuntu)
Download archive from Releases:  [webcam_cursor.tar.gz](https://github.com/nexayq/webcam_cursor/releases/download/webcam_cursor_v2.3/webcam_cursor.tar.gz)

Extract **webcam_cursor.tar.gz** archive to some directory

Execute **webcam_cursor.run** from file manager or terminal


## Windows
Download archive from Releases:  [webcam_cursor.exe](https://github.com/nexayq/webcam_cursor/releases/download/webcam_cursor_v2.3/webcam_cursor.zip)

Extract **webcam_cursor.zip** to some directory

Run **webcam_cursor** (webcam_cursor.vbs) from File Explorer

# Development

## Ubuntu - install dependencies for development
    $ cd development/ubuntu/
    $ ./install_dependencies.sh


## Run
    $ cd source/
    $ ./run.sh


# License

    GPL-2.0

[aruco_screenshot]:       https://github.com/nexayq/webcam_cursor/blob/master/data/screenshots/aruco_screenshot.png
[color_screenshot]:       https://github.com/nexayq/webcam_cursor/blob/master/data/screenshots/color_screenshot.png

[aruco_symbol]:           https://github.com/nexayq/webcam_cursor/blob/master/source/aruco_43.png
