import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize hand tracking with Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Get screen size for mapping hand movements to mouse movements
screen_width, screen_height = pyautogui.size()

# Set up webcam capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set the resolution for better performance
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)           # Set the camera's FPS setting, if supported

# State variables to manage actions
clicking = False
dragging = False
scrolling = False
prev_x, prev_y = 0, 0  # Previous cursor positions for smoothing movement
smooth_factor = 0.2    # Smoothing factor for smoother cursor motion

def distance(point1, point2):
    """Calculate the Euclidean distance between two points."""
    return np.hypot(point2[0] - point1[0], point2[1] - point1[1])

def smooth_movement(curr_x, curr_y, prev_x, prev_y):
    """Smooth cursor movement using a simple weighted average."""
    x = prev_x + (curr_x - prev_x) * smooth_factor
    y = prev_y + (curr_y - prev_y) * smooth_factor
    return x, y

def perform_gestures(index_tip, thumb_tip, middle_tip, ring_tip, pinky_tip):
    """Check for specific gestures and perform corresponding actions."""
    global clicking, dragging, scrolling, prev_x, prev_y

    # Convert index finger position to screen coordinates
    screen_x = index_tip[0] * screen_width / frame_width
    screen_y = index_tip[1] * screen_height / frame_height

    # Smooth the movement to avoid jittery cursor motion
    screen_x, screen_y = smooth_movement(screen_x, screen_y, prev_x, prev_y)
    prev_x, prev_y = screen_x, screen_y

    # Move the mouse cursor based on the index finger's position
    pyautogui.moveTo(screen_x, screen_y)

    # Left Click: Index and middle fingers close together
    if distance(index_tip, middle_tip) < 30:
        if not clicking:
            clicking = True
            pyautogui.click()
    else:
        clicking = False

    # Right Click: Index, middle, and ring fingers close together
    if distance(index_tip, ring_tip) < 30 and distance(middle_tip, ring_tip) < 30:
        pyautogui.click(button='right')

    # Dragging: Index finger and thumb close together
    if distance(index_tip, thumb_tip) < 30:
        if not dragging:
            dragging = True
            pyautogui.mouseDown()
        pyautogui.moveTo(screen_x, screen_y)
    else:
        if dragging:
            dragging = False
            pyautogui.mouseUp()

    # Scrolling: Pinky movement controls scrolling
    if index_tip[1] < pinky_tip[1] - 30:  # Scroll up
        if not scrolling:
            scrolling = True
            pyautogui.scroll(20)
    elif index_tip[1] > pinky_tip[1] + 30:  # Scroll down
        if not scrolling:
            scrolling = True
            pyautogui.scroll(-20)
    else:
        scrolling = False

# Main loop: Capture and process each frame from the webcam
while True:
    start_time = time.time()  # Measure the time at the start of the loop for FPS calculation
    ret, frame = cap.read()   # Read a frame from the webcam
    if not ret:
        break

    # Flip the frame horizontally for a mirror-like experience
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Convert the frame to RGB format as required by Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hand landmarks
    result = hands.process(rgb_frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get landmark positions of the hand
            landmarks = hand_landmarks.landmark
            # Extract the positions of finger tips
            index_tip = [landmarks[8].x * frame_width, landmarks[8].y * frame_height]
            thumb_tip = [landmarks[4].x * frame_width, landmarks[4].y * frame_height]
            middle_tip = [landmarks[12].x * frame_width, landmarks[12].y * frame_height]
            ring_tip = [landmarks[16].x * frame_width, landmarks[16].y * frame_height]
            pinky_tip = [landmarks[20].x * frame_width, landmarks[20].y * frame_height]

            # Perform gestures based on the detected landmarks
            perform_gestures(index_tip, thumb_tip, middle_tip, ring_tip, pinky_tip)

            # Draw landmarks on the frame for visualization
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display FPS on the video feed
    fps = int(1.0 / (time.time() - start_time))
    cv2.putText(frame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Show the video feed with gestures
    cv2.imshow("Virtual Gesture Control Mouse", frame)

    # Exit the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
