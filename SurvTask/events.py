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
        if len(s.mon) == 2:
            super(Window, self).__init__(size=s.wsize[1], screen=1, fullscr=s.Fullscreen, color=(-1, -1, -1),
                                         allowGUI=True)
        else:
            super(Window, self).__init__(size=s.wsize, screen=0, fullscr=s.Fullscreen, color=(-1, -1, -1),
                                         allowGUI=True)

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
        changed = False

        stim.drw_matrix()
        # For DEMO PURPOSE ONLY
        filters = ['Gaussian', 'SaltAndPepper', 'Poisson', 'Speckle', 'Blur', 'Tearing', 'MPEG', 'None']
        start_time = time.time()
        elapsed_time = 0  # seconds
        duration = 2  # seconds
        clock = core.Clock()  # for analysis of the image change
        watchdog = core.Clock()
        fps = 1 / 60  # Fixed at 60 Hz
        while self.alive:
            # Start Watchdog for reset the frame time
            watchdog.reset()
            # Get key event
            if changed:
                duration = 1 + random()
                changed = False
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
            r_time = fps - watchdog.getTime()
            if r_time > 0:
                core.wait(r_time)
            # time.sleep(1/30) # 30 Hz refresh (Putting the actual refresh of the monitor is CRITICAL)
            # Time WatchDog for the refresh of the image: DEMO
            if elapsed_time >= duration:
                i = randint(0,8)
                s_filt = choice(filters)
                r_case = randint(0, 3) # 0 - Original / 1: 90deg CClock / 2: 180deg CClock / 3: 270deg CClock
                if s_filt == 'None':
                   Rects[i].changeImg(randint(0, 29159))
                elif s_filt == 'Gaussian':
                   Rects[i].changeImg(randint(0, 29159), rotate=r_case, gaussian=0.5)
                elif s_filt == 'SaltAndPepper':
                   Rects[i].changeImg(randint(0, 29159), rotate=r_case, saltpepper=0.2)
                elif s_filt == 'Poisson':
                   Rects[i].changeImg(randint(0, 29159), rotate=r_case, poisson=1)
                elif s_filt == 'Speckle':
                   Rects[i].changeImg(randint(0, 29159), rotate=r_case, speckle=0.1)
                elif s_filt == 'Blur':
                   Rects[i].changeImg(randint(0, 29159), rotate=r_case, blur=0.4)
                elif s_filt == 'Tearing':
                   Rects[i].changeImg(randint(0, 29159), rotate=r_case, tearing=1)
                elif s_filt == 'MPEG':
                   Rects[i].changeImg(randint(0, 29159), rotate=r_case, mpeg=1)
                   # Removed LowContrast,Bars and Vignette for compatibility issue with NORB DB
                start_time = time.time()
                changed = True
                print('Image changed in ', "%.3f" % (elapsed_time), ' sec')
                clock.reset()  # to reset the clock
            else:
                pass

            elapsed_time = clock.getTime()
            self.render()


win = Window()
