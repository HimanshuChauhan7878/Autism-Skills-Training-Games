import cv2
import mediapipe as mp
import random
import time

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Define gestures with landmark indices
GESTURES = {
    "Thumbs Up": [(4, 2)],  # Thumb tip above thumb MCP
    "Peace Sign": [(8, 6), (12, 10)],  # Index and middle fingers extended
    "OK Sign": [(4, 8)],  # Thumb and index finger touching
    "Fist": [(8, 6), (12, 10), (16, 14), (20, 18)],  # All fingers curled
    "Five Fingers Open": [(8, 6, True), (12, 10, True), (16, 14, True), (20, 18, True)],  # All fingers extended
    "Pointing Up": [(8, 6), (12, 10, False), (16, 14, False), (20, 18, False)],  # Index extended, others curled
    "Rock Sign": [(8, 6, False), (12, 10, False), (16, 14, False), (20, 18, True)],  # Index & pinky extended
    "Three Fingers Up": [(8, 6, True), (12, 10, True), (16, 14, True)],  # Thumb, index, and middle extended
}

# Initialize variables
score = 0
gesture_to_match = random.choice(list(GESTURES.keys()))
start_time = time.time()
MAX_GAME_TIME = 60  # Run for 60 seconds

# Use phone camera if available, otherwise use default webcam
PHONE_CAMERA_URL = "http://192.168.31.49:8080/video"
cap = cv2.VideoCapture(PHONE_CAMERA_URL)  # Try to open phone camera

if not cap.isOpened():  # If phone camera fails, use default webcam
    print("Phone camera not available, using laptop webcam.")
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Gesture Recognition Game Started!")

def check_gesture(landmarks, gesture_name):
    conditions = GESTURES[gesture_name]
    for condition in conditions:
        if len(condition) == 2:
            tip, base = condition
            if landmarks[tip].y > landmarks[base].y:
                return False
        elif len(condition) == 3:
            tip, base, extended = condition
            if (landmarks[tip].y < landmarks[base].y) != extended:
                return False
    return True

while cap.isOpened() and (time.time() - start_time) < MAX_GAME_TIME:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Display gesture to match
    cv2.putText(frame, f"Match: {gesture_to_match}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Check if gesture matches
            landmarks = hand_landmarks.landmark
            if check_gesture(landmarks, gesture_to_match):
                score += 1
                gesture_to_match = random.choice(list(GESTURES.keys()))
                start_time = time.time()  # Reset timer for next gesture

    # Show score
    cv2.putText(frame, f"Score: {score}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (255, 0, 0), 2)

    # Display frame
    cv2.imshow("Hand Gesture Game", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Game exited by user.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Gesture Recognition Game Ended.")
