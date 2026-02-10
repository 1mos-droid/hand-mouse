# Hand-Controlled Mouse

This project allows you to control your computer's mouse using hand gestures captured through your webcam. It uses computer vision to track your hand movements and translate them into mouse actions, such as moving the cursor and clicking.

## Technologies Used

*   **Python**: The core programming language for the application.
*   **OpenCV**: Used for capturing video from the webcam and processing images.
*   **MediaPipe**: Google's open-source framework for building multimodal (e.g., video, audio, any time series data) applied ML pipelines. We use it for hand tracking.
*   **PyAutoGUI**: A cross-platform GUI automation Python module used to programmatically control the mouse and keyboard.
*   **NumPy**: A fundamental package for scientific computing with Python, used here for numerical operations.
*   **PyGetWindow**: Used to control application windows, for example, to minimize them.

## Gestures

*   **Mouse Movement**: Move the cursor by moving your index finger.
*   **Clicking**: Perform a click by pinching your thumb and index finger together.
*   **Close Window**: Make a fist to close the current active window (sends `Alt+F4`).
*   **Switch Window (Forward)**: With an open palm, swipe your hand to the right to switch to the next window (sends `Alt+Tab`).
*   **Switch Window (Backward)**: With an open palm, swipe your hand to the left to switch to the previous window (sends `Alt+Shift+Tab`).
*   **Minimize Window**: Hold all five fingers up and swipe downwards to minimize the active window.
*   **Scrolling**: Hold your index and middle fingers up and move your hand up or down to scroll.
*   **Volume Control**: Make a "thumbs up" gesture and move your hand left to decrease volume or right to increase volume.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/1mos-droid/hand-mouse.git
    cd hand-mouse
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

Execute the main script to start the application:

```bash
python run_mouse.py
```

A window will appear showing your webcam feed. Place your hand in the frame to begin controlling the mouse. Press `q` with the video window in focus to quit the application.

## Calibration

You can fine-tune the controls by editing the parameters in the `GestureController` class in `run_mouse.py`:

*   `smoothing`: A higher value will make the cursor movement smoother but might add a slight delay.
*   `click_distance`: The distance (in pixels on the camera feed) between your thumb and index finger to trigger a click.
*   `swipe_threshold`: The horizontal distance (in pixels) your hand needs to move to trigger a window-switching swipe.
*   `swipe_vertical_threshold`: The vertical distance your hand needs to move to trigger the minimize-window gesture.
*   `scroll_threshold`: The vertical distance your hand needs to move to trigger scrolling.
*   `cam_id`: If you have multiple cameras, you may need to change this value (e.g., to `1`, `2`, etc.).
