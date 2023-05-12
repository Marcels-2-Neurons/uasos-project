# stimuli.py>
# Library used for stimuli elaboration
# Imported in events as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

from typing import Tuple
from psychopy import visual, core, event
from mathandler import NORBd
from settings import n_num, m_num
from random import *

class Colors:
    red: Tuple[int, int, int] = [255, 0, 0]
    green: Tuple[int, int, int] = [0, 255, 0]
    black: Tuple[int, int, int] = [0, 0, 0]
    blue: Tuple[int, int, int] = [51, 153, 255]
    white: Tuple[int, int, int] = [255, 255, 255]


# in PsychoPy, x,y,width and height are defined in % of screen width/height
class RecObj:
    def __init__(self, x, y, n_img, width, height):
        from events import win
        self.hobj = visual.Rect(win, pos=(x, y),
                                size=(width, height),
                                fillColor=Colors.white,
                                opacity=0.0,
                                colorSpace='rgb255')

        self.img = visual.ImageStim(win, image=NORBd.imghandler(n_img), #'.\lenna.png',
                                    pos=(x, y), size=(width*0.95, height*0.95), interpolate=False)

    def show(self):
        self.hobj.visible = True

    def highlight(self):
        if self.hobj.opacity == 0.0:
            self.hobj.opacity = 1.0
        elif self.hobj.opacity != 0.0:
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

    def draw(self):
        self.hobj.draw()
        self.img.draw()

    def changeImg(self, n_img, gaussian=0, saltpepper=0, poisson=0, speckle=0, blur=0, tearing=0):
        self.img.image = NORBd.imghandler(n_img, gaussian, saltpepper, poisson, speckle, blur, tearing)
        # if self.hobj.opacity != 0.0:
        #    self.hobj.opacity = 0.0


global Rects
Rects = {}


def drw_matrix(n_num=n_num, m_num=m_num):
    from settings import ratio
    h_space = (1 / 30)
    w_space = h_space/ratio
    h_rect = 2*((1-4*h_space) / n_num)
    w_rect = h_rect/ratio
    b_space = 1 - (3 / 2 * w_rect + w_space)

    # Positions of the rectangles
    k: int = 0  # counter
    xr = {}
    yr = {}
    # Iteration will start from bottom left rectangle, continue left from right
    # and rising up. With the same number order of the Keyboard Numpad
    for i in range(0, n_num):
        for j in range(0, m_num):
            # xr[k] = (-1 + b_space) + (((3 - j) * w_rect) + ((2 - j) * w_space))
            # yr[k] = 1 - ((h_space * (i + 1)) + (h_rect * (i + 1)))
            xr[k] = (-1 + b_space + w_rect/2) + j * (w_rect + w_space)
            yr[k] = (1 - 3*h_space - h_rect/2) - i * (h_rect + h_space)
            k += 1

    # Now I should add defined number of rectangles and draw with the Window Class
    for i in range(0, n_num * m_num):
        Rects[i] = RecObj(xr[i], yr[i],randint(1, 29160),w_rect, h_rect)
        Rects[i].draw()
