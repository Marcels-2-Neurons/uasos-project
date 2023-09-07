# mathandler.py>
# Library used for handling .mat file from NORB Dataset
# Imported in stimuli as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

import numpy as np
# import mat73 as mat
import imgtreat as imt
from scipy import io
import time

global NORBd

# Still to implement:
# A new NORB dataset with balanced no. of images for each case

# Initialize NORB Dataset


class NORB:
    def __init__(self):
        print('Loading Mat Libs...')
        s_time = time.time()
        self.imgs = io.loadmat('.\imgs\mat_im_10_cut.mat')
        self.ikeys = list(self.imgs.keys())
        self.cat = io.loadmat('.\imgs\mat_cat_10_cut.mat')
        self.ckeys = list(self.cat.keys())
        print('Loading Done in', "%.2f" % (time.time() - s_time), ' sec')

    def imghandler(self, no_img=1, gaussian=0, saltpepper=0, poisson=0, speckle=0, blur=0, tearing=0, mpeg=0):
        # Retrieve img_handler by passing all the parameters
        imgHandler = self.imgs[self.ikeys[3]][0, no_img].astype(
            np.uint8)  # the name of the variable now is in the 4th position (3)
        # Filter Application
        if gaussian != 0:  # Default: 0.5
            imgHandler = imt.gaussiannoise(imgHandler, gaussian)
        elif saltpepper != 0:  # Default: 0.2
            imgHandler = imt.saltpeppernoise(imgHandler, saltpepper)
        elif poisson != 0:  # Default 1
            imgHandler = imt.poissonnoise(imgHandler, poisson)
        elif speckle != 0:  # Default 0.1
            imgHandler = imt.specklenoise(imgHandler, speckle)
        elif blur != 0:  # Default 0.4
            imgHandler = imt.blur(imgHandler, blur)
        elif tearing != 0:  # Default 1 ON/OFF
            imgHandler = imt.tearing(imgHandler)
        elif mpeg != 0:  # Default 1 ON/OFF
            imgHandler = imt.mpeg_pixel(imgHandler)

        imgHandler = np.flipud((imgHandler / 255) * 2 - 1.0)  # Image Matrix Normalization
        return imgHandler

    def get_cat(self, no_img):
        # retrieve value from mat_cat
        return self.cat[self.ckeys[3]][no_img].astype(str)


NORBd = NORB()
