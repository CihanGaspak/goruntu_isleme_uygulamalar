import cv2
import numpy as np
import time
import os
import ElizlemeModulu_v2 as htm

###################
brusThickness = 25
eraserThickness = 100
###################


folderPath = r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\UstMenu"
myList= os.listdir(folderPath)
print(myList)
overlayList= []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))    

header = overlayList[0]
drawColor = (252, 15, 192)  #ilk seçili renk pembe

#videoyu göster
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionCon=0.65, maxHands=1)
xp,yp = 0, 0 
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    #resim cek
    success, img = cap.read()
    #videoyu aynala
    img = cv2.flip(img,1)

    img = detector.findHands(img)
    lmList= detector.findPosition(img, draw=False)

    if len(lmList) !=0:
        x1, y1= lmList[8][1:]
        x2, y2= lmList[12][1:]

        fingers= detector.fingersUp()
        print(fingers)

        #seçim modunda ise(işaret parmagı ortaparmağı yukarıda)
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Seçim modu")
            #üst menüden renk ya da silgi seçimi
            if y1<125:
                if 250 < x1 < 450:
                    header=overlayList[0]
                    drawColor = (255, 192, 203)  # Pembe
                elif 550 < x1 < 750:
                    header=overlayList[1]
                    drawColor = (255, 20, 147)  # Mavi
                elif 800 < x1 < 950:
                    header=overlayList[2]
                    drawColor = (0, 128, 0)  # Yeşil
                elif 1050 < x1 < 1200:
                    header=overlayList[3]
                    drawColor = (0, 0, 0)  # Siyah
            cv2.rectangle(img, (x1,y1-25), (x2, y2+25), drawColor, cv2.FILLED)

        # eğer çizim modunda ise (sadece işaret ve ortaparmak yukarıda)    
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Çizim modu")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brusThickness)

            if drawColor == (0,0,0):
                cv2.line(img, (xp,yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness )

            else:
                cv2.line(img, (xp,yp), (x1, y1), drawColor, brusThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brusThickness )    

            xp, yp = x1, y1   


    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)


    #üst menü(header) resmini seçme
    img[0:125, 0:1280] = header

    #resmi göster
    cv2.imshow('Image',img)
    #cv2.imshow('Canvas',imgCanvas)
    #cv2.imshow('Inv', imgInv)
    
    #esc'ye basınca kapat
    a = cv2.waitKey(1)
    if a == 27: 
        break

mask = cv2.imread(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\nesne_tanima\traffic_video.mp4")
cv2.imwrite(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\nesne_tanima\traffic_video.mp4", img)