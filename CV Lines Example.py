import cv2 as cv
import numpy as np
from Path_Functions import *

image = cv.imread("images/self.jpg")
imageBW = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imageBW = cv.GaussianBlur(imageBW, (9, 9), 0)
canny = cv.Canny(imageBW, 30, 40)

cannyCopy = canny.copy()
contours_raw, hierarchy = cv.findContours(cannyCopy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

imHeight, imWidth = canny.shape

#cv.drawContours(image, contours, -1, (0, 255, 0), 2)
#organize contours by cells
contour_count = 0
contour_list = []
for contour in contours_raw:
    if contour.size > 2:
        curr_contour = []
        # unpack and wrap contours as list of tuples. Makes it easier to handle and allows list removal. Numpy array did not
        for point in contour:
            point = tuple(point[0])
            curr_contour.append(point)
        contour_list.append(curr_contour)


contours = contour_list
#starting from closest contour to edge, draw, then look for nearest contour and draw that
curr_contour = find_start_contour(contours, imHeight, imWidth)
last_point = curr_contour[0]
curr_bin_ind = (0,0)
while len(contours) > 0:
    for i, point in enumerate(curr_contour):
        cv.line(image, last_point, point, (0, 255, 0))
        #cv.circle(image, point, 10, (0,0,255))
        last_point = point
    contours.remove(curr_contour)
    curr_contour = find_nearest(curr_contour, contours)




cv.imshow("start", image)
#cv.imshow("Canny", cannyCopy)
cv.waitKey(0)