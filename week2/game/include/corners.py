import cv2 as cv
import numpy as np
from color import *


def getcorners(img):
    bin = img.copy()
    cv.imshow("threshold", bin)
    cv.waitKey()

    bin = cv.medianBlur(bin, 5)
    cv.imshow("blurred", bin)
    cv.waitKey()

    # shi-tomasi
    corners = cv.goodFeaturesToTrack(bin, 3, 0.2, 40, blockSize=11)

    arr = np.empty((3, 2))
    it = 0
    for i in corners:
        x, y = i.ravel()
        arr[it][0] = x
        arr[it][1] = y
        it += 1

    return arr


def getdir(img):
    corners = getcorners(img)
    assert corners.shape == (3, 2)

    xmax, _ = (np.max(corners, axis=0)).ravel()

    # arrow is guarenteed to be horizontal
    bool_arr = corners[:, 0] > xmax - 10
    if np.count_nonzero(bool_arr) == 2:
        return Dir.LT
    else:
        return Dir.RT


def test(path, clr):
    inp = cv.imread(path)
    cv.imshow("original image", inp)
    cv.waitKey()

    bin = color_thresh(inp, clr)
    corners = getcorners(bin)

    inp_clone = inp.copy()
    for coord in corners:
        # print(coord)
        cv.circle(inp_clone, (int(coord[0]), int(coord[1])), 6, (0, 0, 255), -1)

    cv.imshow("processed image", inp_clone)
    cv.waitKey()

    direc = getdir(bin)
    if direc == direc.LT:
        print("left")
    else:
        print("right")

    contours, _ = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    mmt = cv.moments(contours)
    centroid = (int(mmt["m10"] / mmt["m00"]), int(mmt["m01"] / mmt["m00"]))
    bin = cv.cvtColor(bin, cv.COLOR_GRAY2BGR)
    cv.circle(bin, centroid, 6, (0, 0, 255), -1)
    cv.imshow("centroid", bin)
    cv.waitKey()

    cv.destroyAllWindows()


test("imgs/sticky1.jpg", (5, 130, 230))
# test("imgs/sticky2.jpg", (100, 150, 70))

# test("imgs/arrow1.jpg")
# test("imgs/arrow2.jpg")
# test("imgs/arrow3.jpg")
# test("imgs/arrow4.jpg")
