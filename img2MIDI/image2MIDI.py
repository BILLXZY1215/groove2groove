import cv2
from PIL import Image
import numpy as np
import pretty_midi

# img = cv2.imread('Amily.jpeg')
# cv2.imshow('output', img)
# cv2.waitKey(2000)
# cv2.destroyAllWindows()

img = np.array(Image.open('Amily.jpeg'))  # RGB Matrix
img = cv2.resize(img, (224, 224))
print(img)
