# Hand-Controlled Mouse

This project allows you to control your computer's mouse using hand gestures captured through your webcam. It uses computer vision to track your hand movements and translate them into mouse actions, such as moving the cursor and clicking.

## Technologies Used

*   **Python**: The core programming language for the application.
*   **OpenCV**: Used for capturing video from the webcam and processing images.
*   **MediaPipe**: Google's open-source framework for building multimodal (e.g., video, audio, any time series data) applied ML pipelines. We use it for hand tracking.
*   **PyAutoGUI**: A cross-platform GUI automation Python module used to programmatically control the mouse and keyboard.
*   **NumPy**: A fundamental package for scientific computing with Python, used here for numerical operations.

## Features

*   **Mouse Movement**: Control the cursor by moving your index finger.
*   **Clicking**: Perform a click by pinching your thumb and index finger together.
*   **Configurable Controls**: Easily adjust settings like mouse smoothing and click sensitivity.

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
    *(Note: You will need to create a `requirements.txt` file. See the section below.)*

### Creating the `requirements.txt` file

To make it easy for others to install the dependencies, create a `requirements.txt` file by running this command in your activated virtual environment:

```bash
pip freeze > requirements.txt
```

## How to Run

Execute the main script to start the application:

```bash
python run_mouse.py
```

A window will appear showing your webcam feed. Place your hand in the frame to begin controlling the mouse. Press `q` with the video window in focus to quit the application.

## Calibration

You can fine-tune the mouse control by editing the configuration variables at the top of the `run_mouse.py` script:

*   `SMOOTHING`: A higher value will make the cursor movement smoother but might add a slight delay. A lower value will make it more responsive but potentially more jittery.
*   `CLICK_DISTANCE`: This is the distance (in pixels on the camera feed) between your thumb and index finger to trigger a click. Adjust this value based on your preference and camera resolution.
*   `CAM_ID`: If you have multiple cameras, you may need to change this value (e.g., to `1`, `2`, etc.) to select the correct one.
