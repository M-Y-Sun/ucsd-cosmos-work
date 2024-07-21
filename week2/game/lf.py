from time import sleep

import cv2 as cv
import picamera
import picamera.array

import include.drive as drive
from include.color import *
from include.corners import *

XRES = 640
YRES = 480
CAM_RES = (XRES, YRES)

camera = picamera.PiCamera()
camera.resolution = CAM_RES
camera.framerate = 32

rawframe = picamera.array.PiRGBArray(camera, size=CAM_RES)

try:
    sleep(1)
    print("[   \033[32;1mOK\033[0m   ] initialized camera")

    while True:
        drive.fwd(50, 50)
        for rframe in camera.capture_continuous(
            rawframe, format="bgr", use_video_port=True
        ):
            frame = rframe.array
            frame = frame[YRES // 3 : YRES // 4, :, :]

            bin = color_thresh(frame, COLOR1_HSV)
            contours, _ = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            centroidx = XRES
            if contours:  # arrow is in the frame, find centroid
                # use the first (biggest/strongest) contour if there are multiple
                mmt = cv.moments(contours[0])
                if mmt["m00"] == 0:
                    rawframe.truncate(0)
                    continue
                centroidx = int(mmt["m10"] / mmt["m00"])

                if centroidx > XRES // 2:
                    drive.fwd(30, 60)
                elif centroidx < XRES // 2:
                    drive.fwd(60, 30)
            else:
                drive.fwd(50, 50)

            cv.circle(frame, (centroidx, YRES // 2), 5, (0, 0, 255), -1)

            cv.imshow("threshold", bin)
            cv.imshow("centroid", frame)
            cv.waitKey(1)

            rawframe.truncate(0)

except KeyboardInterrupt:
    rawframe.truncate(0)
    cv.destroyAllWindows()
    camera.close()
