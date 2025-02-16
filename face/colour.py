import cv2
import numpy as np
import random

# Define color ranges in HSV format
color_ranges = {
    "Red": [(0, 120, 70), (10, 255, 255)],
    "Green": [(36, 50, 70), (89, 255, 255)],
    "Blue": [(90, 50, 70), (128, 255, 255)],
}

# Choose a random target color
target_color = random.choice(list(color_ranges.keys()))

# Open webcam
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

print(f"Find an object of color: {target_color}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_color = None
    correct_detected = False

    # Check all colors
    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        color_pixels = cv2.countNonZero(mask)

        if color_pixels > 5000:  # If enough pixels of a color are detected
            detected_color = color
            if detected_color == target_color:
                correct_detected = True
            break  # Stop checking further if any color is detected

    # Display messages based on detection
    if correct_detected:
        cv2.putText(frame, "Correct!", (50, 50), font, 1, (0, 255, 0), 3)
    elif detected_color and detected_color != target_color:
        cv2.putText(frame, "Wrong! Try Again!", (50, 50), font, 1, (0, 0, 255), 3)
    else:
        cv2.putText(frame, f"Find {target_color}!", (50, 50), font, 1, (255, 255, 255), 3)

    # Show the frames
    cv2.imshow("Game", frame)

    # Press 'q' to quit the game
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
