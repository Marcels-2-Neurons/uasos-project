# settings.py>
# Library used for initialize global variables and settings
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import ctypes

import screeninfo
import sys

# Still to implement:


# Data about monitor
widthPix = 1920  # screen width in px
heightPix = 1080  # screen height in px

# TO-DO: BETTER MULTIDISPLAY INFO ACQUISITION FOR AUTOMATIC SETUP
global n_num
global m_num
n_num: int = 3
m_num: int = 3


class settings:
    def __init__(self):
        self.mon = screeninfo.get_monitors()
        self.SRCwin = 1
        self.NAVwin = 0
        self.pyro4_path = "C:\\Users\\vi.vitale\\AppData\\Local\\Programs\\PsychoPy\\Scripts\\pyro4-ns.exe"
        if len(self.mon) == 2:
            self.n_mon = 2
            self.wsize = [(0, 0), (0, 0)]
            self.ratio = [0, 0]
            self.wsize[0] = (self.mon[0].width, self.mon[0].height)
            self.wsize[1] = (self.mon[1].width, self.mon[1].height)
            self.ratio[0] = self.wsize[0][0] / self.wsize[0][1]
            self.ratio[1] = self.wsize[1][0] / self.wsize[1][1]
            self.Fullscreen = False
        else:
            self.n_mon = 1
            self.wsize = [(0, 0), (0, 0)]
            self.wsize[0] = (1280, 720)  # (widthPix, heightPix)
            self.ratio = [0, 0]
            self.ratio[0] = self.wsize[0][0] / self.wsize[0][1]
            self.Fullscreen = False

        self.n_num: int = 3
        self.m_num: int = 3

        self.close = False


set = settings()
