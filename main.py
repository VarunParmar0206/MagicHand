import cv2
import mediapipe as mp
import math
import time
from pynput.keyboard import Controller, Key

# Initialize keyboard controller
keyboard = Controller()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2
)

# Initialize webcam - CHANGE THE INDEX IF NEEDED (0, 1, 2, etc.)
cap = cv2.VideoCapture(1)

# Function to calculate distance between two landmarks
def calculate_distance(landmark1, landmark2):
    """Calculate Euclidean distance between two hand landmarks"""
    x1, y1 = landmark1.x, landmark1.y
    x2, y2 = landmark2.x, landmark2.y
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

# Gesture state tracking
class GestureState:
    def __init__(self):
        self.left_touch_count = 0
        self.right_touch_count = 0
        self.last_left_touch_time = 0
        self.last_right_touch_time = 0
        self.touch_cooldown = 0.8  # Cooldown after action executed
        self.double_tap_window = 0.6  # Time window for double tap (increased from 0.4)
        self.right_action_pending = False
        self.right_pending_timer = None
        self.single_tap_delay = 0.5  # Delay before executing single tap
        
    def reset_left_count(self):
        """Reset left hand touch count after timeout"""
        if time.time() - self.last_left_touch_time > self.double_tap_window:
            self.left_touch_count = 0
    
    def reset_right_count(self):
        """Reset right hand touch count after timeout"""
        if time.time() - self.last_right_touch_time > self.double_tap_window:
            self.right_touch_count = 0
            self.right_action_pending = False

gesture_state = GestureState()

# Thresholds
TOUCH_THRESHOLD = 0.05
Y_THRESHOLD = 0.7  # Hand must be above this Y-level (0=top, 1=bottom). Adjust between 0.5-0.8
previous_left_touching = False
previous_right_touching = False

print("Hand Gesture Music Controller Started!")
print("Controls:")
print("- Right Hand: Index finger + Thumb single touch = Next song")
print("- Right Hand: Index finger + Thumb double touch = Pause/Play")
print("- Left Hand: Index finger + Thumb single touch = Previous song")
print(f"- Gesture Detection Zone: Above {int((1-Y_THRESHOLD)*100)}% of screen height")
print("Press 'q' to quit\n")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Failed to grab frame")
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    gesture_state.reset_left_count()
    gesture_state.reset_right_count()
    
    left_hand_touching = False
    right_hand_touching = False
    
    # Draw activation zone line on frame
    h, w, c = frame.shape
    zone_y = int(Y_THRESHOLD * h)
    cv2.line(frame, (0, zone_y), (w, zone_y), (0, 255, 255), 2)
    cv2.putText(frame, "ACTIVATION ZONE ABOVE THIS LINE", (10, zone_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    # Check if pending right hand action should execute
    if gesture_state.right_action_pending:
        if time.time() - gesture_state.last_right_touch_time > gesture_state.single_tap_delay:
            # Execute single tap action
            print("Right Hand: Single Touch Confirmed - Next Song")
            try:
                keyboard.press(Key.media_next)
                keyboard.release(Key.media_next)
            except:
                keyboard.press(Key.shift)
                keyboard.press('n')
                keyboard.release('n')
                keyboard.release(Key.shift)
            gesture_state.right_action_pending = False
            gesture_state.right_touch_count = 0
    
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS
            )
            
            hand_label = handedness.classification[0].label
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            # Get wrist landmark for Y-position check
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            
            # Check if hand is in activation zone (above Y_THRESHOLD)
            is_in_activation_zone = wrist.y < Y_THRESHOLD
            
            distance = calculate_distance(thumb_tip, index_tip)
            
            cx, cy = int(thumb_tip.x * w), int(thumb_tip.y * h)
            
            # Display hand status
            zone_status = "ACTIVE" if is_in_activation_zone else "INACTIVE"
            color = (0, 255, 0) if is_in_activation_zone else (0, 0, 255)
            cv2.putText(frame, f"{hand_label}: {zone_status} - {distance:.2f}", 
                       (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, color, 2)
            
            # Only process gestures if hand is in activation zone
            if not is_in_activation_zone:
                continue
            
            # Detect touch gesture
            is_touching = distance < TOUCH_THRESHOLD
            
            if hand_label == "Right":
                right_hand_touching = is_touching
                
                if right_hand_touching and not previous_right_touching:
                    current_time = time.time()
                    
                    # Check if within double tap window
                    if current_time - gesture_state.last_right_touch_time < gesture_state.double_tap_window:
                        gesture_state.right_touch_count += 1
                    else:
                        gesture_state.right_touch_count = 1
                    
                    gesture_state.last_right_touch_time = current_time
                    
                    if gesture_state.right_touch_count == 1:
                        # Don't execute immediately, wait to see if double tap comes
                        print("Right Hand: Touch detected, waiting for possible double tap...")
                        cv2.putText(frame, "TOUCH 1", (50, 50), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                        gesture_state.right_action_pending = True
                        
                    elif gesture_state.right_touch_count == 2:
                        # Cancel pending single tap and execute double tap
                        print("Right Hand: Double Touch Detected - Pause/Play")
                        cv2.putText(frame, "PAUSE/PLAY", (50, 50), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                        gesture_state.right_action_pending = False
                        try:
                            keyboard.press(Key.media_play_pause)
                            keyboard.release(Key.media_play_pause)
                        except:
                            keyboard.press('k')
                            keyboard.release('k')
                        time.sleep(0.1)
                        gesture_state.right_touch_count = 0
            
            elif hand_label == "Left":
                left_hand_touching = is_touching
                
                if left_hand_touching and not previous_left_touching:
                    current_time = time.time()
                    
                    # Left hand executes immediately (no double tap needed)
                    if current_time - gesture_state.last_left_touch_time > gesture_state.touch_cooldown:
                        gesture_state.left_touch_count += 1
                        gesture_state.last_left_touch_time = current_time
                        
                        print("Left Hand: Single Touch Detected - Previous Song")
                        cv2.putText(frame, "PREVIOUS SONG", (50, 100), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)
                        try:
                            keyboard.press(Key.media_previous)
                            keyboard.release(Key.media_previous)
                        except:
                            keyboard.press(Key.shift)
                            keyboard.press('p')
                            keyboard.release('p')
                            keyboard.release(Key.shift)
                        time.sleep(0.1)
    
    previous_left_touching = left_hand_touching
    previous_right_touching = right_hand_touching
    
    cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    cv2.imshow('Hand Gesture Music Controller', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
