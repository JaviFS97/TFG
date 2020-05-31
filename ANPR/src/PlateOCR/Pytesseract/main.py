import os

from cv2 import cv2 as cv
import pytesseract

"""
Module about license plate OCR.
This method is using a Google OCR Classifer named pytesseract.
@author: Javier Fernandez Santos
"""

def processImage(image):
    """
    Process all the images, converting to 1 bit image.
    :param image: to process.
    :return: 
    """
    imageGray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imageGray, 127, 255, cv.THRESH_BINARY)

    return imageGray, ret, thresh

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
    directoryPath = '../data/FromPlateSegmentation/'
    for imagePath in os.listdir(directoryPath):
        original = cv.imread(directoryPath + imagePath)

        ## Process image.
        imageGray, ret, thresh = processImage(original)

        ## Predict class of a image.
        pred = pytesseract.image_to_string(thresh, config='--psm 10')
        
        print('The prediction is: ' + pred)
        showImages({'im': thresh})