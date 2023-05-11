# mathandler.py>
# Library used for handling .mat file from NORB Dataset
# Imported in stimuli as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
global NORBd
import mat73 as mat
from scipy import io


# Initialize NORB Dataset
class NORB:
    def __init__(self):
        print('Loading Mat Libs...')
        self.imgs = mat.loadmat('.\imgs\mat_im_10.mat')
        self.keys = list(self.imgs.keys())
        self.cat = io.loadmat('.\imgs\mat_cat_10.mat')
    def imghandler(self,no_img=1):
        # Retrieve img_handler by passing all the parameters
        imgHandler = self.imgs[self.keys[0]][no_img]
        return imgHandler

NORBd = NORB()