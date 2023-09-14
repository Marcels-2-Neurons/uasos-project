# SRCstimuli.py>
# Library used for stimuli elaboration
# Imported in events as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
# Author: Nhat Tien PHAN - INSA
###################################################################
import string
from copy import deepcopy
from typing import Tuple

import numpy as np
from psychopy import visual
from PIL import Image


class Colors:
    red: Tuple[int, int, int] = [255, 0, 0]
    green: Tuple[int, int, int] = [0, 255, 0]
    black: Tuple[int, int, int] = [0, 0, 0]
    blue: Tuple[int, int, int] = [51, 153, 255]
    white: Tuple[int, int, int] = [255, 255, 255]
    dblue: Tuple[int, int, int] = [35, 54, 88]

class tile():
    def __init__(self, win, x, y, width, height):
        self.rect = visual.Rect(win, pos=(x, y), size=(width, height), fillColor=None,
                                lineColor=Colors.white, lineWidth=2, opacity=1.0, colorSpace='rgb255')
        self.value = None

    def draw(self):
        self.rect.draw()

class marker(): # TODO DEBUG
    def __init__(self, win, x, y, width, height):
        self.marker = visual.ImageStim(win, image="./imgs/wpy_label.png", colorSpace="rgb1",
                                        pos=(x, y), size=(width, height), interpolate=False, opacity=0.0)
        self.alive = False
        self.ratio = None
        self.center = None

    def enable_marker(self):
        self.marker.opacity = 1.0
        self.alive = True
        self.marker.draw()

    def disable_marker(self):
        self.marker.opacity = 1.0
        self.alive = False

    def draw(self):
        self.marker.draw()

    def set_pos(self, x, y):
        self.marker.pos = (x,y)
        self.enable_marker()

    def move_pos(self, x, y):
        # Input x,y as variation in px
        pos = self.marker.pos
        if pos[0] >= self.center[0]:
            pos[0] = pos[0] - x * self.ratio
        else:
            pos[0] = pos[0] + x * self.ratio
        if pos[1] >= self.center[1]:
            pos[1] = pos[1] - y * self.ratio
        else:
            pos[1] = pos[1] + y * self.ratio
        self.marker.pos = pos
        if abs(pos[0]-self.center[0]) < 0.01 and abs(pos[1]-self.center[1]) < 0.01:
            self.disable_marker()  # Disables the marker on the map
class Map():
    def __init__(self, x=0, y=0, width=0, height=0, opaque=1.0):
        from NAVevents import NAVwin
        self.map_pth = './imgs/testext.png'
        self.map_load = Image.open(self.map_pth)  # cv.imread(self.map_pth, cv.IMREAD_UNCHANGED)
        self.map = np.array(self.map_load, order="C")
        self.map = (self.map.astype(float) / 255.0)  # convert to float in 0--1 range, assuming image is 8-bit uint.
        self.map = np.flip(self.map, axis=0)
        self.h_img, self.w_img, self.ch = self.map.shape
        n = 4
        m = 4
        self.ROI = None
        self.map_sqr = visual.ImageStim(NAVwin, image=self.ROI, colorSpace="rgb1",
                                        pos=(0, 0), size=(width, height), interpolate=False, opacity=opaque)
        self.tiles = []
        self.boxes = []
        self.x_labels = []
        self.y_labels = []
        self.x_lbls = ["" for _ in range(n)]
        self.y_lbls = [int(0) for _ in range(m)]
        self.HDG_box = visual.Rect(NAVwin, pos=(x, y), size=(width, height), fillColor=Colors.dblue,
                                lineColor=Colors.white, lineWidth=2, opacity=1.0, colorSpace='rgb255')
        self.HDG_Ttxt = visual.TextStim(NAVwin, name='y_label', text='180', font='Arial',
                                                 pos=(0, 0), height=0.08, wrapWidth=None, ori=0.0,
                                                 color=Colors.white, colorSpace='rgb255', bold=True,
                                                 languageStyle='LTR', depth=0.0)
        self.HDG_Ftxt = visual.TextStim(NAVwin, name='y_label', text='180', font='Arial',
                                       pos=(0, 0), height=0.08, wrapWidth=None, ori=0.0,
                                       color=Colors.white, colorSpace='rgb255', bold=True,
                                       languageStyle='LTR', depth=0.0)
        self.WPY_box = visual.Rect(NAVwin, pos=(x, y), size=(width, height), fillColor=Colors.dblue,
                                   lineColor=Colors.white, lineWidth=2, opacity=1.0, colorSpace='rgb255')
        self.WPY_Ttxt = visual.TextStim(NAVwin, name='y_label', text='A1', font='Arial',
                                       pos=(0, 0), height=0.08, wrapWidth=None, ori=0.0,
                                       color=Colors.white, colorSpace='rgb255', bold=True,
                                       languageStyle='LTR', depth=0.0)
        self.WPY_Ftxt = visual.TextStim(NAVwin, name='y_label', text='A1', font='Arial',
                                        pos=(0, 0), height=0.08, wrapWidth=None, ori=0.0,
                                        color=Colors.white, colorSpace='rgb255', bold=True,
                                        languageStyle='LTR', depth=0.0)
        for _ in range(4):
            self.boxes.append(visual.Rect(NAVwin, pos=(x, y), size=(width, height), fillColor=Colors.black,
                                          opacity=1.0, colorSpace='rgb255'))
            self.x_labels.append(visual.TextStim(NAVwin, name='x_label', text='A', font='Arial',
                                         pos=(0, 0), height=0.08, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR', depth=0.0))
            self.y_labels.append(visual.TextStim(NAVwin, name='y_label', text='8', font='Arial',
                                                 pos=(0, 0), height=0.08, wrapWidth=None, ori=0.0,
                                                 color=Colors.white, colorSpace='rgb255', bold=True,
                                                 languageStyle='LTR', depth=0.0))
        for _ in range(n * m):
            self.tiles.append(tile(win=NAVwin, x=0, y=0, width=100, height=100))  # Placeholder values
        # Tiles are always hidden, while the wpy is hidden until the respective tile is selected
        self.wpy = None
        # these will have the tiles in which the waypoint will appear
        # TODO think about if the cursor of the mouse should be integrated here
        self.compass = visual.ImageStim(NAVwin, image='./imgs/compass_extn.png', colorSpace="rgb1",
                                        pos=(0, 0), size=(width, height), interpolate=False, opacity=opaque)
        self.needle = visual.ImageStim(NAVwin, image='./imgs/compass_point.png', colorSpace="rgb1",
                                        pos=(0, 0), size=(width, height), interpolate=False, opacity=opaque)
        self.reaper = visual.ImageStim(NAVwin, image='./imgs/UAV.png', colorSpace="rgb1",
                                        pos=(0, 0), size=(width, height), interpolate=False, opacity=opaque)
        self.h_size = None
        self.w_size = None
        self.r_square = None
        self.mouse_pos = (0, 0)
        self.mrk = marker(win=NAVwin, x=0, y=0, width=0, height=0)

    def cut_map(self, x_pos, y_pos):
        # It uses OpenCV to generate a map matrix
        # Here the coords should be within the max size of the img [0-11683] (both dimensions)
        from settings import set
        # First I check if I'm outside "boundaries"
        # Boundaries are practically conventional borders put for trigger the respawn of the a/c in the central zone of the image matrix
        # This means if I go over the first quarter - half size of the ROI, or third quarter + half size of the ROI
        # I need to force the coord to respawn in the correct region of the central area
        # 5824px is the delta in px between border and respective coord in the center map
        if round(x_pos + self.w_img/2) < (self.w_img / 4 - self.w_size / 2) or round(y_pos + self.h_img/2) < (self.h_img / 4 - self.h_size / 2):  # Case of pos near the border, I need to spawn myself on the central map
            if round(x_pos + self.w_img/2) < (self.w_img / 4 - self.w_size / 2) and round(y_pos + self.h_img/2) < (self.h_img / 4 - self.h_size / 2):
                x_pos += 5824  # round(self.w_img / 2)
                y_pos += 5824  # round(self.h_img / 2)
                #print('changed +x and +y')
            elif round(x_pos + self.w_img/2) < (self.w_img / 4 - self.w_size / 2):
                x_pos += 5824  # round(self.w_img / 2)
                #print('changed +x')
            elif round(y_pos + self.h_img/2) < (self.h_img / 4 - self.h_size / 2):
                y_pos += 5824  # round(self.h_img / 2)
                #print('changed +y')

        if round(x_pos + self.w_img/2) > (3*self.w_img / 4 + self.w_size / 2) or round(y_pos + self.h_img/2) > (3*self.h_img / 4 + self.h_size / 2):
            if round(x_pos + self.w_img/2) > (3*self.w_img / 4 + self.w_size / 2) and round(y_pos + self.h_img/2) > (3*self.h_img / 4 + self.h_size / 2):
                x_pos -= 5824  # round(self.w_img / 2)
                y_pos -= 5824  # round(self.h_img / 2)
                #print('changed -x and -y')
            elif round(x_pos + self.w_img/2) > (3*self.w_img / 4 + self.w_size / 2):
                x_pos -= 5824  # round(self.w_img / 2)
                #print('changed -x')
            elif round(y_pos + self.h_img/2) > (3*self.h_img / 4 + self.h_size / 2):
                y_pos -= 5824  # round(self.h_img / 2)
                #print('changed -y')

        self.ROI = deepcopy(
            self.map[round(self.w_img / 2 + x_pos - self.w_size / 2):round(self.w_img / 2 + x_pos + self.w_size / 2),
            round(self.h_img / 2 - y_pos - self.h_size / 2):round(self.h_img / 2 - y_pos + self.h_size / 2)])

        self.map_sqr.image = self.ROI


    def draw(self,task):
        self.map_sqr.draw()
        if self.mrk.alive is True:
            self.mrk.draw()
        for i in range(0, 16):
            self.tiles[i].draw()
        self.compass.draw()
        self.needle.draw()
        for i in range(0, 4):
            self.boxes[i].draw()
        for i in range(0, 4):
            self.x_labels[i].draw()
            self.y_labels[i].draw()
        self.reaper.draw()
        self.HDG_box.draw()
        self.WPY_box.draw()
        if task == 5:
            self.HDG_Ttxt.draw()
            self.WPY_Ftxt.draw()
        elif task == 6:
            self.HDG_Ftxt.draw()
            self.WPY_Ttxt.draw()
        else:
            self.HDG_Ftxt.draw()
            self.WPY_Ftxt.draw()

    def get_labels(self, x, y):
        x_coord = int((self.w_img/4 + x) / (225))
        y_coord = int((self.h_img/4 - y) / (225))
        for i in range(0, 4):
            self.x_labels[i].text = string.ascii_uppercase[(x_coord-(+1-i)) % 26]
            self.x_lbls[i] = self.x_labels[i].text
            self.y_labels[i].text = (y_coord-(+1-i)) % 26 + 1
            self.y_lbls[i] = self.y_labels[i].text


global map
map = Map()

def draw_map(n=4, m=4):
    # This will draw the map at the start
    from settings import set
    if set.ratio[1] != 0:
        screen = 0
    else:
        screen = 0
    h_space = (1 / 5)
    w_space = h_space / set.ratio[screen]
    h_rect = (2 - 2 * h_space) * (1 / n)
    w_rect = h_rect / set.ratio[screen]
    b_space = 1 - (3 / 2 * w_rect + w_space)

    # Our ROI will be always BIGGER than the shown on the screen, so we can perform turning and
    # at the same time

    # Generate the ROI
    # Size of the cut for the map (per 1.5 (>sqrt(2)) so we can avoid potential graphical issues on rotating)
    size = set.wsize[screen]
    zoom = 0.8  # It should be set up accordingly to the aircraft flight
    map.h_size = round((size[1] / 2) * n * h_rect * zoom)
    map.w_size = round((size[0] / 2) * n * w_rect * zoom)

    # Positions of the rectangles
    k: int = 0  # counter
    xr = {}
    yr = {}
    # Iteration will start from bottom left rectangle, continue left from right
    # and rising up. With the same number order of the Keyboard Numpad
    for i in range(0, n):
        for j in range(0, m):
            xr[k] = (-1 + 1.5 * b_space + w_rect / 2) + j * (w_rect)  # - (w_rect + w_space)
            # Last term is used for giving space to flight Director in monitor 1 (Left one)
            yr[k] = (1 - 1 * h_space - h_rect / 2) - i * (h_rect)
            k += 1
    # Set the dims of the map square
    map.map_sqr.size = (4 * w_rect * 1.5, 4 * h_rect * 1.5)
    map.r_square = 4*w_rect/map.w_size
    map.map_sqr.pos = (xr[5] + w_rect / 2, yr[5] - h_rect / 2)
    map.compass.size = ((4 * w_rect * 1.5)/(set.ratio[screen]), (4 * w_rect * 1.5))
    map.compass.pos = (xr[5] + w_rect / 2, yr[5] - h_rect / 2)
    map.compass.ori = n2mHDG(0)
    map.needle.size = ((4 * w_rect * 1.5)/(set.ratio[screen]), (4 * w_rect * 1.5))
    map.needle.pos = (xr[5] + w_rect / 2, yr[5] - h_rect / 2)
    map.needle.ori = n2mHDG(0)
    map.reaper.size = (w_rect*0.8, h_rect*0.8)
    map.reaper.pos = (xr[5] + w_rect / 2, yr[5] - h_rect / 2)

    map.mouse_pos = (xr[5] + w_rect / 2, yr[5] - h_rect / 2)
    map.mrk.marker.size = (0.7 * w_rect, h_rect * 0.35)
    map.mrk.ratio = map.r_square
    map.mrk.center = map.reaper.pos
    # Position, size of HDG and WPY Boxes
    map.HDG_box.pos = (xr[5] + w_rect / 2, yr[5])
    map.HDG_box.size = (w_rect / 2, h_rect / 4)
    map.HDG_Ttxt.pos = (xr[5] + w_rect / 2, yr[5])
    map.HDG_Ftxt.pos = (xr[5] + w_rect / 2, yr[5])
    map.WPY_box.pos = (xr[9] + w_rect / 2, yr[9])
    map.WPY_box.size = (w_rect / 2, h_rect / 4)
    map.WPY_Ttxt.pos = (xr[9] + w_rect / 2, yr[9])
    map.WPY_Ftxt.pos = (xr[9] + w_rect / 2, yr[9])

    # Set the black boxes to hide the rotations
    map.boxes[0].pos = (xr[1]+w_rect/2, 1 - h_space/2)  # Upper
    map.boxes[0].size = (2, h_space)
    map.boxes[1].pos = (xr[1]+w_rect/2, -1 + h_space/2)  # Lower
    map.boxes[1].size = (2, h_space)
    map.boxes[2].pos = ((-1 + 0.75 * b_space), 0)  # left
    map.boxes[2].size = (abs(-1 + 0.735 * b_space)+w_rect, 2)
    map.boxes[3].pos = ((xr[3]+w_rect/2)+(1-(xr[3]+w_rect/2))/2, 0)  # right
    map.boxes[3].size = ((1-(xr[3]+w_rect/2)), 2)

    #Setup the labels
    for i in range(0,4):
        map.x_labels[i].pos = (xr[i], yr[0]+h_rect/2+0.05)
        map.y_labels[i].pos = (xr[0]-w_rect/2-0.05, yr[4*i])

    # I will call update map here
    update_map(0, 0, 0)

    # Now I should add defined number of rectangles and draw with the Window Class
    s2 = 1
    for i in range(0, n * m):
        map.tiles[i].rect.size = (w_rect, h_rect)
        map.tiles[i].rect.pos = (xr[i], yr[i])
        map.tiles[i].value = ((i % 4)+1, s2)
        #map.tiles[i].draw()
        if (i % 4) + 1 == 4:
            s2 += 1


def update_map(x, y, HDG: int, x_wpy=None, y_wpy=None, freeze=False):
    # TODO Update the ROI of the map!
    # Since Tien returns me x and y as px coordinates, I should convert the central pos as in a cyclical position
    x_cyc = x % (5824)
    y_cyc = y % (5824)
    map_HDG = n2mHDG(HDG)

    # if freeze is True:
    #     pass
    #     # x_wpy = x_wpy % (5824)
    #     # y_wpy = y_wpy % (5824)
    #     #map.get_labels(x_wpy, y_wpy)
    # if freeze is False:
    #     map.get_labels(x_cyc, y_cyc)
    map.cut_map(x_pos=x_cyc, y_pos=y_cyc)
    map.map_sqr.ori = map_HDG
    map.compass.ori = map_HDG

def update_needle(HDG: int):
    map.needle.ori = -n2mHDG(HDG)
def n2mHDG(nHDG: int):  # It returns the correct Aeronautical Heading
    return 90 - nHDG
