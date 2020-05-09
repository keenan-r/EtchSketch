import cv2 as cv
import numpy as np
from Path_Functions import *

image = cv.imread("images/self.jpg")
imageBW = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imageBW = cv.GaussianBlur(imageBW, (9, 9), 0)
canny = cv.Canny(imageBW, 30, 40)

cannyCopy = canny.copy()
contours_raw, hierarchy = cv.findContours(cannyCopy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#create bins for line drawing
imHeight, imWidth = canny.shape
xBins = 10
yBins = 10
bins = [[[] for y in range(yBins)] for x in range(xBins)] #initialize array of lists


#cv.drawContours(image, contours, -1, (0, 255, 0), 2)
#organize contours by cells
contour_count = 0
contour_list = []
for contour in contours_raw:
    if contour.size > 2:
        contour_count += 1
        startPoint = contour[0][0]
        xBin = startPoint[0] // (imWidth / xBins)
        yBin = startPoint[1] // (imHeight / yBins)
        curr_contour = []
        # unpack and wrap contours as list of tuples. Makes it easier to handle and allows list removal. Numpy array did not
        for point in contour:
            point = tuple(point[0])
            curr_contour.append(point)
        contour_list.append(curr_contour)
        bins[int(xBin)][int(yBin)].append(curr_contour)

contours = contour_list
#starting from closest contour to edge, draw, then look for nearest contour and draw that
curr_contour = find_start_contour(contours, bins, xBins, yBins, imHeight, imWidth)
last_point = curr_contour[0]
curr_bin_ind = (0,0)
while contour_count > 0:
    #draw current contour
    for i, point in enumerate(curr_contour):
        cv.line(image, last_point, point, (0, 255, 0))
        cv.circle(image, point, 10, (0,0,255))
        #cv.imshow("start", image)
        #cv.waitKey(5)
        last_point = point
        if i == len(contour) - 1:
            curr_bin_ind = (int(point[0] // (imWidth / xBins)), int(point[1] // (imHeight / yBins)))
    try:
        bins[curr_bin_ind[0]][curr_bin_ind[1]].remove(curr_contour)
        contours.remove(curr_contour)
        contour_count -= 1
    except:
        sshhs = 10


    #find next contour by searching nearby bins for closest one
    curr_bin = bins[curr_bin_ind[0]][curr_bin_ind[1]]
    if len(curr_bin) > 0:
        curr_contour = find_nearest(last_point, curr_bin)
    elif contour_count > 0:
        curr_contour = search_surrounding_bins(last_point, curr_bin_ind, bins)




cv.imshow("start", image)
#cv.imshow("Canny", cannyCopy)
cv.waitKey(0)