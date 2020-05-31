import os
import math
import sys

from cv2 import cv2 as cv
import numpy as np
import pickle

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

# Re-use functions from training.
import training as tng

"""
Module about license plate OCR.
This method is created by myself.
Based on KNN. Is using the classifier trained in training.py script.
"""

mapOfCharacters = { 0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T', 30: 'U', 31: 'V' , 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'}


def knnTest(k, knnTrained, dataTest):
    """
    To validate the assurence of the trained classifier.
    :param knnTrained: knn classifier trained.
    :param dataTest: data to test the trained classifier.
    """
    x_test = []
    for data in dataTest:
        x_test.append(data[0])

    y_pred = knnTrained.predict(x_test)

    print("     + Pred: {class: ", y_pred, ', character: ', mapOfCharacters[y_pred[0]], '}')
    
    return y_pred

if __name__ == '__main__':
    print('[VERSION CV]: ', cv.__version__)

    ## Load trained classifier.
    loaded_model = pickle.load(open('KNN1_Trained.sav', 'rb'))
    # loaded_model = pickle.load(open('KNN3_Trained.sav', 'rb'))

    # [ [[List of Attributes], Class], [[List of Attributes], Class], ... ]
    attributesOfCharacters = [] 

    directoryPath = '../data/FromPlateSegmentation/'
    #directoryPath = '../data/FromPlateDetection&PlateSegmentation/'
    for imagePath in os.listdir(directoryPath):
        print(imagePath)
        original = cv.imread(directoryPath + imagePath)

        ## Process image.
        imageGray, ret, thresh = tng.processImage(original)
                    
        ## Removing unnecessary information.
        characterFit = tng.characterFitAndCentered(thresh)
        heigh, width = characterFit.shape

        # Predict class of a image.
        pred = knnTest(1, loaded_model, [tng.getAttributesAndClass(characterFit)])
        tng.showImages({'Clasificator':thresh})

        # Images with class.
        #characterClass = imagePath.split('.')[0]
        # attributesOfCharacters.append(tng.getAttributesAndClass(characterFit))



