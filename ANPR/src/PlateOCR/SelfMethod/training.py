import os
import math
import time
import sys
import random

from cv2 import cv2 as cv
import numpy as np
import pickle

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

"""
Module about license plate OCR.
This method is created by myself.
My method creates a grid in each image obtained from the previous step. 
In this way, we generate for each photo x * x attributes.
These attributes are passed to the KNN classifier to be trained.
"""

## Configuration options.
np.set_printoptions(threshold=sys.maxsize)
Macro_Debug = False

mapOfCharacters = { '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15, 'G':16, 'H':17, 'I': 18, 'J': 19, 'K':20, 'L':21, 'M':22, 'N': 23, 'O':24, 'P':25, 'Q':26, 'R':27, 'S': 28, 'T':29, 'U':30, 'V':31 , 'W':32, 'X':33, 'Y':34, 'Z':35}


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


def removingWhiteRegions(thresh):
    """
    Removed white regions.
    I guess a region is white while most of its pixels are. (White pixel = 255, Black picel = 0).
    :param thresh: character thresh.
    """
    thresholding = 250

    significantRows = []
    for row in thresh:
        # print(type(row), sum(row), np.mean(row))
        if np.mean(row) < thresholding:
            significantRows.append(row) 

    return np.asarray(significantRows)


def characterFitAndCentered(thresh):
    """
    Received a character with white margins an return a character centered without white margins.
    :param thresh: character thresh.
    """
    # Delete white rows regions 
    threshWithOutWhiteRegions = removingWhiteRegions(thresh)

    # Delete white cols regions 
    threshTranspose = threshWithOutWhiteRegions.transpose() # Doing transpose
    threshWithOutWhiteRegionsTranspose = removingWhiteRegions(threshTranspose)

    # Return to original orientation
    characterFit = threshWithOutWhiteRegionsTranspose.transpose()

    if Macro_Debug:
        showImages({'[1.1] - thresh': thresh})
        showImages({'[1.2] - threshWithOutWhiteRegions': threshWithOutWhiteRegions})
        showImages({'[2.1] - threshTranspose': threshTranspose})
        showImages({'[2.2] - threshWithOutWhiteRegionsTranspose': threshWithOutWhiteRegionsTranspose})
        showImages({'[3] - characterFitAndCentered': characterFit})

    return characterFit


def intervals(characterFit):
    """
    Calculate the intervals according to a height and width.
    :param characterFit: character centered without white regions.
    """
    # 7 points to generate 6 intervals => 6intervalsRow * 6intervalsCol == 36 attributes/character.
    numberOfPoints = 7

    # Getting heigh and width to create intervals.
    heigh, width = characterFit.shape
    rowDivision = np.array(np.linspace(0,heigh, numberOfPoints), dtype=int)
    colDivision = np.array(np.linspace(0,width, numberOfPoints), dtype=int)
    if Macro_Debug:
        print('         # ', width, heigh, rowDivision, colDivision)

    return rowDivision, colDivision


def getAttributesAndClass(characterFit, classOfCharacter=None):
    """
    Return a list of [[List of Attributes], Class] to train KNN classifier.
    :param characterFit: character centered without white regions.
    :param classOfCharacter: the class of the character.
    """
    global mapOfCharacters
    rowDivision, colDivision = intervals(characterFit)

    attributesOfCharacter = []
    for x in range(len(rowDivision)-1):
        for y in range(len(colDivision)-1):
            attribute = characterFit[rowDivision[x]:rowDivision[x + 1], colDivision[y]:colDivision[y + 1]]
            assert len(attribute) != 0
            # Because attributes have different shapes.
            meanValue = np.mean(attribute)
            attributesOfCharacter.append(meanValue)
            if Macro_Debug:
                print('         - meanValue of [(' + str(rowDivision[x]) + ',' + str(rowDivision[x+1]) + '),(' + str(colDivision[y]) + ',' + str(colDivision[y+1]) + ')]: ', meanValue)
                showImages({'Attribute': attribute})


    # [[List of Attributes], Class]
    attributesAndClassOfCharacter = []
    attributesAndClassOfCharacter.append(attributesOfCharacter)
    if classOfCharacter != None:
        attributesAndClassOfCharacter.append(mapOfCharacters[classOfCharacter])

    if Macro_Debug:
        print(attributesAndClassOfCharacter)

    return attributesAndClassOfCharacter


def errores(yTest, yPred):
    """
    Compare the predictions made with the chosen classifier with the real classes, to calculate the error rate.
    : param yTest: real classes. 
    :param yPred: preditction classes
    """

    num_data = 0
    fail_ok = []
    ok = 0
    fail = 0

    for data in yTest:
        if data == yPred[num_data]:
            ok += 1
        else:
            fail += 1

        num_data += 1

    fail_ok.append(fail)
    fail_ok.append(ok)
    rate_fail = fail / (ok+fail)
    rate_ok = 1.0 - rate_fail

    print("     - [FAIL, OK]:" + str(fail_ok) + ", Rate of success: " + str(rate_ok*100) + "%")


def saveKNN(k, model):
    """
    Saving trained classifier to disk for later predict data.
    :param k: number of neighbors.
    :param model: classifier trained.
    """
    filename = 'KNN' + str(k) + '_Trained.sav'
    pickle.dump(model, open(filename, 'wb'))


def knnTrain(k, dataTrain):
    """
    Train the classifier.
    :param k: number of k neighbors.
    :param dataTrain: data to train the classifier. 
    """

    x_train = []
    y_train = [] 
    for data in dataTrain:
        x_train.append(data[0])
        y_train.append(data[1])

    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(x_train, y_train)

    return knn


def plotConfusionMatrix(confusionMatrix, target_names,
                          title='Confusion matrix',
                          normalize=False):
    import seaborn as sn
    import pandas as pd
    import matplotlib.pyplot as plt

    df_cm = pd.DataFrame(confusionMatrix, index = [i for i in target_names],
                  columns = [i for i in target_names])
    sn.set(font_scale=0.7)#for label size                  
    fig = plt.figure(figsize = (15,10))
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 5})    
    fig.suptitle('Confusion Matrix', fontsize=20)
    plt.show()


def knnTest(k, knnTrained, dataTest):
    """
    To validate the assurence of the trained classifier.
    :param knnTrained: knn classifier trained.
    :param dataTest: data to test the trained classifier.
    """
    x_test = []
    y_test = [] 
    for data in dataTest:
        x_test.append(data[0])
        y_test.append(data[1])

    y_pred = knnTrained.predict(x_test)
    print("     + Number of neighbors (k): ",k)
    errores(y_test, y_pred)
    print("     - Confusion matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    plotConfusionMatrix(cm, mapOfCharacters.keys())


if __name__ == '__main__':
    start_time = time.time()
    print('[VERSION CV]: ', cv.__version__)

    ## [ [[List of Attributes], Class], [[List of Attributes], Class], ... ]
    ## Each image has --> [ [List of Attributes], Class ]
    attributesOfCharacters = [] 
    numberOfCharacters = 0

    directoryOfCharacters = '../../../Dataset/Characters/'
    for character in os.listdir(directoryOfCharacters):
        print( ' + ', character)
        ## For each character type (eg. 'A')
        for imagePath in os.listdir(directoryOfCharacters + character + '/'):
            original = cv.imread(directoryOfCharacters + character + '/' + imagePath)

            ## Processing image.
            imageGray, ret, thresh = processImage(original)
                        
            ## Removing unnecessary information.
            characterFit = characterFitAndCentered(thresh)

            ## Getting attributes of image and adding to the 'attributesOfCharacters' list 
            heigh, width = characterFit.shape
            if heigh > 70 and width > 50:
                attributesOfCharacters.append(getAttributesAndClass(characterFit, character))
        
        numberOfCharacters += 1

    
    print("--- %s seconds processing all the images ---" % (time.time() - start_time))
    start_time = time.time()
        
    ## Shuffle all the images.
    random.shuffle(attributesOfCharacters)

    ## Dividing dataset in two datasets (for training and for testing)
    numberOfImages = len(attributesOfCharacters)
    print('Number of images' + str(numberOfImages))
    dataTrain = attributesOfCharacters[:int(numberOfImages*0.8)]
    dataTest = attributesOfCharacters[int(numberOfImages*0.8):]

    ## Applying KNN with 1,3 and 5 neighbors.
    for k in [1,3,5]:
        knnTrained = knnTrain(k, dataTrain)
        knnTest(k, knnTrained, dataTest)

        ## Saving classifier on a file.
        saveKNN(k, knnTrained)
    print("--- %s seconds trainning and testing ---" % (time.time() - start_time))