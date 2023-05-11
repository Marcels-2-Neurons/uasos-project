# Main of the Surveillance Task Experiment
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
#############################################################################
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import settings as s
import pyglet as pgl
import utilities as util  # Utilities Library: utilities.py
import events as eve
import numpy as np


if __name__ == "__main__":
    s.init()
    # pgl.app.run()  # Execute window opening
    # win = eve.Window()
    s.win.run()

