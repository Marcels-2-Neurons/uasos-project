# events.py>
# Library used for the events callout in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import random
import time
from random import *
from scriptgen import script

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

    def update_stim(self, step):
        # Function that updates the images
        from stimuli import Rects
        from flightdir import FDir
        # Reset opacity of the highlights
        for a in range(0, s.n_num*s.m_num):
            Rects[a].hobj.opacity = 0.0

        for pic in range(0, s.n_num*s.m_num):
            if step == 0 or script.IMGS[step-1][pic] != script.IMGS[step][pic]:
                f_num = script.FILS[step][pic]
                if f_num == 0:  # None
                    Rects[pic].changeImg(script.IMGS[step][pic])
                elif f_num == 1:  # Gaussian
                    Rects[pic].changeImg(script.IMGS[step][pic], rotate=script.ROTS[step][pic], gaussian=0.5)
                elif f_num == 2:  # SaltAndPepper
                    Rects[pic].changeImg(script.IMGS[step][pic], rotate=script.ROTS[step][pic], saltpepper=0.2)
                elif f_num == 3:  # Poisson
                    Rects[pic].changeImg(script.IMGS[step][pic], rotate=script.ROTS[step][pic], poisson=1)
                elif f_num == 4:  # Speckle
                    Rects[pic].changeImg(script.IMGS[step][pic], rotate=script.ROTS[step][pic], speckle=0.1)
                elif f_num == 5:  # Blur
                    Rects[pic].changeImg(script.IMGS[step][pic], rotate=script.ROTS[step][pic], blur=0.4)
                elif f_num == 6:  # Tearing
                    Rects[pic].changeImg(script.IMGS[step][pic], rotate=script.ROTS[step][pic], tearing=1)
                elif f_num == 7:  # MPEG
                    Rects[pic].changeImg(script.IMGS[step][pic], rotate=script.ROTS[step][pic], mpeg=1)
            else: pass

        for a in range(0, s.n_num * s.m_num):
            if script.CORS[step][a] == 1: # Case Correct, for DEBUG purposes
                Rects[a].correct()
        if script.TASK[step] in [1,4]:
            FDir.led_on()
            FDir.item_change(script.TASK[step])
        else:
            FDir.item_change(0)
            FDir.led_off()

    # Drawing of the stimuli
    def on_draw(self):
        self.render()

    # Rendering of the stimuli
    def render(self):
        # self.clear()
        # stimuli drawing
        from stimuli import Rects
        from flightdir import FDir
        for i in range(0, s.n_num*s.m_num):
            Rects[i].draw()
        FDir.draw()
        self.flip()

    def run(self):
        from stimuli import Rects
        changed = False

        stim.drw_matrix()
        # For DEMO PURPOSE ONLY
        exp_step = 0
        elapsed_time = 0  # seconds
        duration = 250  # msec
        clock = core.Clock()  # for analysis of the image change
        watchdog = core.Clock()
        fps = 1 / 60 * 1000  # Fixed at 60 Hz - msec

        while self.alive:
            # Start Watchdog for reset the frame time
            watchdog.reset()
            if changed:
                exp_step += 1
                duration = script.TIME[exp_step]
                changed = False

            # Change of the Image Stim
            r_time = fps - (watchdog.getTime() * 1000)
            if r_time > 0:
                core.wait(r_time/1000)

            if elapsed_time >= duration:
                self.update_stim(exp_step)
                changed = True
                print('Image changed in ', "{:.3f}".format(elapsed_time), ' msec')
            else:
                pass

            elapsed_time = clock.getTime() * 1000
            self.render()

            # Get key event: Generate a Keylog function
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

win = Window()
