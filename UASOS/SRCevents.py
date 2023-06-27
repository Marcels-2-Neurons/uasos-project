# SRCevents.py>
# Library used for the events callout in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import pyglet.image

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
        self.USER_ID = None
        self.duration = 0
        self.phase = 0  # 0 - Training Phase / 1 - Current Experiment
        self.alive = 1
        self.spack = None
        self.pack = Packet()

        # Persisting Parameters
        self.keyLog = [0 for _ in range(9)]
        self.RT = 0
        self.ACC = 0
        self.Tnum = [0,0]
        self.SRCLatency = 0
        self.good_choice = 0  # User good choices
        self.Ov_choice = 0  # All the user choices
        self.Ov_true = 0  # All the true values

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
                if self.keyLog[a] == 1 and Rects[a].hobj.opacity == 0.0:  # Case Selected, for DEBUG purposes
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
        usr = self.USER_ID
        self.pkproxy.set_USER_info(usr)
        exp_step = 0
        elapsed_time = -1  # msec
        self.duration = 0  # msec
        react_clock = core.Clock()
        # filetxt = open('latency_test.txt', 'w', newline='') # DEBUG PURPOSE: Latency Test
        while self.alive:

            if elapsed_time >= self.duration:
                self.send_pkg() # I send the packet here!
                react_clock.reset()  # Reset the Reaction Time clock!
                self.update_stim(exp_step, change=True)
                self.render()
                self.SRCLatency = (self.pkproxy.get_time() * 1000) - self.duration
                self.keyLog = [0 for _ in range(9)]
                changed = True
                # print('Image changed in ', "{:.3f}".format(elapsed_time), ' msec,', "{:.3f}".format(elapsed_time-self.duration), ' msec late.')
                # filetxt.write("{:.3f}".format(elapsed_time-self.duration)+'\n') # DEBUG PURPOSE: Latency Test
            else:
                pass

            # Keypress event should be within the refresh cycle
            key = input.get_num_keys()
            if key is not None and key not in ['s', 'escape']:
                self.keyLog[int(key)] = 1
                if self.count_ones(self.keyLog) == 1:  # I take the first and last keypresses
                    self.Tnum[0] = self.pkproxy.get_time() * 1000
                    self.RT = react_clock.getTime() * 1000  # Catch the Reaction Time
                else:
                    self.Tnum[1] = self.pkproxy.get_time() * 1000
            elif key == 'escape' or set.close is True:
                self.pkproxy.close(self.phase)  # Server Closing
                self.close()
                atexit.register(os.system("taskkill /f /im python.exe"))  # Guarantee the clean exit of the experiment
                core.quit()
            elif key == 's' and self.case == 0:  # routine for starting the experiment
                self.case = 1
                self.phase = 0  # TODO: early stage, Traning still not defined!
                self.duration = self.pack.Time
                elapsed_time = self.pkproxy.start_time() * 1000
                changed = False
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
                elapsed_time = self.pkproxy.get_time() * 1000
            else:
                self.render()

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

    def send_pkg(self):
        # Function for sending the packet to the server to print
        self.pack.USER_ID = self.USER_ID
        self.pack.INorOUT = 1  # It defines the package from SRCTask
        self.pack.UserType = deepcopy(self.keyLog)
        self.pack.RT = self.RT
        self.pack.SRCLatency = self.SRCLatency

        if self.pack.Switch == 3 and self.pack.Task in [1,4]:
            self.pack.Tnum = self.Tnum[0] # I take the one from the first keypress
        elif self.pack.Switch == 3 and self.pack.Task in [5,6]:
            self.pack.Tnum = self.Tnum[1]  # I take the one from the last keypress
        else:
            self.pack.Tnum = 0

        self.good_choice += self.count_match()
        self.pack.GoodCh = self.good_choice
        self.Ov_choice += self.count_ones(self.keyLog)
        self.pack.OvCh = self.Ov_choice
        self.Ov_true += self.count_ones(self.pack.Corr)
        self.pack.OvTrue = self.Ov_true
        # Send the packet
        out_pkg = serpent.dumps(self.pack)
        self.pkproxy.thread_send(out_pkg)

    def count_ones(self, vec):
        count=0
        for element in vec:
            if element == 1:
                count += 1
        return count

    def count_match(self):
        count = 0
        for e_C, e_User in zip(self.pack.Corr, self.pack.UserType):
            if e_C == 1 and e_User == 1:
                count += 1
        return count

SRCwin = SRCWindow()
