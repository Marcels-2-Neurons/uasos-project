# settings.py>
# Library used for initialize global variables and settings
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
from psychopy import visual, core, event, monitors
import screeninfo

#Data about monitor
widthPix = 1920 # screen width in px
heightPix = 1080 # screen height in px
# monitorwidth = 53.1 # monitor width in cm
# viewdist = 60. # viewing distance in cm
monitorname = 'Philips'
scrn = 0 # 0 to use main screen, 1 to use external screen

# TO-DO: BETTER MULTIDISPLAY INFO ACQUISITION FOR AUTOMATIC SETUP
global mon
global Fullscreen
global wsize
global ratio
wsize = {}
ratio = {}
mon = screeninfo.get_monitors()

if len(mon) == 2:
    wsize[0]=(mon[0].width,mon[0].height)
    wsize[1]=(mon[1].width,mon[1].height)
    # ratio[0] = wsize[0][0]/wsize[0][1]
    # ratio[1] = wsize[1][0]/wsize[1][1]
    # For DEBUG ONLY i use fixed ratio
    ratio = wsize[1][0]/wsize[1][1]
    Fullscreen = True
else:
    wsize = (1600,1400) # (widthPix, heightPix)
    ratio = wsize[0]/wsize[1]
    Fullscreen = False
# mon = monitors.Monitor(monitorname)
# mon.setSizePix((widthPix, heightPix))
# n_monitors = len(screeninfo.get_monitors())


global n_num,m_num
n_num: int = 3
m_num: int = 3


def init():
    pass