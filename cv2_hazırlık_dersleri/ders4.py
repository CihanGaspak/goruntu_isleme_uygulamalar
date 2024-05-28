import cv2

yakala = cv2.VideoCapture(0)

# yakalanan fotoları video olarak izlememizi sağlıyor

while True:
    deger, kare = yakala.read()
    aynalanan_kare = cv2.flip(kare, 1)
    cv2.imshow("ben", aynalanan_kare)
    a = cv2.waitKey(1)
    if a == 27: 
        break

yakala.release()
cv2.destroyAllWindows()
