# Webcam Cursor
Move mouse cursor by following ArUco symbol 43(4x4) or specific color from your webcam


ArUco symbol 43 tracking
![Screenshot - ArUco symbol 43 tracking][aruco_screenshot]


Custom Color tracking
![Screenshot - Custom Color tracking][color_screenshot]


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

[aruco_screenshot]:       https://github.com/nexayq/follow_color/blob/master/data/screenshots/aruco_screenshot.png
[color_screenshot]:       https://github.com/nexayq/follow_color/blob/master/data/screenshots/color_screenshot.png
