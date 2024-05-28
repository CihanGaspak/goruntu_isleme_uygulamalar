import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

pyautogui.FAILSAFE = False

index_x = 0
index_y = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks 

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            for id, landmark in enumerate(hand.landmark):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=14, color=(0, 255, 0))
                    index_x = screen_width / frame_width * x 
                    index_y = screen_height / frame_height * y
                elif id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=14, color=(0, 255, 0))
                    thumb_x = screen_width / frame_width * x 
                    thumb_y = screen_height / frame_height * y  
                    print("disinda", abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 10:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:  
                        pyautogui.moveTo(index_x, index_y)  

    cv2.imshow("sanal fare", frame)

    # esc'ye basınca kapat
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
