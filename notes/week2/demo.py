import time

import cv2 as cv
import numpy as np

img = cv.imread("demo_img.jpg")

cv.imshow("original img", img)
cv.waitKey()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("grayscale", gray)
cv.waitKey()

_, bin = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

contours, hierarchy = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
for c in contours:
    M = cv.moments(c)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    cv.circle(bin, (cx, cy), 3, (0, 0, 255))

cv.destroyAllWindows()
