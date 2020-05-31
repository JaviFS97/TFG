import os
from cv2 import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


directoryPath = '../../../Dataset/Cars/baza_slika/A/'
for imagePath in os.listdir(directoryPath):
    img = cv.imread(directoryPath + imagePath)
    # Initiate ORB detector
    orb = cv.ORB_create()
    # find the keypoints with ORB
    kp = orb.detect(img,None)
    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)
    # draw only keypoints location,not size and orientation
    img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)

    cv.imshow('title', img2)

    if cv.waitKey(0) & 0xff == 27:
        cv.destroyAllWindows()
