# settings.py>
# Library used for initialize global variables and settings
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import screeninfo

# TO-DO: BETTER MULTIDISPLAY INFO ACQUISITION FOR AUTOMATIC SETUP
global n_num
global m_num
n_num: int = 3
m_num: int = 3


class settings:
    def __init__(self):
        self.mon = screeninfo.get_monitors()
        self.SRCwin = 1  # It should be your LEFT SCREEN
        self.NAVwin = 0  # It should be your RIGHT SCREEN
        self.processes = []
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
