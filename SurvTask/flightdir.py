# flightdir.py>
# Library used for Flight Director drawing and execution
# Imported in events as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

from typing import Tuple
from psychopy import visual  #, core, event
from mathandler import NORBd
from settings import n_num, m_num

from random import *
global FDir


class Colors:
    green: Tuple[int, int, int] = [0, 255, 0]
    dgreen: Tuple[int, int, int] = [15, 88, 10]  # Hex: 0F580A
    black: Tuple[int, int, int] = [0, 0, 0]
    white: Tuple[int, int, int] = [255, 255, 255]
    # From Vintage PC Color Palettes
    lgray: Tuple[int, int, int] = [190, 190, 190]  # Hex: BEBEBE
    gray: Tuple[int, int, int] = [146, 147, 147]  # Hex: 929393
    dgray: Tuple[int, int, int] = [55, 55, 56]  # Hex: 373738


class flightdir:
    def __init__(self, x=0, y=0, cat=0, width=0, height=0, opaque=1.0):
        from events import win
        from local import langue
        self.border = visual.Rect(win, pos=(x, y),
                                size=(width, height),
                                fillColor=Colors.lgray,
                                opacity=1.0,
                                colorSpace='rgb255')
        self.face = visual.Rect(win, pos=(x, y),
                                size=(width, height),
                                fillColor=Colors.gray,
                                opacity=1.0,
                                colorSpace='rgb255')
        self.screen = visual.Rect(win, pos=(x, y),
                                size=(width, height),
                                fillColor=Colors.dgray,
                                opacity=1.0,
                                colorSpace='rgb255')
        self.led = visual.Circle(win, pos=(x, y),
                                size=(width, height),
                                fillColor=Colors.dgreen,
                                opacity=1.0,
                                colorSpace='rgb255')
        src_str: str = langue.get_string('SEARCH')
        item_str: str = langue.get_string('NONE')

        self.text_src = visual.TextStim(win=win, name='text',
                                        text=src_str,
                                        font='Open Sans',
                                        pos=(x, y), height=0.1, wrapWidth=None, ori=0.0,
                                        color=Colors.white, colorSpace='rgb255', bold=True,
                                        languageStyle='LTR',
                                        depth=0.0)

        self.text_item = visual.TextStim(win=win, name='text',
                                        text=item_str,
                                        font='Open Sans',
                                        pos=(x, y), height=0.07, wrapWidth=None, ori=0.0,
                                        color=Colors.white, colorSpace='rgb255', bold=True,
                                        languageStyle='LTR',
                                        depth=0.0)
        self.generate(1)


    def generate(self, n_monitor):
        # generate on the screen the flight director interface
        from settings import wsize,ratio
        h_space = (1 / 30)
        w_space = h_space / ratio
        h_rect = 1 * ((1 - 4 * h_space) / n_num)
        r_border = 0.05  # 2% of the size is the border
        w_rect = 1 / ratio
        rad_led = 1/30

        # Set up the Face of the Flight Director
        self.face.pos = ((1-w_rect/2), (1 - 3*h_space - h_rect/2))
        self.face.size = (w_rect, h_rect)
        # Set up the border
        self.border.pos = ((1-w_rect/2), (1 - 3*h_space - h_rect/2))
        self.border.size = (w_rect*(1+r_border), h_rect*(1+r_border))
        # Set up the screen
        self.screen.pos = (1-(2*w_rect/3-8*w_space), (1 - 9*h_space))
        self.screen.size = (w_rect, h_rect/3)
        # Set up the LED
        self.led.pos = (1-(w_rect-3*w_space), (1 - 5.5*h_space))
        self.led.size = (1.5*h_space, 1.5*h_space*ratio)
        # Set up the Text SEARCH
        self.text_src.pos = (1-(w_rect-16*w_space), (1 - 5.5*h_space))
        # Set up the Text ITEM
        self.text_item.pos = (1 - (w_rect - 16 * w_space), (1 - 9 * h_space))

    def draw(self):
        self.border.draw()
        self.face.draw()
        self.screen.draw()
        self.led.draw()
        self.text_src.draw()
        self.text_item.draw()

    def item_change(self, id_item):
        from local import langue
        if id_item == 1:
            self.text_item.text = langue.get_string('PEOPLE')
        elif id_item == 4:
            self.text_item.text = langue.get_string('VEHICLES')
        elif id_item == 5:
            self.text_item.text = langue.get_string('HEADING')
        elif id_item == 6:
            self.text_item.text = langue.get_string('WAYPOINT')
        else:
            self.text_item.text = langue.get_string('NONE')
        return

    def led_on(self):
        self.led.color = Colors.green

    def led_off(self):
        self.led.color = Colors.dgreen


FDir = flightdir()