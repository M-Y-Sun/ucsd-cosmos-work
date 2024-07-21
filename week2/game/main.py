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
camera.framerate = 60

rawframe = picamera.array.PiRGBArray(camera, size=CAM_RES)

try:
    sleep(1)
    print("[   \033[32;1mOK\033[0m   ] initialized camera")

    direc = Dir.RT  # turn right at the beginning of the program
    curcolor = COLOR1_HSV  # start with color1 (orange/red)
    while True:
        print("curcolor: ", curcolor)

        # turn to the arrow
        # if direc == Dir.LT:
        #     drive.fwd(25, 0)
        # else:
        #     drive.fwd(0, 25)

        arrowpic = None
        for rframe in camera.capture_continuous(
            rawframe, format="bgr", use_video_port=True
        ):
            frame = rframe.array

            if direc == Dir.LT:
                drive.fwd(40, -40)
            else:
                drive.fwd(-40, 40)

            sleep(0.2)
            drive.stop()

            bin = color_thresh(frame, curcolor)
            contours, _ = cv.findContours(bin, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            centroidx = XRES
            if contours:  # arrow is in the frame, find centroid
                # use the first (biggest/strongest) contour if there are multiple
                mmt = cv.moments(contours[0])
                if mmt["m00"] == 0:
                    rawframe.truncate(0)
                    continue
                centroidx = int(mmt["m10"] / mmt["m00"])

                if centroidx > XRES / 2 - 40 and centroidx < XRES / 2 + 40:
                    rawframe.truncate(0)
                    print("centroid near center, break loop")
                    break

            else:  # blank frame (no arrow), set centroid to edge
                if direc == Dir.LT:
                    centroidx = 0

            # dist * 80 / res + 40
            dist = abs(centroidx - XRES / 2)
            drive.PWMA.ChangeDutyCycle(40 * dist / XRES + 20)
            drive.PWMB.ChangeDutyCycle(40 * dist / XRES + 20)

            cv.circle(frame, (centroidx, YRES // 2), 5, (0, 0, 255), -1)

            # drive.stop()
            # sleep(0.5)

            cv.imshow("threshold", bin)
            cv.imshow("centroid", frame)
            cv.waitKey(1)

            rawframe.truncate(0)

        cv.destroyAllWindows()

        # move forward until close enough
        drive.fwd(40, 40)
        for rframe in camera.capture_continuous(
            rawframe, format="bgr", use_video_port=True
        ):
            frame = rframe.array

            bin = color_thresh(frame, curcolor)
            # subframe = bin[
            #     int(YRES * 0.45) : int(YRES * 0.55), int(YRES * 0.4) : int(YRES * 0.6)
            # ]
            # if np.all(subframe):
            if np.count_nonzero(bin) > XRES * YRES // 20:
                arrowpic = bin
                print("close enough, break loop")
                rawframe.truncate(0)
                break

            cv.imshow("frame", frame)
            cv.imshow("threshold", bin)
            cv.waitKey(1)

            rawframe.truncate(0)

        # get direction of the arrow
        direc = getdir(arrowpic)

        # filter again
        curcolor = COLOR2_HSV if curcolor == COLOR1_HSV else COLOR1_HSV

        cv.destroyAllWindows()


except KeyboardInterrupt:
    rawframe.truncate(0)
    cv.destroyAllWindows()
    camera.close()
