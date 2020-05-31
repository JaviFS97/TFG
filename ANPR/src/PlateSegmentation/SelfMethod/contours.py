import os
import math

from cv2 import cv2 as cv
import numpy as np


"""
Module about license plate segmentation.
I don't use anything special because it is the first approach to the problem.
In the next modules, I will use more specifics tools for license plate segmentation.  
It's based on Connect Component Analysis (CCA) and finding possibleChars.
"""

shapeRectangle = None
shapeSquare = None
counter = 0


def processImage(image):
    """
    Process all the images, converting to 2 bit image.
    :param image: to process.
    :return: 
    """
    imageGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # edges = cv.Canny(imageGray,100,200)
    # ret, thresh = cv.threshold(edges, 127, 255, cv.THRESH_BINARY)

    ret, thresh = cv.threshold(imageGray, 127, 255, cv.THRESH_BINARY)
    img, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return imageGray, ret, thresh, contours, hierarchy


def writeImage(image, savePath):
    """
    Use the function cv.imwrite() to save an image.
    :param image: the file name.
    :param savePath: path to save image.
    """
    cv.imwrite(savePath, image)


def showImages(images):
    """
    Shows all the images and wait until press one key.
    :param images: map with the title of the image and the image.
    """
    for title, image in images.items():
        cv.imshow(title, image)

    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()


def drawContours(srcImage, contours):
    """
    Prints in the original image all the interesting contours that was found.
    :param srcImage: 
    :param contours: to print.
    """
    contourID = -1      # Print all contours
    color = (255,60,0)   # Blue
    thickness = 2
    cv.drawContours(srcImage, contours, contourID, color, thickness)


def drawRectangleInContours(srcImage, contours):
    """
    Prints in the original image all the interesting contours that was found with a rectangle.
    :param srcImage: 
    :param contours: to print.
    """
    for cnt in contours:
        x,y,w,h = cv.boundingRect(cnt)
        color = (0,255,0)   # Green rectangle
        thickness = 2
        cv.rectangle(srcImage,(x,y),(x+w,y+h), color, thickness)

        # drawContours(srcImage, contours)
        cropImage(srcImage, cnt)


def cropImage(srcImage, contour):
    """
    Crop the image from top left corner to bottom right corner.
    :param srcImage: to crop.
    :param contour: to crop.
    """
    global counter
    minX, minY, maxX, maxY = searchCorners(contour)
    ROI = srcImage[minY:maxY, minX:maxX]
    cv.imshow('ROI', ROI)
    #writeImage(ROI, '../../PlateOCR/data/FromPlateSegmentation/' + str(counter) + '.png')
    #writeImage(ROI, '../../PlateOCR/data/FromPlateDetection&PlateSegmentation/' + str(counter) + '.png')
    counter+=1


def searchCorners(contour):
    """
    Find top left corner (minX, minY) and bottom right corner (maxX, maxY)
    :param contour: coordenates of the lines of the contour.
    """
    minX = np.amin(contour, axis=0)[0][0]
    minY = np.amin(contour, axis=0)[0][1]
    maxX = np.amax(contour, axis=0)[0][0]
    maxY = np.amax(contour, axis=0)[0][1]

    return minX, minY, maxX, maxY


def contourPerimeter(contour):
    """
    Calculates the perimeter of a contour
    :param contour: to calculates the perimeter.
    :return: 
    """
    closedContour = True
    perimeter = cv.arcLength(contour, closedContour)
    return perimeter


def findingPossibleChars(contours):
    """
    Search for the contours of greatest interest.
    :param contours: that was found.
    :return: 
    """
    interestingContours = []
    for contour in contours:
        if isPossibleChar(contour):
            interestingContours.append(contour)

    return interestingContours


def isPossibleChar(contour):
    """
    With the contour determines if it is a character.
    :params contour: that was found.
    """
    MIN_WIDTH = 15
    MAX_WIDTH = 80
    MIN_HEIGHT = 30 
    MAX_HEIGHT = 80
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = float(w)/float(h)
    area = w * h
    perimeter = contourPerimeter(contour)
    diagonal = math.sqrt(w*w + h*h)

    if w > MIN_WIDTH and w < MAX_WIDTH and h > MIN_HEIGHT and h < MAX_HEIGHT:
        return True
    return False


if __name__ == '__main__':
    print('[VERSION CV]: ', cv.__version__)

    ## Each image with car plate.
    directoryPath = '../../../Dataset/Plates/Internet/'
    for imagePath in os.listdir(directoryPath):
        original = cv.imread(directoryPath + imagePath)

        ## Resize original image.
        #original = cv.resize(original, (300, 150), interpolation = cv.INTER_AREA)

        ## Processing image.
        imageGray, ret, thresh, originalContours, hierarchy = processImage(original)

        ## Finding possible characters.
        interestingContours = findingPossibleChars(originalContours)

        ## Painting rectangle on possigle characters.
        drawRectangleInContours(original, interestingContours)

        ## Show some info about contours of the image.
        print('[INFO] New contorous list size: ' + str(len(interestingContours)) + ', Old contorous list size: ' + str(len(originalContours)))
        
        showImages({'thresh': thresh,
                    'original': original})