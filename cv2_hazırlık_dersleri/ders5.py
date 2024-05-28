import cv2
import numpy as np

# siyah arkaplan
img = np.zeros((512,512,3), np.uint8)
cv2.imshow("siyah ekran", img)

#siyah arka plana çizgi çizme
img2 = cv2.line(img, (23,44), (124,124),(0,0,185),4)
cv2.imshow("cizgili",img2)

cv2.waitKey(0)
cv2.destroyAllWindows()