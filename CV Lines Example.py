import cv2 as cv
import numpy as np
from Path_Functions import *
import pickle

image = cv.imread("images/alex.jpg")
imageBW = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imageBW = cv.GaussianBlur(imageBW, (9, 9), 0)
canny = cv.Canny(imageBW, 30, 40)

cannyCopy = canny.copy()
contours_raw, hierarchy = cv.findContours(cannyCopy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

imHeight, imWidth = canny.shape
blank = np.zeros((imHeight,imWidth,3), np.uint8)

#cv.drawContours(image, contours, -1, (0, 255, 0), 2)

#reformat contour array
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


#pathfinding
contours = contour_list
curr_contour = find_start_contour(contours, imHeight, imWidth)
last_point = curr_contour[0]
curr_bin_ind = (0,0)
ordered_lines = []
point_list = []
while len(contours) > 0:
    for i, point in enumerate(curr_contour):
        cv.line(image, last_point, point, (0, 255, 0))
        point_list.append(point)
        last_point = point
    ordered_lines.append(curr_contour)
    #definitely need a better way of doing this, but if contour gets reversed need to still remove
    try:
        contours.remove(curr_contour)
    except:
        contours.remove(list(reversed(curr_contour)))
    curr_contour = find_nearest(curr_contour, contours)

#remove lines that are small to speed up execution on etch
limit = 4
last_point = point_list[0]
for point in point_list:
    if point != last_point:
        if point_dist(last_point, point) < limit:
            point_list.remove(point)
        else:
            cv.line(blank, last_point, point, (0, 255, 0))
            last_point = point



with open("points.txt", "wb") as fp:
    pickle.dump(point_list, fp)

cv.imshow("start", image)
cv.imshow("blank", blank)
#cv.imshow("Canny", cannyCopy)
cv.waitKey(0)