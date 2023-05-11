# events.py>
# Library used for the events callout in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import random
import time
from random import *

global win
# global sprites
# global batch
global keyLog
global saveLog
# batch = pgl.graphics.Batch()
# sprites = {}
keyLog: list = []
saveLog: list = [0 for i in range(9)]

from psychopy import visual, core, event
import stimuli as stim
import settings as s


class Window(visual.Window):
    # Initialization of the class
    def __init__(self):
        from settings import wsize
        super(Window, self).__init__(size=wsize, fullscr=False, color=(-1, -1, -1), allowGUI=True)

        self.alive = 1

    # Drawing of the stimuli
    def on_draw(self):
        self.render()

    # Rendering of the stimuli
    def render(self):
        # self.clear()
        # stimuli drawing
        from stimuli import Rects
        for i in range(0, s.n_num*s.m_num):
            Rects[i].draw()
        self.flip()

    def run(self):
        from stimuli import Rects
        stim.drw_matrix()
        # For DEMO PURPOSE ONLY
        filters = ['Gaussian','SaltAndPepper','Poisson','Speckle','Blur','LowContrast','Bars','Vignette','Tearing','None']
        start_time = time.time()
        elapsed_time = 0  # seconds
        duration = 2  # seconds
        while self.alive:
            # Get key event
            keys = event.getKeys()

            for symbol in keys:
                if symbol == 'num_1':
                    keyLog.append(6)
                    Rects[6].highlight()
                elif symbol == 'num_2':
                    keyLog.append(7)
                    Rects[7].highlight()
                elif symbol == 'num_3':
                    keyLog.append(8)
                    Rects[8].highlight()
                elif symbol == 'num_4':
                    keyLog.append(3)
                    Rects[3].highlight()
                elif symbol == 'num_5':
                    keyLog.append(4)
                    Rects[4].highlight()
                elif symbol == 'num_6':
                    keyLog.append(5)
                    Rects[5].highlight()
                elif symbol == 'num_7':
                    keyLog.append(0)
                    Rects[0].highlight()
                elif symbol == 'num_8':
                    keyLog.append(1)
                    Rects[1].highlight()
                elif symbol == 'num_9':
                    keyLog.append(2)
                    Rects[2].highlight()
                elif symbol == 'escape':
                    self.close()
                    core.quit()
                else:
                    pass
            # Random Change of the image: DEMO Test
            time.sleep(1/60) # 60 Hz refresh
            # Time WatchDog for the refresh of the image: DEMO
            if elapsed_time >= duration:
                for i in range(0, 9):
                    s_filt = choice(filters)
                    if s_filt == 'None':
                        Rects[i].changeImg(randint(1, 29160))
                    elif s_filt == 'Gaussian':
                        Rects[i].changeImg(randint(1, 29160), gaussian=0.5)
                    elif s_filt == 'SaltAndPepper':
                        Rects[i].changeImg(randint(1, 29160), saltpepper=0.2)
                    elif s_filt == 'Poisson':
                        Rects[i].changeImg(randint(1, 29160), poisson=1)
                    elif s_filt == 'Speckle':
                        Rects[i].changeImg(randint(1, 29160), speckle=0.1)
                    elif s_filt == 'Blur':
                        Rects[i].changeImg(randint(1, 29160), blur=0.4)
                    elif s_filt == 'LowContrast':
                        Rects[i].changeImg(randint(1, 29160), lowcontrast=1)
                    elif s_filt == 'Bars':
                        Rects[i].changeImg(randint(1, 29160), bars=0.6)
                    elif s_filt == 'Vignette':
                        Rects[i].changeImg(randint(1, 29160), vignette=1)
                    elif s_filt == 'Tearing':
                        Rects[i].changeImg(randint(1, 29160), tearing=1)

                start_time = time.time()
            else: pass

            elapsed_time = time.time() - start_time
            self.render()


win = Window()
