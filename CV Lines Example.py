import cv2 as cv
import numpy as np

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
for contour in contours:
    if contour.size > 1:
        startPoint = contour[0][0]
        xBin = startPoint[0] // (imWidth / xBins)
        yBin = startPoint[1] // (imHeight / yBins)
        bins[int(xBin)][int(yBin)].append(contour)

lastPoint = (0,0)
#snake through bins
for i in range(xBins * yBins):
    yPos = i // xBins
    xPos = i - (yPos * xBins)
    if yPos % 2 == 1:
        xPos = xBins - xPos
    try:
        for contour in bins[xPos][yPos]:
            for i, point in enumerate(contour):
                point = tuple(point[0])  # extract tuple from ndarray
                cv.line(image, lastPoint, point, (0, 255, 0))
                lastPoint = point
                cv.imshow("start", image)
                #cv.waitKey(1)
    except:
        x = 10
        #TODO: Some cases where xPos = 11, 10



cv.imshow("start", image)
#cv.imshow("Canny", cannyCopy)
cv.waitKey(0)