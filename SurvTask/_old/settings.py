# settings.py>
# Library used for initialize global variables and settings
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import pyglet as pgl
import events as eve

global win
win = eve.Window()  # Creates the window

global label
label = pgl.text.Label('Hold on',
                           font_name='Arial',
                           font_size=36,
                           x=win.width // 2, y=win.height // 2,
                           anchor_x='center', anchor_y='center')  # Generates a label

global n_num,m_num
n_num: int = 3
m_num: int = 3

def init():
    pass