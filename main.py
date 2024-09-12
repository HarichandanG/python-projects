"""
1. Capture the video from the video source
2. Detecting the Hand by importing mediapipe
3. Separating the index fingertip
4. Moving the mouse pointer using finger
5. Click operation
"""

import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)  # Capturing the video
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils  # Draws the landmarks
screen_width, screen_height = pyautogui.size()  # Getting screen width and height
index_x, index_y = 0, 0
threshold = 60  # Adjust threshold as needed
# Exponential Moving Average parameters
alpha = 0.5
prev_x, prev_y = index_x, index_y
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # RGB mode is used for Detecting anything from Frame or Video
    output = hand_detector.process(rgb_frame)  # Processing the RGB Frame
    hands = output.multi_hand_landmarks  # landmarks are the points in our Hand
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)  # drawing_utils draws the landmarks and displaying on the frame
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)  # since x-axis is horizontal
                y = int(landmark.y * frame_height)  # since y-axis is vertical
                if id == 8:  # For index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))  # Yellow circle formation
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)  # moving the cursor
                if id == 4:  # For thumb finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('outside', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < threshold:  # absolute difference
                        pyautogui.click()  # clicking
                        pyautogui.sleep(1)
    # Apply Exponential Moving Average to smooth cursor movement
    index_x = int(alpha * index_x + (1 - alpha) * prev_x)
    index_y = int(alpha * index_y + (1 - alpha) * prev_y)
    prev_x, prev_y = index_x, index_y
    pyautogui.moveTo(index_x, index_y, duration=0.1)  # Smoothly move the mouse
    cv2.imshow('Virtual Mouse', frame)  # Displaying the image
    cv2.waitKey(1)
