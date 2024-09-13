# Virtual-Mouse

Here's a detailed description you can use for your Git repository, outlining the project's purpose, features, and setup instructions:

Virtual Gesture Control Mouse using Mediapipe and OpenCV
This project implements a virtual gesture-controlled mouse using a webcam, Mediapipe, and OpenCV. The application tracks hand gestures in real-time, allowing you to control your computer’s cursor and perform mouse actions like clicking, dragging, and scrolling, without touching a physical mouse.

Features
Real-Time Hand Tracking: Uses Mediapipe's hand tracking module to detect and track hand movements accurately.
Gesture Recognition: Recognizes various gestures such as:
Move Cursor: Control the cursor position using your index finger.
Left Click: Perform a left-click by bringing the index and middle fingers close together.
Right Click: Perform a right-click by bringing the index, middle, and ring fingers close together.
Dragging: Initiate a drag-and-drop operation by touching the thumb and index finger together.
Scrolling: Control scrolling actions by moving your pinky finger up or down relative to your index finger.
Smooth Cursor Movement: Implements a smoothing function to reduce jittery cursor movements, providing a more natural user experience.
High FPS Performance: Optimized to run at high frame rates, ensuring smooth and responsive control.



#Installation and Setup
Clone the Repository

bash
git clone https://github.com/your-username/gesture-control-mouse.git
cd gesture-control-mouse
Install Dependencies Ensure you have Python installed, then install the required libraries:

bash
pip install opencv-python mediapipe pyautogui numpy
Run the Application Start the application using the following command:

bash
python gesture_control_mouse.py
Usage
Start the program: The application will automatically detect your hand when placed in view of your webcam.
Control the cursor: Move your hand to control the cursor's position on the screen.
Perform gestures: Use predefined hand gestures for clicking, dragging, and scrolling.
Exit the application: Press 'q' on your keyboard to close the application.
Requirements
Python 3.7 or higher
A functional webcam
Libraries: OpenCV, Mediapipe, PyAutoGUI, Numpy
