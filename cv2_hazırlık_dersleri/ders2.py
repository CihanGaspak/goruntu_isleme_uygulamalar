import cv2

# Görüntüyü oku
image = cv2.imread(r"C:\src\survival_in_medieval\assets\icons\logo.png")

# Görüntünün başarılı bir şekilde yüklenip yüklenmediğini kontrol et
if image is None:
    print("Görüntü yüklenemedi. Dosya yolunu kontrol edin.")
else:
    # Görüntü boyutunu al
    height, width = image.shape[:2]

    # Yeniden boyutlandırma oranı
    scale = 2  # İstediğiniz oranı ayarlayın, örneğin 2 kat büyütmek için 2 kullanabilirsiniz

    # Yeniden boyutlandırma işlemi
    new_height = int(height * scale)
    new_width = int(width * scale)
    upscaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    # Yeniden boyutlandırılmış görüntüyü göster
    cv2.imshow("Upscaled Image", upscaled_image)
    cv2.imshow("normal hali", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()