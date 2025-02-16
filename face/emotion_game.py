import cv2
import numpy as np
from fer import FER
import time

def emotion_learning_game():
    # Initialize the face emotion recognition detector
    emotion_detector = FER(mtcnn=True)

    # Use phone camera (IP Webcam)
    phone_camera_url = "http://192.168.31.49:8080/video"
    cap = cv2.VideoCapture(phone_camera_url)

    if not cap.isOpened():
        print("❌ Error: Could not connect to phone camera.")
        return

    # Set up scenarios
    scenarios = [
        ("Your watch is lost. How would you feel?", "sad"),
        ("You won a prize! How would you feel?", "happy")
    ]

    for scenario, target_emotion in scenarios:
        print(f"\n=== Emotion Learning Game ===")
        print(f"\nScenario: {scenario}")
        print(f"Please show a {target_emotion} face to the camera.")
        print("\nPress 'q' to quit the game.")

        correct_emotion_shown = False
        start_time = time.time()
        feedback_duration = 2  # Duration to show feedback in seconds

        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Error: Could not access the camera stream.")
                break

            frame = cv2.flip(frame, 1)
            emotions = emotion_detector.detect_emotions(frame)
            display_frame = frame.copy()

            if emotions:
                emotion_data = emotions[0]
                emotions_dict = emotion_data['emotions']
                dominant_emotion = max(emotions_dict, key=emotions_dict.get)
                box = emotion_data['box']
                cv2.rectangle(display_frame, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)

                if dominant_emotion.lower() == target_emotion:
                    if not correct_emotion_shown:
                        correct_emotion_shown = True
                        start_time = time.time()
                    cv2.putText(display_frame, "✅ Correct!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(display_frame, f"😕 Try to show a {target_emotion} face (Current: {dominant_emotion})",
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('Emotion Learning Game', display_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if correct_emotion_shown and (time.time() - start_time) > feedback_duration:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    emotion_learning_game()
