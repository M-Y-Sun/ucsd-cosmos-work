import cv2 as cv

img = cv.cvtColor(cv.imread("2cnts.jpg"), cv.COLOR_BGR2GRAY)
_, img = cv.threshold(img, 127, 255, 0)

contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

img_clr = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
it = 0
for c in contours:
    cv.drawContours(img_clr, contours, it, (0, 255 - it * 30, 0), 3)
    print(f"\ncontour {it}:\n{c}")
    it += 1

print("\nhierarchy (RETR_EXTERNAL):\n", hierarchy)

_, hierarchy = cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print("\nhierarchy (RETR_LIST):\n", hierarchy)

_, hierarchy = cv.findContours(img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
print("\nhierarchy (RETR_CCOMP):\n", hierarchy)

_, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
print("\nhierarchy (RETR_TREE):\n", hierarchy)

cv.imshow("image", img_clr)
cv.waitKey()
