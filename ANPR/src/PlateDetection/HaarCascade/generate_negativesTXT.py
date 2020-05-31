import os

"""
This module generates negatives.txt file.
This file contains all the names of negatives directory.
"""

f=open('negatives.txt','a')
directoryPath = './negatives/'
for imagePath in os.listdir(directoryPath):
    f.write('negatives/' + imagePath + '\n')

f.close()