# Screen Recorder

## Overview

Screen Recorder is a simple Python application that allows you to capture your screen along with the mouse cursor's position. It provides a user-friendly graphical interface using the Tkinter library, and the recording is done using OpenCV and PyAutoGUI.

## Features

- **Screen Recording:** Capture your screen in real-time.
- **Mouse Cursor Tracking:** Record the movement of the mouse cursor.
- **User-Friendly GUI:** Intuitive graphical interface for easy operation.
- **Elapsed Time Display:** Track the duration of your recording.

## How it works?

This code creates a Tkinter GUI with buttons to start and stop screen recording. The recording includes the captured screen and the mouse cursor's position, displayed on a canvas. The recorded video is saved as an AVI file in the user's "Documents" directory. The GUI is updated in real-time to show the elapsed time, current mouse position, and the captured screen with the mouse cursor. The recording is done in a separate thread to prevent freezing the GUI during the recording process.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3
- OpenCV
- PyAutoGUI
- Pillow (PIL)
- ScreenInfo

You can install these dependencies by running the provided `setup.py` script:

python setup.py

## Getting Started

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/imasharc/screenrec.git
    ```

2. Install the required libraries:

    ```bash
    python setup.py
    ```

3. Run the application:

    ```bash
    python main.py
    ```

4. Use the "Start Recording" and "Stop Recording" buttons to control the screen recording.

## Configuration

You can customize the recording settings, such as output file location and video parameters, by modifying the `main.py` file.