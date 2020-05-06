import cv2 as cv
import numpy as np
from Path_Functions import *

image = cv.imread("images/self.jpg")
imageBW = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imageBW = cv.GaussianBlur(imageBW, (9, 9), 0)
canny = cv.Canny(imageBW, 30, 40)

cannyCopy = canny.copy()
contours, hierarchy = cv.findContours(cannyCopy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#create bins for line drawing
imHeight, imWidth = canny.shape
xBins = 10
yBins = 10
bins = [[[] for y in range(yBins)] for x in range(xBins)] #initialize array of lists


#cv.drawContours(image, contours, -1, (0, 255, 0), 2)
#organize contours by cells
contour_count = 0
for contour in contours:
    if contour.size > 1:
        contour_count += 1
        startPoint = contour[0][0]
        xBin = startPoint[0] // (imWidth / xBins)
        yBin = startPoint[1] // (imHeight / yBins)
        bins[int(xBin)][int(yBin)].append(contour)

#starting from closest contour to edge, draw, then look for nearest contour and draw that
curr_contour = find_start_contour(contours, bins, xBins, yBins, imHeight, imWidth)
last_point = tuple(curr_contour[0][0])
curr_bin_ind = (0,0)
while contour_count > 0:
    #draw current contour
    for i, point in enumerate(contour):
        point = tuple(point[0])
        cv.line(image, last_point, point, (0, 255, 0))
        last_point = point
        if i == len(contour) - 1:
            curr_bin = (point[0] // (imWidth / xBins), point[1] // (imHeight / yBins))
    contours.remove(contour)
    contour_count -= 1

    #find next contour by searching nearby bins for closest one
    curr_bin = bins[curr_bin_ind[0]][curr_bin_ind[1]]
    if len(curr_bin) > 0:
        curr_contour = find_nearest(last_point, curr_bin)
    else:
        curr_contour = search_surrounding_bins(last_point)




cv.imshow("start", image)
#cv.imshow("Canny", cannyCopy)
cv.waitKey(0)