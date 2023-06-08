# SRCevents.py>
# Library used for the events callout in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import input
import os
import atexit
import Pyro4 as pyro
from psychopy import visual, core
import serpent
import base64
from copy import *
from packet import Packet
import subprocess
import stimuli as stim
from settings import set

global SRCwin
# Rewrite the keyLog!
global keyLog
global saveLog

keyLog: list = [0 for _ in range(9)]
saveLog: list = [0 for _ in range(9)]


# Still to implement:
# Navigation update/render/run cycle (similar to the one from Search task)
# Call to the csv writing lib


class SRCWindow(visual.Window):
    # Initialization of the class
    def __init__(self):
        if len(set.mon) == 2:
            width, height = set.wsize[1]
            super(SRCWindow, self).__init__(size=(width, height), screen=1, fullscr=set.Fullscreen, color=(-1, -1, -1),
                                            allowGUI=True)
        else:
            super(SRCWindow, self).__init__(size=set.wsize, screen=0, fullscr=set.Fullscreen, color=(-1, -1, -1),
                                            allowGUI=True)

        self.case = 0  # Case 0 - Start of the Experiment, in Hold / Case 1 - Experiment Routine
        self.duration = 0
        self.alive = 1
        self.spack = None
        self.pack = Packet()

        # Pyro Client Init
        pyro4_path = "C:\\Users\\vi.vitale\\AppData\\Local\\Programs\\PsychoPy\\Scripts\\pyro4-ns.exe"
        subprocess.Popen([pyro4_path])
        subprocess.Popen(["python", "pyro_server.py"])
        # Wait for the server start up, cycle until the uri is obtained
        uri = None
        while uri is None:
            try:
                uri = pyro.locateNS().lookup("pyro_svr")
            except pyro.errors.NamingError:
                pass

        # Connect to the pyro server
        self.pkproxy = pyro.Proxy(uri)

    def update_stim(self, step, change):
        # Function that updates the images
        from stimuli import Rects
        from flightdir import FDir

        if change:
            # Reset opacity of the highlights
            for a in range(0, set.n_num * set.m_num):
                Rects[a].hobj.opacity = 0.0

            for pic in range(0, set.n_num * set.m_num):
                if step == 0 or self.pack.pImgs[pic] != self.pack.Imgs[pic]:
                    f_num = self.pack.Fils[pic]
                    if f_num == 0:  # None
                        Rects[pic].changeImg(self.pack.Imgs[pic])
                    elif f_num == 1:  # Gaussian
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], gaussian=0.5)
                    elif f_num == 2:  # SaltAndPepper
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], saltpepper=0.2)
                    elif f_num == 3:  # Poisson
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], poisson=1)
                    elif f_num == 4:  # Speckle
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], speckle=0.1)
                    elif f_num == 5:  # Blur
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], blur=0.4)
                    elif f_num == 6:  # Tearing
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], tearing=1)
                    elif f_num == 7:  # MPEG
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], mpeg=1)
                else:
                    pass
            # Led activity changes just at every new step
            if self.pack.Task in [1, 4]:
                FDir.led_on()
                FDir.item_change(self.pack.Task)
            else:
                FDir.item_change(0)
                FDir.led_off()
        else:
            for a in range(0, set.n_num * set.m_num):
                if keyLog[a] == 1 and Rects[a].hobj.opacity == 0.0:  # Case Selected, for DEBUG purposes
                    Rects[a].highlight()

    # Drawing of the stimuli
    def on_draw(self):
        self.render()

    # Rendering of the stimuli
    def render(self):
        # stimuli drawing
        from stimuli import Rects
        from flightdir import FDir
        for i in range(0, set.n_num * set.m_num):
            Rects[i].draw(case=self.case)
        FDir.draw(case=self.case)
        self.flip()
        self.getFutureFlipTime()  # Code in-sync with the Monitor

    def run(self):
        # Graphical Runtime
        changed = False
        self.request_pkg(0)
        stim.drw_matrix()

        exp_step = 0
        elapsed_time = -1  # msec
        self.duration = 0  # msec
        clock = core.Clock()  # for analysis of the image change
        # filetxt = open('latency_test.txt', 'w', newline='') # DEBUG PURPOSE: Latency Test
        while self.alive:
            global keyLog
            # Start Watchdog for reset the frame time

            if elapsed_time >= self.duration:
                self.update_stim(exp_step, change=True)
                self.render()
                elapsed_time = clock.getTime() * 1000
                changed = True
                keyLog = [0 for _ in range(9)]
                # print('Image changed in ', "{:.3f}".format(elapsed_time), ' msec,', "{:.3f}".format(elapsed_time-script.TIME[exp_step]), ' msec late.')
                # filetxt.write("{:.3f}".format(elapsed_time-script.TIME[exp_step])+'\n') # DEBUG PURPOSE: Latency Test
            else:
                pass

            if changed:
                exp_step += 1
                self.request_pkg(exp_step)
                self.duration = self.pack.Time
                changed = False

            self.update_stim(exp_step, change=False)
            if self.duration != 0:  # we don't want to have updates where we are in waiting
                self.render()
                elapsed_time = clock.getTime() * 1000
            else:
                self.render()
                clock.reset()  # maintain the clock at zero

            key = input.get_num_keys()
            if key is not None and key not in ['s', 'escape']:
                keyLog[int(key)] = 1
            elif key == 'escape':
                self.pkproxy.close()  # Server Closing
                self.close()
                atexit.register(os.system("taskkill /f /im python.exe"))  # Guarantee the clean exit of the experiment
                core.quit()
            elif key == 's' and self.case == 0:  # routine for starting the experiment
                self.case = 1
                self.duration = self.pack.Time
                clock.reset()
                elapsed_time = clock.getTime() * 1000
                changed = False
            else:
                pass

    def request_pkg(self, it):
        # Function to retrieve the packet
        del self.spack
        del self.pack
        self.pack = Packet()  # Reset of the packet
        self.spack = self.pkproxy.read_data(it)
        decoded_data = base64.b64decode(self.spack['data'])
        dicts = serpent.loads(decoded_data)
        # load the dicts inside packet structure
        self.pack.iter = dicts['iter']
        self.pack.Tot_iters = dicts['Tot_iters']
        self.pack.Time = dicts['Time']
        self.pack.Switch = dicts['Switch']
        self.pack.Task = dicts['Task']
        self.pack.pImgs = deepcopy(dicts['pImgs'])
        self.pack.Imgs = deepcopy(dicts['Imgs'])
        self.pack.Fils = deepcopy(dicts['Fils'])
        self.pack.Rots = deepcopy(dicts['Rots'])
        self.pack.Corr = deepcopy(dicts['Corr'])


SRCwin = SRCWindow()
