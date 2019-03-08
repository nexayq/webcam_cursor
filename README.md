# Webcam Cursor
Move mouse cursor by following ArUco symbol 43(4x4) or specific color from your webcam

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

Pdf file with ArUco 4x4 symbol 43 various sizes can be downloaded and printed from [pdf_Aruco_43](https://github.com/nexayq/webcam_cursor/blob/master/data/aruco_markers/aruco_43_4x4/aruco_all_dimensions.pdf)

You can get custom sizes from link: [ArUco 43 (4x4)](http://chev.me/arucogen/)

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
Download binary from Releases:  [webcam_cursor_linux.run](https://github.com/nexayq/webcam_cursor/releases/download/webcam_cursor_v1.0/webcam_cursor_linux.run)


Make file executable:

    $ chmod +x webcam_cursor_linux.run


Run application:

    $ ./webcam_cursor_linux.run


## Windows
Download .exe from Releases:  [webcam_cursor.exe](https://github.com/nexayq/webcam_cursor/releases/download/webcam_cursor_v1.0/webcam_cursor.exe)



# Development

## Ubuntu - install dependencies
    $ cd install/ubuntu/
    $ ./install_dependencies.sh


## Run
    $ cd source/
    $ ./run.sh

[aruco_screenshot]:       https://github.com/nexayq/webcam_cursor/blob/master/data/screenshots/aruco_screenshot.png
[color_screenshot]:       https://github.com/nexayq/webcam_cursor/blob/master/data/screenshots/color_screenshot.png

[aruco_symbol]:           https://github.com/nexayq/webcam_cursor/blob/master/source/aruco_43.png
