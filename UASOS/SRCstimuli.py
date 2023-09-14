# SRCstimuli.py>
# Library used for stimuli elaboration
# Imported in events as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
from typing import Tuple

from psychopy import visual
from mathandler import NORBd
from settings import n_num, m_num
from random import *
import imgtreat as img


class Colors:
    red: Tuple[int, int, int] = [255, 0, 0]
    green: Tuple[int, int, int] = [0, 255, 0]
    black: Tuple[int, int, int] = [0, 0, 0]
    blue: Tuple[int, int, int] = [51, 153, 255]
    white: Tuple[int, int, int] = [255, 255, 255]
    dblue: Tuple[int, int, int] = [35, 54, 88]


# in PsychoPy, x,y,width and height are defined in % of screen width/height

class RecObj:
    def __init__(self, x, y, n_img, width, height, opaque=1.0):
        from SRCevents import SRCwin
        self.hobj = visual.Rect(SRCwin, pos=(x, y),
                                size=(width, height),
                                fillColor=Colors.white,
                                opacity=0.0,
                                colorSpace='rgb255')

        self.img = visual.ImageStim(SRCwin, image=NORBd.imghandler(n_img),
                                    pos=(x, y), size=(width * 0.95, height * 0.95), interpolate=False, opacity=opaque)
        pass

    def show(self):
        self.hobj.visible = True

    def highlight(self):
        if self.hobj.opacity == 0.0:
            self.hobj.opacity = 1.0

    def no_hlight(self):
        if self.hobj.opacity != 0.0:
            self.hobj.opacity = 0.0

    def correct(self):
        # update hobj color to green
        self.hobj.opacity = 0.0
        self.hobj.color = Colors.green
        self.hobj.opacity = 1.0

    def wrong(self):
        # update hobj color to red
        self.hobj.opacity = 0.0
        self.hobj.color = Colors.red
        self.hobj.opacity = 1.0

    def draw(self, case=0):
        if case != 0:
            self.hobj.draw()
            self.img.draw()
        else:
            pass

    def changeImg(self, n_img, rotate=0, gaussian=0, saltpepper=0, poisson=0, speckle=0, blur=0, tearing=0, mpeg=0):
        if rotate != 0:
            self.img.image = img.rotate(self.img.image, rotate)
        self.img.image = NORBd.imghandler(n_img, gaussian, saltpepper, poisson, speckle, blur, tearing, mpeg)
        self.img.opacity = 1.0  # due to the opacity 0.0 put in the matrix initialization
        if self.hobj.opacity != 0.0:
            self.hobj.color = Colors.white
            self.hobj.opacity = 0.0


global Rects
Rects = {}


def drw_matrix(n=n_num, m=m_num, Imgs=None):
    from settings import set
    if set.ratio[1] != 0:
        screen = 1
    else:
        screen = 0
    h_space = (1 / 30)
    w_space = h_space / set.ratio[screen]
    h_rect = 2 * ((1 - 4 * h_space) / n)
    w_rect = h_rect / set.ratio[screen]
    b_space = 1 - (3 / 2 * w_rect + w_space)

    # Positions of the rectangles
    k: int = 0  # counter
    xr = {}
    yr = {}
    # Iteration will start from bottom left rectangle, continue left from right
    # and rising up. With the same number order of the Keyboard Numpad
    for i in range(0, n):
        for j in range(0, m):
            xr[k] = (-1 + b_space + w_rect / 2) + j * (w_rect + w_space) - (w_rect + w_space)  # Last term is used for giving space to flight Director
            yr[k] = (1 - 3 * h_space - h_rect / 2) - i * (h_rect + h_space)
            k += 1

    # Now I should add defined number of rectangles and draw with the Window Class
    if Imgs is None:
        for i in range(0, n * m):
            Rects[i] = RecObj(xr[i], yr[i], randint(0, 911), w_rect, h_rect, opaque=0.0)
            Rects[i].draw()
    else:
        for i in range(0, n * m):
            Rects[i] = RecObj(xr[i], yr[i], randint(0, 911), w_rect, h_rect, opaque=0.0)
            Rects[i].img.image = NORBd.imghandler(Imgs[i])
            Rects[i].draw()