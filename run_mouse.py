import cv2
import mediapipe as mp
from mediapipe.python import solutions as mp_solutions # type: ignore
import pyautogui
import numpy as np
import time
from collections import deque
import pygetwindow as gw

class GestureController:
    def __init__(self, cam_id=0, frame_reduction=200, smoothing=5, click_distance=30, swipe_threshold=50, swipe_vertical_threshold=40, scroll_threshold=20):
        self.cam_id = cam_id
        self.frame_reduction = frame_reduction
        self.smoothing = smoothing
        self.click_distance = click_distance
        self.swipe_threshold = swipe_threshold
        self.swipe_vertical_threshold = swipe_vertical_threshold
        self.scroll_threshold = scroll_threshold
        
        pyautogui.FAILSAFE = True
        self.screen_width, self.screen_height = pyautogui.size()

        self.mp_hands = mp_solutions.hands
        self.mp_drawing = mp_solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        self.cap = cv2.VideoCapture(self.cam_id)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera with ID {self.cam_id}.")
            return

        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0

        self.last_action_time = 0
        self.action_cooldown = 1.0

        self.swipe_history = deque(maxlen=10)
        self.swipe_history_y = deque(maxlen=10)
        self.scroll_history = deque(maxlen=10)
        self.volume_history = deque(maxlen=10)

    def are_fingers_up(self, hand_landmarks):
        finger_tips_y = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y
        ]
        finger_pips_y = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].y,
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP].y
        ]
        for i in range(5):
            if finger_tips_y[i] > finger_pips_y[i]:
                return False
        return True

    def is_two_fingers_up(self, hand_landmarks):
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]

        if not (index_tip.y < index_pip.y and middle_tip.y < middle_pip.y):
            return False
        
        if not (ring_tip.y > ring_pip.y and pinky_tip.y > pinky_pip.y):
            return False

        return True

    def is_thumbs_up(self, hand_landmarks):
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
        
        if thumb_tip.y > thumb_ip.y:
            return False

        finger_tips = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        ]
        finger_pips = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
        ]
        for i in range(4):
            if finger_tips[i].y < finger_pips[i].y:
                return False
        return True

    def is_fist(self, hand_landmarks):
        finger_tips = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        ]
        finger_pips = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
        ]
        for i in range(4):
            if finger_tips[i].y < finger_pips[i].y:
                return False
        return True

    def is_palm_open(self, hand_landmarks):
        finger_tips = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        ]
        finger_pips = [
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
        ]
        
        for i in range(4):
            if finger_tips[i].y > finger_pips[i].y:
                return False
        return True

    def handle_gestures(self, hand_landmarks, frame_width, frame_height):
        current_time = time.time()
        
        if self.is_fist(hand_landmarks):
            if current_time - self.last_action_time > self.action_cooldown:
                print("Fist detected, closing window.")
                pyautogui.hotkey('alt', 'f4')
                self.last_action_time = current_time
            self.clear_histories()
            return

        if self.are_fingers_up(hand_landmarks):
            wrist_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].y * frame_height
            self.swipe_history_y.append(wrist_y)
            if len(self.swipe_history_y) == self.swipe_history_y.maxlen:
                if self.swipe_history_y[-1] - self.swipe_history_y[0] > self.swipe_vertical_threshold:
                    if current_time - self.last_action_time > self.action_cooldown:
                        print("Downward swipe with five fingers detected, minimizing window.")
                        try:
                            active_window = gw.getActiveWindow()
                            if active_window:
                                active_window.minimize()
                        except Exception as e:
                            print(f"Could not minimize window: {e}")
                        self.last_action_time = current_time
                        self.clear_histories()
            return
        
        if self.is_two_fingers_up(hand_landmarks):
            index_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame_height
            self.scroll_history.append(index_y)
            if len(self.scroll_history) == self.scroll_history.maxlen:
                if self.scroll_history[0] - self.scroll_history[-1] > self.scroll_threshold:
                    print("Scrolling up")
                    pyautogui.scroll(20) 
                    self.scroll_history.clear()
                elif self.scroll_history[-1] - self.scroll_history[0] > self.scroll_threshold:
                    print("Scrolling down")
                    pyautogui.scroll(-20)
                    self.scroll_history.clear()
            return

        if self.is_thumbs_up(hand_landmarks):
            thumb_x = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].x * frame_width
            self.volume_history.append(thumb_x)
            if len(self.volume_history) == self.volume_history.maxlen:
                if self.volume_history[-1] - self.volume_history[0] > self.swipe_threshold:
                    if current_time - self.last_action_time > self.action_cooldown:
                        print("Volume up")
                        pyautogui.press('volumeup')
                        self.last_action_time = current_time
                        self.volume_history.clear()
                elif self.volume_history[0] - self.volume_history[-1] > self.swipe_threshold:
                    if current_time - self.last_action_time > self.action_cooldown:
                        print("Volume down")
                        pyautogui.press('volumedown')
                        self.last_action_time = current_time
                        self.volume_history.clear()
            return

        if self.is_palm_open(hand_landmarks):
            print("Palm is open")
            wrist_x = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST].x * frame_width
            self.swipe_history.append(wrist_x)

            if len(self.swipe_history) == self.swipe_history.maxlen:
                if self.swipe_history[-1] - self.swipe_history[0] > self.swipe_threshold:
                    if current_time - self.last_action_time > self.action_cooldown:
                        print("Swipe right detected.")
                        pyautogui.hotkey('alt', 'tab')
                        self.last_action_time = current_time
                        self.swipe_history.clear()
                elif self.swipe_history[0] - self.swipe_history[-1] > self.swipe_threshold:
                    if current_time - self.last_action_time > self.action_cooldown:
                        print("Swipe left detected.")
                        pyautogui.hotkey('alt', 'shift', 'tab')
                        self.last_action_time = current_time
                        self.swipe_history.clear()
        else:
            self.clear_histories()
            self.handle_mouse_movement(hand_landmarks, frame_width, frame_height)

    def clear_histories(self):
        self.swipe_history.clear()
        self.swipe_history_y.clear()
        self.scroll_history.clear()
        self.volume_history.clear()

    def handle_mouse_movement(self, hand_landmarks, frame_width, frame_height):
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]

        x1 = int(index_tip.x * frame_width)
        y1 = int(index_tip.y * frame_height)
        x2 = int(thumb_tip.x * frame_width)
        y2 = int(thumb_tip.y * frame_height)

        x3 = np.interp(x1, (self.frame_reduction, frame_width - self.frame_reduction), (0, self.screen_width))
        y3 = np.interp(y1, (self.frame_reduction, frame_height - self.frame_reduction), (0, self.screen_height))

        self.clocX = self.plocX + (x3 - self.plocX) / self.smoothing
        self.clocY = self.plocY + (y3 - self.plocY) / self.smoothing
        
        pyautogui.moveTo(self.clocX, self.clocY)
        self.plocX, self.plocY = self.clocX, self.clocY

        distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        print(f"Distance: {distance:.2f}")
        if distance < self.click_distance:
            if time.time() - self.last_action_time > self.action_cooldown:
                pyautogui.click()
                self.last_action_time = time.time()
                print("Clicked")

    def run(self):
        print("System started. Press 'q' to exit.")
        while True:
            success, frame = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            cv2.rectangle(frame, (self.frame_reduction, self.frame_reduction), 
                         (frame_width - self.frame_reduction, frame_height - self.frame_reduction),
                         (255, 0, 255), 2)

            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                print("Hand detected.")
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    self.handle_gestures(hand_landmarks, frame_width, frame_height)
            else:
                print("No hand detected.")
                self.clear_histories()

            cv2.imshow('Gesture Controller', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    controller = GestureController()
    controller.run()