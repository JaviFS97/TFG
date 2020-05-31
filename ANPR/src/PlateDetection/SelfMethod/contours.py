import os

from cv2 import cv2 as cv
import numpy as np


"""
Module about license plate detection.
I don't use anything special because it is the first approach to the problem.
In the next modules, I will use more specifics tools for license plate detection.  
It's based on Connect Component Analysis (CCA), shape matching, aspect ratio and perimeter.
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
    writeImage(ROI, '../../PlateSegmentation/data/FromPlateDetection/' + str(counter) + '.png')
    cv.imshow('ROI', ROI)


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


def extremePoints(cnt):
    """
    Find extreme points of a contour.    
    :param cnt: to find extreme points.
    :return:
    """
    leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
    rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])

    return leftmost, rightmost, topmost, bottommost


def contourPerimeter(contour):
    """
    Calculates the perimeter of a contour
    :param contour: to calculates the perimeter.
    :return: 
    """
    closedContour = True
    perimeter = cv.arcLength(contour, closedContour)
    return perimeter


def findingInterestingContours(contours):
    """
    Search for the contours of greatest interest.
    :param contours: that was found.
    :return: 
    """
    interestingContours = []
    print('[INFO] Possible plates: ')
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        aspect_ratio = float(w)/h
        perimeter = contourPerimeter(contour)
        if isRectanglePlate(aspect_ratio, perimeter, contour) or isSquarePlate(aspect_ratio, perimeter, contour):
            interestingContours.append(contour)

    return interestingContours
 

def isRectanglePlate(aspect_ratio, perimeter, contour):
    global shapeRectangle

    if 3.5 < aspect_ratio < 8.0 and 450 < perimeter < 1000:
        match = similarShape(contour, shapeRectangle)
        print(' + Rectangle: aspect_ratio->', aspect_ratio, ' perimeter->', perimeter, ' shape->', match)
        if match < 0.7:
            return True
    return False


def isSquarePlate(aspect_ratio, perimeter, contour):
    global shapeSquare

    if 1.0 < aspect_ratio < 1.5 and 300 < perimeter < 500:
        match = similarShape(contour, shapeSquare)
        print(' + Square:    aspect_ratio->', aspect_ratio, ' perimeter->', perimeter, ' shape->', match)
        if match < 0.4:
            return True
    return False


def similarShape(contour, shape):
    """
    Compares the shape of contour with plate shape.
    :param contour: one of all contours. 
    :param shape: of the plate.
    """
    comparisonMethod = 2
    match = cv.matchShapes(contour, shape, comparisonMethod, 1)

    return match


if __name__ == '__main__':
    print('[VERSION CV]: ', cv.__version__)

    ## Taking shape of rectangle plate for matchShapes.
    plateShapeRectangle = cv.imread('./plateShapes/Plate-Shape-Rectangle.png')
    imageGray, ret, thresh, shapeRectangleContours, hierarchy = processImage(plateShapeRectangle)
    drawContours(plateShapeRectangle, shapeRectangleContours)

    ## Taking shape of square plate for matchShapes.
    plateShapeSquare = cv.imread('./plateShapes/Plate-Shape-Square.png')
    imageGray, ret, thresh, shapeSquareContours, hierarchy = processImage(plateShapeSquare)
    drawContours(plateShapeSquare, shapeSquareContours)

    ## Global values.
    shapeRectangle = shapeRectangleContours[0]
    shapeSquare = shapeSquareContours[0]

    ## Each image with car plate.
    directoryPath = '../../../Dataset/Cars/Sample/'
    for imagePath in os.listdir(directoryPath):
        original = cv.imread(directoryPath + imagePath)

        ## Resize image.
        # original = cv.resize(original, (640, 480), interpolation = cv.INTER_AREA)

        ## Process image.
        imageGray, ret, thresh, originalContours, hierarchy = processImage(original)
        print('[INFO] Total size of contorous list: ' + str(len(originalContours)))
        ## Finding contours.
        interestingContours = findingInterestingContours(originalContours)
        drawRectangleInContours(original, interestingContours)

        ## Show some info about contours of the image.
        print('[INFO] Final size of contorous list: ' + str(len(interestingContours)) )
        showImages({'plateShapeRectangle': plateShapeRectangle,
                    'plateShapeSquare': plateShapeSquare,
                    'thresh': thresh,
                    'original': original})

        counter += 1