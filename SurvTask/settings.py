# settings.py>
# Library used for initialize global variables and settings
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
from psychopy import visual, core, event, monitors

#Data about monitor
widthPix = 1920 # screen width in px
heightPix = 1080 # screen height in px
# monitorwidth = 53.1 # monitor width in cm
# viewdist = 60. # viewing distance in cm
monitorname = 'iiyama'
scrn = 0 # 0 to use main screen, 1 to use external screen

global mon
global wsize
global ratio
wsize = (1920,1080) # (widthPix, heightPix)
ratio = wsize[0]/wsize[1]
mon = monitors.Monitor(monitorname)
mon.setSizePix((widthPix, heightPix))

global n_num,m_num
n_num: int = 3
m_num: int = 3


def init():
    pass