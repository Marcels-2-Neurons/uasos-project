# cvlib.py>
# Library used for OpenCV integration, are just custom functions
# Imported where necessary
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

import cv2 as cv


# function for just having in one command the sample photo
def lena():
    img = cv.imread(cv.samples.findFile("lena.jpg"))
    return img

