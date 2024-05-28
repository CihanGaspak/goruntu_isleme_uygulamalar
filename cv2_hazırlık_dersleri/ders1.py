import cv2
import numpy as np
import pyttsx3

# Speech engine oluştur
engine = pyttsx3.init()

# Türkçe sesleri almak için kayıt defteri konumunu ayarla
registry_path = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech_OneCore\\Voices\\Tokens\\2"
engine.setProperty('voice', registry_path)

# Metni konuştur
engine.say("Merhaba, nasılsınız?")

# Konuşmayı başlat
engine.runAndWait()


#foto yolunu giriyoruz
#resim = cv2.imread("C:\\Users\\DELL\\Desktop\\yapayzeka\\Goruntu_Isleme\\ejderha.jpg",0) 

#bir pencerede gösteriyoruz
#cv2.imshow("Ejderha",resim)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


