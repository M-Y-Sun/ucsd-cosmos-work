from enum import Enum

import cv2 as cv
import numpy as np

COLOR1_HSV = (5, 130, 230)  # orange-red
# COLOR2_HSV = (205, 160, 220)  # blue
COLOR2_HSV = (95, 200, 160)


class Dir(Enum):
    LT = 0
    RT = 1


def color_thresh(img_bgr, hsv_clr):
    cln = img_bgr.copy()
    cln = cv.GaussianBlur(cln, (7, 7), sigmaX=0, sigmaY=0)
    cln = cv.cvtColor(cln, cv.COLOR_BGR2HSV)

    h, s, v = hsv_clr
    lct = np.array([max(h - 20, 0), s - 90, v - 80])
    uct = np.array([min(h + 20, 255), 255, 255])

    return cv.inRange(cln, lct, uct)
