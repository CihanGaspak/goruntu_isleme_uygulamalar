import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Kamera ayarları
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Genişlik
cap.set(4, 720)   # Yükseklik

# Gerekli görselleri içe aktar
imgBackground = cv2.imread(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\pong_oyunu\Background.png")
imgGameOver = cv2.imread(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\pong_oyunu\gameOver.png")
imgBall = cv2.imread(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\pong_oyunu\Ball.png", cv2.IMREAD_UNCHANGED)  # Bu satırı ekleyin
imgBat1 = cv2.imread(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\pong_oyunu\bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\pong_oyunu\bat2.png", cv2.IMREAD_UNCHANGED)
winner = cv2.imread(r"C:\Users\DELL\Desktop\yapayzeka\Goruntu_Isleme\pong_oyunu\winner.png", cv2.IMREAD_UNCHANGED)


# El tespiti için bir detektör oluştur
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Topun başlangıç ​​konumu ve hızı
ballPos = [100, 100]
speedX = 12
speedY = 12


# Oyun durumu ve skor
gameOver = False
score = [0, 0]
winner_score = 0
winner_x = 590

while True:
    # Kameradan görüntüyü al
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()  # Görüntüyü kopyala

    # Elleri ve el işaretlerini tespit et
    hands, img = detector.findHands(img, flipType=False)  # Elleri tespit et ve görselleştir

    # Arka plan görselini ekleyin
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Elleri kontrol et
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            # Sol el kontrolü
            if hand['type'] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            # Sağ el kontrolü
            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    # Oyun sonu kontrolü
    if ballPos[0] < 70 or ballPos[0] > 1210:
        gameOver = True

    if gameOver:
        img = imgGameOver
        # Kazananı belirle
        if score[0] > score[1]:
            winner_text = "Sol Oyuncu Kazandi!"
            winner_score = score[0]
            winner_x = 360
        elif score[0] < score[1]:
            winner_text = "Sag Oyuncu Kazandi!"
            winner_score = score[1]
            winner_x = 860
        else:
            winner_text = "Berabere!"
        # Kazananı ekrana yazdır
        cv2.putText(img, str(winner_score).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                    2.5, (200, 0, 200), 5)
        text_size, _ = cv2.getTextSize(winner_text, cv2.FONT_HERSHEY_COMPLEX, 2, 2)
        img = cvzone.overlayPNG(img, winner, (winner_x, 460))
        

    # Oyun bitmediyse topu hareket ettir
    else:
        # Topun sınırlara çarpma kontrolü
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Topu çiz
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        # Skorları ekrana yazdır
        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

    # Orijinal görüntüyü küçültüp ekrana ekleyin
    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        # Oyunu yeniden başlat
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/gameOver.png")
    elif key == 27: 
        break    
