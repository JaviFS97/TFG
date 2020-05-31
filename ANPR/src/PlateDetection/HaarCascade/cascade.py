import os

import numpy as np
from cv2 import cv2 as cv


"""
This module is about plate detection.
This module is using the classifier Haar Cascade. 
Haar Cascade is a classifer that train with a lot of positives and negatives images. 
After trained, it creates a file with extension 'xml'. That file is the classifier. 
I use this classifier in this file.
"""


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


def showImages(images):
    """
    Shows all the images and wait until press one key.
    :param images: map with the title of the image and the image.
    """
    for title, image in images.items():
        cv.imshow(title, image)

    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()



if __name__ == '__main__':
    
    ## Load the classifier.
    # plate_cascade = cv.CascadeClassifier('./classifiers/haarcascade_russian_plate_number.xml')
    plate_cascade = cv.CascadeClassifier('./classifiers/own/HAAR/cascade.xml')

    directoryPath = '../../../Dataset/Cars/Sample/'
    for imagePath in os.listdir(directoryPath):
        img = cv.imread(directoryPath + imagePath)

        imageGray, ret, thresh, contours, hierarchy = processImage(img)

        ## Using classifier.
        plates = plate_cascade.detectMultiScale(imageGray, 1.01, 7)

        ## Painting a rectangle on the license plates found.
        for (x,y,w,h) in plates:
            img = cv.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        ## Showing this image with rectangle.
        showImages({'img': img})
