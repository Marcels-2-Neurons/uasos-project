# events.py>
# Library used for the events callout in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

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
from pyglet.window import key


class Window(visual.Window):
    # Initialization of the class
    def __init__(self):
        from settings import wsize
        super(Window, self).__init__(size=wsize, fullscr=False, color=(-1, -1, -1))

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
                else:
                    pass

            self.render()



win = Window()
