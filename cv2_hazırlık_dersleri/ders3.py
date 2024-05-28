import cv2
from matplotlib import pyplot as plt

image = cv2.imread(r"C:\src\survival_in_medieval\assets\icons\logo.png",0)

# görseli pyplot arayüzü ile incelemek için bunu kullandık

plt.imshow(image, cmap= "gray", interpolation="bicubic")
plt.xticks([])
plt.yticks([])
plt.show()