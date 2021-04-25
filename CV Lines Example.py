import cv2 as cv
import numpy as np
from Path_Functions import *
import pickle
import Graph_Connector

image = cv.imread("images/2square.jpg")
imageBW = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imageBW = cv.GaussianBlur(imageBW, (9, 9), 0)
canny = cv.Canny(imageBW, 30, 40)

cannyCopy = canny.copy()
contours_raw, hierarchy = cv.findContours(cannyCopy, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

imHeight, imWidth = canny.shape
blank = np.zeros((imHeight,imWidth,3), np.uint8)

cv.drawContours(image, contours_raw, -1, (0, 255, 0), 2)
cv.imshow("start", image)
cv.waitKey(0)

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
point_list = []
#need to get a list of points to travel

connector = Graph_Connector.PathConnector(contours)


for path in connector.path_line_list:
    last_point = path.line[0]
    for point in enumerate(path.line, start=2):
        point = point[1]
        cv.line(blank, last_point, point, (0, 255, 0))
        last_point = point
    try:
        cv.line(blank, path.this_closest_point, path.closest_line_point, (255, 0, 0))
    except:
        x = 1

#remove lines that are small to speed up execution on etch
#limit = 2
#last_point = point_list[0]
#for point in point_list:
#    if point != last_point:
#        if point_dist(last_point, point) < limit:
#            point_list.remove(point)
#        else:
#            cv.line(blank, last_point, point, (0, 255, 0))
#            last_point = point



with open("points.txt", "wb") as fp:
    pickle.dump(point_list, fp)

cv.imshow("start", image)
cv.imshow("blank", blank)
cv.imshow("Canny", cannyCopy)
cv.waitKey(0)