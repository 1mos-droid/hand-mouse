import cv2
import mediapipe as mp
from mediapipe.python import solutions as mp_solutions # type: ignore
import pyautogui
import numpy as np
import time

# --- Configuration ---
CAM_ID = 0
FRAME_REDUCTION = 100
SMOOTHING = 10  # Increase for more smoothing
CLICK_DISTANCE = 30  # Adjust as needed
pyautogui.FAILSAFE = True
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def main():
    mp_hands = mp_solutions.hands
    mp_drawing = mp_solutions.drawing_utils
    
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )

    cap = cv2.VideoCapture(CAM_ID)
    if not cap.isOpened():
        print(f"Error: Could not open camera with ID {CAM_ID}.")
        return

    plocX, plocY = 0, 0 
    clocX, clocY = 0, 0 
    last_click_time = 0

    print("System started. Press 'q' to exit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        cv2.rectangle(frame, (FRAME_REDUCTION, FRAME_REDUCTION), 
                     (frame_width - FRAME_REDUCTION, frame_height - FRAME_REDUCTION),
                     (255, 0, 255), 2)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            print("Hand detected.")
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                index_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]

                x1 = int(index_tip.x * frame_width)
                y1 = int(index_tip.y * frame_height)
                x2 = int(thumb_tip.x * frame_width)
                y2 = int(thumb_tip.y * frame_height)

                # Movement
                x3 = np.interp(x1, (FRAME_REDUCTION, frame_width - FRAME_REDUCTION), (0, SCREEN_WIDTH))
                y3 = np.interp(y1, (FRAME_REDUCTION, frame_height - FRAME_REDUCTION), (0, SCREEN_HEIGHT))

                # Smoothing
                clocX = plocX + (x3 - plocX) / SMOOTHING
                clocY = plocY + (y3 - plocY) / SMOOTHING
                
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY

                # Click
                distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
                print(f"Distance: {distance:.2f}")
                if distance < CLICK_DISTANCE:
                    cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    if time.time() - last_click_time > 0.5:
                        pyautogui.click()
                        last_click_time = time.time()
                        print("Clicked")
        else:
            print("No hand detected.")

        cv2.imshow('Gesture Controller', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()