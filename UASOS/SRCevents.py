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
from lslmarkers import lslmarkers
import subprocess
import stimuli as stim
from settings import set
from flightdir import flightdir
from mathandler import NORBd
from threading import Thread

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

        self.case = -5  # Case 0 - Start of the Experiment, in Hold / Case 1 - Experiment Routine
        self.type_w = 'SRC'  # Window Type
        self.setup_complete = False
        self.pause = None
        self.USER_ID = None
        self.duration = 0
        self.alive = 1
        self.spack = None
        self.phase = 0  # TODO: define the phase for writing on training or exp csv
        self.pack = Packet()
        self.total_it = 0  # Casual number to start
        self.FDir = flightdir(self, type_m=self.type_w)
        self.LSLHldr = lslmarkers(type_m=self.type_w)
        self.newpics = False  # In order to command the IMG Markers
        self.charged = False  # It avoids the overcharging of markers
        self.nexts = 99  # Flag for switching phase-by-phase
        # Persisting Parameters
        self.keyLog = [0 for _ in range(9)]
        self.RT = 0
        self.ACC = 0
        self.Tnum = [0, 0]
        self.SRCLatency = 0
        self.ovLat = 0
        self.good_choice = 0  # User good choices
        self.Ov_choice = 0  # All the user choices
        self.Ov_true = 0  # All the true values
        # Execution order - It is the order of showing tutorial training etc...
        self.ex_order = [-5, -4, 2, -3, 3, -2, 4, -1, 0, 1, 5]  # Composition of the experiment
        self.last_pos = None  # Last index of the ex_order called, for pause purpose
        self.last_TASK = None
        self.last_IMGS = None
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

        self.FDir.draw(case=self.case)
        self.flip()

    def update_stim(self, step, change):
        # Function that updates the images
        from stimuli import Rects

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

                    if self.keyLog[pic] == 1:  # This means that it was selected
                        self.keyLog[pic] = 0  # Reset of the selection
                        Rects[pic].no_hlight()
                else:
                    pass
            # Led activity changes just at every new step
            self.good_choice = self.pack.GoodCh
            self.ACC = self.pack.OvTrue - self.pack.GoodCh
            if self.pack.Task in [1, 4]:
                self.FDir.led_on()
                self.FDir.item_change(self.pack.Task)
            else:
                self.FDir.item_change(0)
                self.FDir.led_off()
        else:
            for a in range(0, set.n_num * set.m_num):
                if self.keyLog[a] == 1 and Rects[a].hobj.opacity == 0.0:  # Case Selected, for DEBUG purposes
                    Rects[a].highlight()

    # Drawing of the stimuli
    def on_draw(self):
        self.render()

    # Rendering of the stimuli
    def render(self, do=False):
        # stimuli drawing
        from stimuli import Rects
        diff = self.count_diff_imgs(self.pack.Imgs, self.pack.pImgs)
        if self.case in [1, 2, 3, 4]:
            if self.case in [2, 3, 4]:  # Only for Training phase
                self.FDir.RT_val.text = f"{round(self.RT)} ms"
                self.FDir.Good_tgtv.text = f"{self.good_choice}"
                self.FDir.Miss_tgtv.text = f"{self.ACC}"
            for i in range(0, set.n_num * set.m_num):
                Rects[i].draw(case=self.case)
                if self.pack.Imgs[i] != self.pack.pImgs[i] and self.charged is False and do is True:
                    self.LSLHldr.send_mrk(typ='IMG', wht=i+1, A=int(NORBd.get_cat(self.pack.Imgs[i])), B=self.pack.Corr[i], it=self.pack.iter, end=False)  # Charging the batch of markers
                    self.charged = True if len(self.LSLHldr.bsample) == diff else False
                    self.newpics = True
            self.FDir.draw(case=self.case, nexts=self.nexts)
        elif self.case not in [1, 2, 3, 4]:
            self.nexts = self.FDir.draw(case=self.case, nexts=self.nexts)
        self.flip()
        self.getFutureFlipTime()  # Code in-sync with the Monitor
        self.pkproxy.check_status()  # Just to let survive the server: it's a harsh way

    def run(self):
        # from stimuli import Rects
        # Graphical Runtime
        pos = 1
        once = False
        self.case = self.ex_order[pos]  # in order to grant the coherent execution
        changed = False
        self.request_pkg(0)  # request first iteration ever
        stim.drw_matrix()
        usr = self.USER_ID
        self.pkproxy.set_USER_info(usr)
        exp_step = 0
        elapsed_time = -1  # msec
        self.duration = 0  # msec
        react_clock = core.Clock()
        # filetxt = open('latency_test.txt', 'w', newline='') # DEBUG PURPOSE: Latency Test
        while self.alive:

            if elapsed_time >= self.duration and self.case in [1, 2, 3, 4] and exp_step <= self.total_it:
                self.send_pkg()  # I send the packet here!
                react_clock.reset()  # Reset the Reaction Time clock!
                self.update_stim(exp_step, change=True)
                self.render(do=True)
                if self.newpics:
                    thread = Thread(target=self.exec_send)
                    thread.start()
                self.SRCLatency = (self.pkproxy.get_time() * 1000) - self.duration
                if self.last_TASK != self.pack.Task and self.pack.Task in [1, 4]:
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
                self.LSLHldr.send_mrk(typ='RES', wht=int(key)+1, A=self.pack.Task, B=self.pack.Corr[int(key)], it=self.pack.iter-1)  # Mark sending
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
            elif key == 's' or self.nexts == -1:  # routine for starting the experiment

                if self.nexts == -1 or self.case == 8:  # slide or end of phase
                    pos += 1
                    once = False
                    elapsed_time = 0  # Reset of the Time
                    # TODO Request reset of the clock from here
                    exp_step = 0  # Reset of the Experiment Steps
                    self.last_pos = pos
                    self.case = self.ex_order[pos]
                    if self.case in [1, 2, 3, 4]:
                        self.LSLHldr.send_mrk(typ='SRT', wht=self.ex_order[self.last_pos])
                    self.nexts = 100

                if self.case in [-4, -3, -2, -1]:  # only in slide modes
                    self.nexts -= 1

                self.duration = self.pack.Time
                if self.case in [1, 2, 3, 4]:
                    elapsed_time = self.pkproxy.start_time() * 1000  # Here the clock resets every time, it's normal!
                    changed = False
                    # I need to put the pause case here
                if self.case in [1, 2, 3, 4, 6] and self.pack.case != 8:
                    if self.pause is False:  # This will be the pause case
                        self.pkproxy.pause_time()
                        self.pause = True
                        self.LSLHldr.send_mrk(typ='PSE', wht=self.pause, it=self.pack.iter-1)
                        self.case = 6
                    elif self.pause is True:
                        elapsed_time = self.pkproxy.get_time() * 1000 - self.SRCLatency
                        self.pause = False
                        self.LSLHldr.send_mrk(typ='PSE', wht=self.pause, it=self.pack.iter-1)
                        if self.case == 6:
                            self.case = self.ex_order[self.last_pos]
                    else:
                        self.pause = False

            else:
                pass

            # This charges the next packet or closes the experiment
            if changed:
                exp_step += 1
                self.charged = False

                if exp_step <= self.total_it-1:
                    self.last_TASK = self.pack.Task
                    self.last_IMGS = deepcopy(self.pack.Imgs)
                    self.request_pkg(exp_step)
                    self.duration = self.pack.Time
                    changed = False
                elif exp_step == self.total_it:
                    self.last_TASK = self.pack.Task
                    self.last_IMGS = deepcopy(self.pack.Imgs)
                    self.duration += 3500
                    self.pack.Time = self.duration
                    changed = False
                else:
                    if not once:
                        self.LSLHldr.send_mrk(typ='STP', wht=self.ex_order[self.last_pos])
                        once = True
                    self.case = 8

            self.update_stim(exp_step, change=False)

            if self.duration != 0 and self.pause is False:  # we don't want to have updates where we are in waiting
                self.render()
                elapsed_time = self.pkproxy.get_time() * 1000 - self.SRCLatency  # Cleaned of the latency build-up
            else:
                self.render()

    def request_pkg(self, it):
        # Function to retrieve the packet
        del self.spack
        del self.pack
        self.pack = Packet()  # Reset of the packet
        if it <= self.total_it-1 or it == 0:
            self.spack = self.pkproxy.read_data(self.case, it)  # This will change the script from where to check
            decoded_data = base64.b64decode(self.spack['data'])
            dicts = serpent.loads(decoded_data)
            # load the dicts inside packet structure
            self.pack.iter = dicts['iter']
            self.pack.Tot_iters = dicts['Tot_iters']
            self.total_it = self.pack.Tot_iters
            self.pack.Time = dicts['Time']
            self.pack.Switch = dicts['Switch']
            self.pack.Task = dicts['Task']
            self.pack.pImgs = deepcopy(dicts['pImgs'])
            self.pack.Imgs = deepcopy(dicts['Imgs'])
            self.pack.Fils = deepcopy(dicts['Fils'])
            self.pack.Rots = deepcopy(dicts['Rots'])
            self.pack.Corr = deepcopy(dicts['Corr'])
        elif it == self.total_it:
            self.case = 8  # Command the end of phase

    def send_pkg(self):
        # Function for sending the packet to the server to print
        self.pack.USER_ID = self.USER_ID
        self.pack.INorOUT = 1  # It defines the package from SRCTask
        self.pack.UserType = deepcopy(self.keyLog)
        self.pack.RT = self.RT
        self.pack.SRCLatency = self.SRCLatency
        self.pack.phase = self.phase
        self.pack.case = self.case

        if self.pack.Switch == 3 and self.pack.Task in [1, 4]:
            self.pack.Tnum = self.Tnum[0]  # I take the one from the first keypress
        elif self.pack.Switch == 3 and self.pack.Task in [5, 6]:
            self.pack.Tnum = self.Tnum[1]  # I take the one from the last keypress
        else:
            self.pack.Tnum = 0

        self.good_choice += self.count_match()
        self.pack.GoodCh = self.good_choice
        self.Ov_choice += self.count_ones(self.keyLog)
        self.pack.OvCh = self.Ov_choice
        self.Ov_true += self.count_ones(self.pack.Corr)
        self.pack.OvTrue = self.Ov_true
        # Calculate ACC here
        if self.good_choice != 0 and self.Ov_true != 0:
            self.ACC = (self.good_choice/self.Ov_choice)
        # Send the packet
        out_pkg = serpent.dumps(self.pack)
        self.pkproxy.thread_send(out_pkg)

    def count_ones(self, vec):
        count = 0
        for element in vec:
            if element == 1:
                count += 1
        return count

    def count_diff_imgs(self, Imgs, pImgs):
        count = 0
        for n1, n2 in zip(Imgs, pImgs):
            if n1 != n2:
                count += 1
        return count

    def count_match(self):
        count = 0
        for e_C, e_User in zip(self.pack.Corr, self.pack.UserType):
            if e_C == 1 and e_User == 1:
                count += 1
        return count

    def exec_send(self):
        if self.case in [1, 2, 3, 4] and self.newpics:
            self.LSLHldr.send_mrk(typ='SND')  # Force Sending
            self.newpics = False
        return


SRCwin = SRCWindow()
