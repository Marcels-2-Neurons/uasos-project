# utilities.py>
# Library used for first (and following) utility functions to use inside the project
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

from typing import Tuple
import pyglet as pgl
from pyglet import shapes
import events as eve
import settings as s
import numpy as np

# Class for a Highlighting Rectangle on-selection
# I should add:
# - Order to the TRect Class! For now the order is Typewriter like
# Other ideas will follow on, it's just a Tech Demo

# Color definition class


class Colors:
    red: Tuple[int, int, int] = (255, 0, 0)
    green: Tuple[int, int, int] = (0, 255, 0)
    blue: Tuple[int, int, int] = (51, 153, 255)
    white: Tuple[int, int, int] = (255, 255, 255)


# Rectangles definition class
class TRect:
    def __init__(self, x, y, width, height, color, batch, group):
        self.hobj = shapes.Rectangle(x-7, y-7, width+14, height+14, Colors.blue, batch, group)  # it starts with blue
        self.objR = shapes.Rectangle(x, y, width, height, color, batch, group)
        self.hobj.visible = False

    def show(self):
        self.objR.visible = True

    def highlight(self):
        self.hobj.color = Colors.blue
        self.hobj.visible = True

    def correct(self):
        # update hobj color to green
        self.hobj.visible = False
        self.hobj.color = Colors.green
        self.hobj.visible = True

    def wrong(self):
        # update hobj color to red
        self.hobj.visible = False
        self.hobj.color = Colors.red
        self.hobj.visible = True

    def draw(self):
        self.hobj.draw()
        self.objR.draw()


global Rects
global Rgroup  # To make an order of rendering
Rgroup = {}
Rects = {}
# Draw Test Matrix - For DEBUG Purposes


def drw_matrix(w_height=s.win.height, w_width=s.win.width, n_num=s.n_num, m_num=s.m_num):
    # Use test rectangles inside here (T_rect)
    # Dimensions of white spaces and rectangles
    h_space: int = round((1/30)*w_height)
    w_space: int = h_space
    h_rect: int = round((w_height - (h_space * 4)) / n_num)
    w_rect: int = h_rect
    b_space: int = round((w_width/2) - (3/2*w_rect+w_space))

    # Positions of the rectangles
    k: int = 0  # counter
    xr = {}
    yr = {}
    # Iteration will start from bottom left rectangle, continue left from right
    # and rising up. With the same number order of the Keyboard Numpad
    for i in range(0, n_num):
        for j in range(0, m_num):
            xr[k] = (w_width-b_space) - (((3-j)*w_rect)+((2-j)*w_space))
            yr[k] = w_height - ((h_space*(i+1)) + (h_rect*(i+1)))
            k += 1

    # Now I should add defined number of rectangles and draw with the Window Class
    for i in range(0, n_num*m_num):
        Rgroup[i] = pgl.graphics.Group(i)
        eve.sprites[i] = TRect(xr[i], yr[i], w_rect, h_rect, Colors.white, eve.batch, Rgroup[i])
