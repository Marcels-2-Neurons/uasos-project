# mathandler.py>
# Library used for handling .mat file from NORB Dataset
# Imported in stimuli as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
global NORBd
import numpy as np
import mat73 as mat
import imgtreat as imt
from scipy import io
from PIL import Image

# Initialize NORB Dataset
class NORB:
    def __init__(self):
        print('Loading Mat Libs...')
        self.imgs = mat.loadmat('.\imgs\mat_im_10.mat')
        self.keys = list(self.imgs.keys())
        self.cat = io.loadmat('.\imgs\mat_cat_10.mat')
        print('Loading Done')

    def imghandler(self, no_img=1, gaussian=0, saltpepper=0, poisson=0, speckle=0, blur=0,
                   lowcontrast=0, bars=0, vignette=0, tearing=0):
        # Retrieve img_handler by passing all the parameters
        imgHandler = self.imgs[self.keys[0]][no_img].astype(np.uint8)
        # Filter Application
        if gaussian != 0: # Default: 0.5
            imgHandler = imt.gaussiannoise(imgHandler, gaussian)
        elif saltpepper != 0: # Default: 0.2
            imgHandler = imt.saltpeppernoise(imgHandler, saltpepper)
        elif poisson != 0: # Default 1
            imgHandler = imt.poissonnoise(imgHandler, poisson)
        elif speckle != 0:  # Default 0.1
            imgHandler = imt.specklenoise(imgHandler, speckle)
        elif blur != 0:  # Default 0.4
            imgHandler = imt.blur(imgHandler, blur)
        elif lowcontrast != 0: # Default 1 ON/OFF
            imgHandler = imt.lowcontrast(imgHandler, lowcontrast)
        elif bars != 0: # Default 0.85
            imgHandler = imt.bars(imgHandler, bars)
        elif vignette != 0:  # Default 1 ON/OFF
            imgHandler = imt.vignette(imgHandler, vignette)
        elif tearing != 0:  # Default 1 ON/OFF
            imgHandler = imt.tearing(imgHandler)

        imgHandler = np.flipud((imgHandler / 255)*2 - 1.0)  # Image Matrix Normalization
        return imgHandler

NORBd = NORB()