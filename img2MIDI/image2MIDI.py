import cv2

img = cv2.imread('Amily.jpeg')
cv2.imshow('output', img)
cv2.waitKey(2000)
cv2.destroyAllWindows()
