import cv2 as cv
import numpy as np

class ImageProcessor:

    def __init__(self, filepath):
        self.rawImage = cv.imread(filepath)
        self.preprocessedImage = self.preprocessImage()
        self.contours = self.getContours()
        self.contouredImage = self.createContourImage()

    def preprocessImage(self):
        imgCopy = self.rawImage.copy()
        imgProcessed = cv.cvtColor(imgCopy, cv.COLOR_BGR2GRAY)
        imgProcessed = cv.GaussianBlur(imgProcessed, (9, 9), 0)
        return imgProcessed

    def getContours(self):
        imgCopy = self.rawImage.copy()
        imgProcessed = cv.cvtColor(imgCopy, cv.COLOR_BGR2GRAY)
        imgProcessed = cv.GaussianBlur(imgProcessed, (9,9), 0)
        canny = cv.Canny(imgProcessed, 30, 40)

        imageCannyCopy = canny.copy()
        contours_raw, hierarchy = cv.findContours(imageCannyCopy, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        return contours_raw

    def createContourImage(self):
        contourImage = self.rawImage.copy()
        cv.drawContours(contourImage, self.contours, -1, (0, 255, 0), 2)
        return contourImage

    def showRaw(self):
        cv.imshow("start", self.rawImage)
        cv.waitKey(0)


    def showImgWithContours(self):
        cv.imshow("Contoured Image", self.contouredImage)
        cv.waitKey(0)

myImage = ImageProcessor("images/self.jpg")
myImage.showImgWithContours()
