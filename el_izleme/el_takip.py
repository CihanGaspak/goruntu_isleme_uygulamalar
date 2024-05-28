import cv2
import mediapipe
import pyttsx3

camera = cv2.VideoCapture(0)

engine = pyttsx3.init()

mpHands = mediapipe.solutions.hands

hands= mpHands.Hands()

mpDraw = mediapipe.solutions.drawing_utils

basParmak= False

while True:
    deger, kare = camera.read()

    imgRGB = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)

    hlms= hands.process(imgRGB)


    height, width,channel = kare.shape

    if hlms.multi_hand_landmarks:
        for handlandmarks in hlms.multi_hand_landmarks:

            for fingerNum, landmark in enumerate(handlandmarks.landmark):
                positionX, positionY = int(landmark.x*width), int(landmark.y*height)

        
                #if fingerNum > 4 and landmark.y < handlandmarks.landmark[2].y:
                #    break

                #if fingerNum == 20 and landmark.y > handlandmarks.landmark[2].y:
                #    basParmak= True

                #bozkurt işareti tanıma
                

            mpDraw.draw_landmarks(kare, handlandmarks, mpHands.HAND_CONNECTIONS)


    cv2.imshow("video", kare)

    if basParmak:
        engine.say("HELLO WORLD")
        engine.runAndWait()
        break

    a = cv2.waitKey(1)
    if a == 27: 
        break