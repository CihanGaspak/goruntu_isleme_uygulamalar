import cv2
import numpy as np
import time
import ElizlemeModulu_v2 as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################
wCam, hCam = 640, 480
######################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionCon=0.7)

#ses ayarlarını kullanmak için gereken kodlar
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

#ekranda volumeyi göstermek için
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    #videoyu aynala
    img = cv2.flip(img,1)

    #eklemleri göster
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        
        #orta noktayı bul
        cx, cy = (x1+x2) //2,  (y1+y2) //2

        #parmaklara daire çiz
        cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
        
        #daireleri birleştir
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        #orta noktaya daire çiz
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        #parmak arası acıklıgı belirliyoruz 
        length = math.hypot(x2-x1, y2-y1)
        #ne kadar oldugunu yazdırıyoruz(ekrandan uzaklık durumuna göre artıp azalıyor)
        #print(int(length))

        #parmakların kapalı oldugu durum 50 acık oldugu durum 300 diye kabul ediyoruz
        #sesin kapalı oldugu durum -65 acık oldugu durumu da 0 olarak kabul ediyoruz
        
        vol = np.interp(length, [50,300], [minVol, maxVol])
        volBar = np.interp(length, [50,300], [400, 150])
        volPer = np.interp(length, [50,300], [0, 100])

        #ses seviyesini yazdır
        print(int(length),vol)
        #ses degerini guncelle
        volume.SetMasterVolumeLevel(vol, None)

        #uzaklık 50den kucukse parmakların kapalı oldugu varsayılıyor 
        #kapalı oldugunu göstermek için de kırmızı daire çizdiriyoruz
        if length<50:
            cv2.circle(img, (cx, cy), 20, (0, 0, 255), cv2.FILLED)

    #volbarı ekranda göster
    cv2.rectangle(img, (50,150), (85,400), (0, 255, 0), 3)
    cv2.rectangle(img, (50,int(volBar)), (85,400), (0, 255, 0), cv2.FILLED)
    #sesin %'sini yaz
    cv2.putText(img, f'% {int(volPer)}', (40,450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
    
    #FPS Göster
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)


    # videoyu göster
    cv2.imshow("Img", img)

    #esc'ye basınca kapat
    a = cv2.waitKey(1)
    if a == 27: 
        break