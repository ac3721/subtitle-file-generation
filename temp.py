import numpy as np
import cv2

image_path = 'image.png'
img = cv2.imread(image_path)
if img is None:
    raise FileNotFoundError(f"Image not found: {image_path}")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_color = np.array([70, 50, 85])
upper_color = np.array([80, 60, 95])

mask = cv2.inRange(hsv, lower_color, upper_color)
filtered = cv2.bitwise_and(hsv, hsv, mask=mask)

colored_pixels = cv2.countNonZero(mask)
present = colored_pixels > 0

cv2.imshow('HSV', hsv)
cv2.imshow('mask', mask)
cv2.imshow('filtered', filtered)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(f"Colored pixels: {colored_pixels}, Present: {present}")
