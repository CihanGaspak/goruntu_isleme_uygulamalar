import cv2
import time
import os
import ElizlemeModulu_v2 as htm
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170) #konuşma hızı

wCam, hCam = 640, 480
cap= cv2.VideoCapture(0)
cap.set(3, wCam)  
cap.set(4, hCam)

#fotoların yolu
folderPath = r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\Parmaklar"
myList = os.listdir(folderPath)
#print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')

    overlayList.append(image)
#print(len(overlayList))    

pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4,8,12,16,20]

while True:
    success, img = cap.read()
    
    #videoyu aynala
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    #print(lmList)

    if len(lmList) !=0:
        fingers = []

        #basparmak 
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)    

        #4 parmak
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]

        #ekranda kaç parmak oldugunu yazdır
        cv2.rectangle(img, (20,255), (170,425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)  

        #if totalFingers ==4:
        #    engine.say("HELLO WORLD")
        #    engine.runAndWait()        

    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


    cv2.imshow("Image", img)
    #esc'ye basınca kapat
    a = cv2.waitKey(1)
    if a == 27: 
        break 
    