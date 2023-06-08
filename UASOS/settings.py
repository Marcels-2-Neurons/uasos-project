# settings.py>
# Library used for initialize global variables and settings
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import screeninfo

# Still to implement:


# Data about monitor
widthPix = 1920  # screen width in px
heightPix = 1080  # screen height in px
# monitorwidth = 53.1 # monitor width in cm
# viewdist = 60. # viewing distance in cm
monitorname = 'Philips'
scrn = 0  # 0 to use main screen, 1 to use external screen

# TO-DO: BETTER MULTIDISPLAY INFO ACQUISITION FOR AUTOMATIC SETUP
global n_num
global m_num
n_num: int = 3
m_num: int = 3


class settings:
    def __init__(self):
        self.mon = screeninfo.get_monitors()

        if len(self.mon) == 2:
            self.wsize = [(0, 0), (0, 0)]
            self.ratio = [0, 0]
            self.wsize[0] = (self.mon[0].width, self.mon[0].height)
            self.wsize[1] = (self.mon[1].width, self.mon[1].height)
            self.ratio[0] = self.wsize[0][0] / self.wsize[0][1]
            self.ratio[1] = self.wsize[1][0] / self.wsize[1][1]
            # For DEBUG ONLY i use fixed ratio
            # self.ratio = self.wsize[1][0]/self.wsize[1][1]
            self.Fullscreen = True
        else:
            self.wsize = (1600, 1400)  # (widthPix, heightPix)
            self.ratio = self.wsize[0] / self.wsize[1]
            self.Fullscreen = False
        # mon = monitors.Monitor(monitorname)
        # mon.setSizePix((widthPix, heightPix))
        # n_monitors = len(screeninfo.get_monitors())

        self.n_num: int = 3
        self.m_num: int = 3


set = settings()
