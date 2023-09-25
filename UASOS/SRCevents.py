# SRCevents.py>
# Library used for the graphical cycle of SEARCH TASK in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import signal
import sys
import pyglet

from pytictoc import TicToc
import questions
from input import keyBoard
from shutil import which
import Pyro4 as pyro
pyro.config.COMPRESSION = True
pyro.config.DETAILED_TRACEBACK = True
pyro.config.SOCK_REUSE = True

from psychopy import visual, core
import serpent
import base64
from copy import *
from packet import Packet
from lslmarkers import lslmarkers
import subprocess
import SRCstimuli as stim
from settings import set
from flightdir import flightdir
from mathandler import NORBd
from threading import Thread
from utilscsv import vas_utils
from questions import *

global SRCwin

def start_subp(command):
    process = subprocess.Popen(command)
    set.processes.append(process)
    return

def close_all():
    for process in set.processes:
        process.kill()

class SRCWindow(visual.Window):
    # Initialization of the class
    def __init__(self):
        if len(set.mon) == 2:
            width, height = set.wsize[1]  #(1280, 720)
            super(SRCWindow, self).__init__(size=(width, height), screen=set.SRCwin, fullscr=set.Fullscreen, color=(-1, -1, -1),
                                            allowGUI=True, title='UASOS: Search Task')
            iconFile = os.path.join("./imgs/isae_logo.png")
            icon = pyglet.image.load(filename=iconFile)
            self.winHandle.set_icon(icon)
        else:
            width, height = set.wsize[0]
            super(SRCWindow, self).__init__(size=(width, height), screen=0, fullscr=set.Fullscreen, color=(-1, -1, -1),
                                            allowGUI=True, title='UASOS: Search Task')
            iconFile = os.path.join("./imgs/isae_logo.png")
            icon = pyglet.image.load(filename=iconFile)
            self.winHandle.set_icon(icon)

        self.case = -5  # Case 0 - Start of the Experiment, in Hold / Case 1 - Experiment Routine
        self.type_w = 'SRC'  # Window Type
        self.setup_complete = False
        self.pause = None
        self.USER_ID = None
        self.duration = 0
        self.delta_t = 0
        self.alive = 1
        self.spack = None
        self.phase = 0
        self.pack = Packet()
        self.total_it = 0  # Casual number to start
        self.FDir = flightdir(self, type_m=self.type_w)
        self.LSLHldr = lslmarkers(type_m=self.type_w)
        self.newpics = False  # In order to command the IMG Markers
        self.charged = False  # It avoids the overcharging of markers
        self.nexts = 99  # Flag for switching phase-by-phase
        self.backup = False
        self.inject = False
        self.extra_time = None  # Time to add to the packet in case of backup
        self.back_case = -5  # Case to restart
        self.back_step = None
        # -- VAS --
        self.VASEnabled = False
        self.VAStime = 0
        self.VASClock = core.Clock()
        self.VASTstart = 0
        self.VASt1pause = 0
        self.VASpause = 0
        self.no_vas = 1
        self.VASinit = False
        self.checkVAS = False
        # -- VAS --
        # Hw start
        self.kb = keyBoard()
        self.t = TicToc()
        self.RTt = TicToc()
        self.cycle = 0
        self.accumulate = 0.0
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
        self.VAS_csv = vas_utils()
        # Execution order - It is the order of showing tutorial training etc...
        self.ex_order = [-5, -4, 2, -3, 3, -2, 4, -1, 0, 1, 5]  # Composition of the experiment
        self.last_pos = None  # Last index of the ex_order called, for pause purpose
        self.last_TASK = None
        self.last_IMGS = None

        # Pyro Client Init
        pyro4_path = which('pyro4-ns.exe')
        if pyro4_path:
            start_subp([pyro4_path])
            start_subp(["python", "pyro_server.py"])
        else:
            print('Please, install pyro4==4.82 through pip')
            sys.exit(1)
        # Wait for the server start up, cycle until the uri is obtained
        uri = None
        while uri is None:
            try:
                uri = pyro.locateNS().lookup("pyro_svr")
            except pyro.errors.NamingError:
                pass
        # Connect to the pyro server
        self.pkproxy = pyro.Proxy(uri)

        # Start NAVevents
        subprocess.Popen(["python", "-c", "from NAVevents import NAVwin; NAVwin.run()"])

        self.FDir.draw(case=self.case)
        self.flip()

    def update_stim(self, step, change):
        # Function that updates the images
        from SRCstimuli import Rects

        if change:
            # Reset opacity of the highlights
            for a in range(0, set.n_num * set.m_num):
                Rects[a].hobj.opacity = 0.0

            for pic in range(0, set.n_num * set.m_num):
                if step == 1 or self.pack.pImgs[pic] != self.pack.Imgs[pic]:
                    f_num = self.pack.Fils[pic]
                    if f_num == 0:  # None
                        Rects[pic].changeImg(self.pack.Imgs[pic])
                    elif f_num == 1:  # Gaussian
                        Rects[pic].changeImg(self.pack.Imgs[pic], rotate=self.pack.Rots[pic], gaussian=0.2)
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
    def render(self, update_step=None, do=False):
        # stimuli drawing
        from SRCstimuli import Rects
        diff = self.count_diff_imgs(self.pack.Imgs, self.pack.pImgs)
        if self.case in [1, 2, 4]:  # Removed 3 from here
            if self.case in [2, 4]:  # Only for Training phase
                self.FDir.RT_val.text = f"{round(self.RT)} ms"
                self.FDir.Good_tgtv.text = f"{self.good_choice}"
                self.FDir.Total_tgtv.text = f"{self.Ov_true}"
            for i in range(0, set.n_num * set.m_num):
                Rects[i].draw(case=self.case)
                if self.pack.Imgs[i] != self.pack.pImgs[i] and self.charged is False and do is True:
                    self.LSLHldr.send_mrk(typ='IMG', wht=i+1, A=int(NORBd.get_cat(self.pack.Imgs[i])), B=self.pack.Corr[i], it=update_step, end=False)  # Charging the batch of markers
                    self.charged = True if len(self.LSLHldr.bsample) == diff else False
                    self.newpics = True
            self.FDir.draw(case=self.case, nexts=self.nexts)
        elif self.case not in [1, 2, 4]:
            self.nexts = self.FDir.draw(case=self.case, nexts=self.nexts)

        self.flip()
        self.getFutureFlipTime()  # Code in-sync with the Monitor
        self.pkproxy.send_status(case=self.case, nexts=self.nexts, pause=self.pause)  # Just to let survive the server: it's a harsh way

    def run(self):
        # from stimuli import Rects
        # Graphical Runtime
        pos = 1
        p_once = False
        pack = [2, 3, 4, 1]
        p_idx = 0
        self.case = self.ex_order[pos]  # in order to grant the coherent execution
        self.start_case = False
        changed = False
        self.request_pkg(0)  # request first iteration ever
        stim.drw_matrix(Imgs=self.pack.Imgs)
        usr = self.USER_ID
        if self.backup is False:
            self.pkproxy.set_USER_info(usr)
        else:
            self.pkproxy.set_USER_info(usr, new=False)  # recover the printing
        exp_step = 0
        elapsed_time = -1  # msec
        self.duration = self.pack.Time  # msec
        print('SRCWin Charged')
        while self.alive:
            self.t.tic()
            self.cycle += 1
            # case of injection
            if self.backup is True and self.inject is False:
                pos = self.last_pos
                self.case = self.ex_order[self.last_pos]
                if self.case in [1, 2, 3, 4]:
                    p_idx = pack.index(self.case)
                    self.pkproxy.pause_time()
                    self.pause = True
                    self.case = 6
                elif self.case == -4:  # SRC
                    p_idx = pack.index(2)
                elif self.case == -3:  # NAV
                    p_idx = pack.index(3)
                elif self.case == -2:  # OV
                    p_idx = pack.index(4)
                elif self.case in [-1, 0]:  # main
                    p_idx = pack.index(1)
                self.request_pkg(it=1, case=self.back_case)
                self.duration = self.pack.Time
                self.delta_t = self.pack.delta_t
                self.update_stim(exp_step, change=True)
                exp_step = 2 if self.case in [1, 2, 3, 4] else 1
                self.render(do=True)
                self.inject = True

            if elapsed_time >= self.duration and self.case in [1, 2, 3, 4] and exp_step <= self.total_it:
                if self.case != 3:
                    self.send_pkg()  # I send the packet here!
                # RESET PARAMS
                self.Tnum = [0, 0]
                self.RT = 0
                self.SRCLatency = 0
                # RESET PARAMS
                if exp_step != 1:
                    self.last_IMGS = deepcopy(self.pack.Imgs)
                    self.last_TASK = self.pack.Task
                self.request_pkg(exp_step)
                self.duration = self.pack.Time
                # Timers restart
                self.t.tic()  # Start timer
                self.RTt.tic()  # Reset the Reaction Time clock!
                self.update_stim(exp_step, change=True)
                if exp_step != 0:
                    self.render(update_step=exp_step-1, do=True)
                else:
                    self.render(do=True)
                if self.newpics:
                    thread = Thread(target=self.exec_send)
                    thread.start()
                if self.last_TASK != self.pack.Task and self.pack.Task in [1, 4]:
                    self.keyLog = [0 for _ in range(9)]
                changed = True if self.case != 8 else False
            else:
                pass

            # Keypress event should be within the refresh cycle
            key = self.kb.get_num_keys()
            if key[0] is not None and key[0] not in ['s', 'escape'] and self.case in [1, 2, 3, 4]:
                self.keyLog[int(key[0])] = 1
                self.LSLHldr.send_mrk(typ='RES', wht=int(key[0])+1, A=self.pack.Task, B=self.pack.Corr[int(key[0])], it=self.pack.iter-1)  # Mark sending
                if self.count_ones(self.keyLog) == 1:  # I take the first and last keypresses
                    self.Tnum[0] = self.pkproxy.get_time() * 1000
                    self.RT = self.RTt.tocvalue()*1000 - key[1]  # Catch the Reaction Time - the response time of the keyboard
                else:
                    self.Tnum[1] = self.pkproxy.get_time() * 1000
            elif key[0] == 'escape' or set.close is True:
                self.pkproxy.close(self.phase)  # Server Closing
                if self.case == 5:
                    self.LSLHldr.send_mrk(typ='CLS')  # Correct execution
                else:
                    self.LSLHldr.send_mrk(typ='BRK', it=exp_step)  # Force closing
                close_all()
                self.close()
                core.quit()
            elif (key[0] == 's' or self.nexts == -1) and self.case != -5:  # routine for starting the experiment

                if self.nexts == -1 or self.case in [0, 8]:  # slide or end of phase
                    pos += 1
                    once = False
                    p_once = False
                    elapsed_time = 0  # Reset of the Time
                    exp_step = 0
                    self.pkproxy.start_time() * 1000  # Here the clock resets every time, it's normal!
                    self.pause = False
                    self.pkproxy.send_tstamp(elapsed_time)
                    self.last_pos = pos
                    self.case = self.ex_order[pos]
                    if self.case in [1, 2, 3, 4]:
                        self.start_case = False
                        self.request_pkg(exp_step)  # request first iteration ever
                        self.duration = self.pack.Time
                        self.LSLHldr.send_mrk(typ='SRT', wht=self.ex_order[self.last_pos])
                        self.update_stim(exp_step, change=True)
                        self.render(do=True)
                        # Timers Restart
                        self.RTt.tic()
                        exp_step = 1  # Reset of the Experiment Steps
                    self.nexts = 100

                if self.case in [-4, -3, -2, -1]:  # only in slide modes
                    self.nexts -= 1

                    # I need to put the pause case here
                if self.case in [1, 2, 3, 4, 6, 7] and self.pack.case != 8 and elapsed_time != 0:
                    if self.pause is False and self.checkVAS is False:  # This will be the pause case
                        self.pkproxy.pause_time()
                        self.pause = True
                        self.LSLHldr.send_mrk(typ='PSE', wht=self.pause, it=self.pack.iter - 1)
                        if self.case == 1 and self.VASEnabled is True:
                            self.VASt1pause = self.VASClock.getTime()
                        self.case = 6
                    elif self.pause is True and self.checkVAS is False:
                        elapsed_time = self.pkproxy.get_time() * 1000
                        self.pkproxy.send_tstamp(elapsed_time)
                        self.pause = False
                        self.LSLHldr.send_mrk(typ='PSE', wht=self.pause, it=self.pack.iter - 1)
                        if self.ex_order[self.last_pos] == 1 and self.VASEnabled is True:
                            self.VASpause += self.VASClock.getTime() - self.VASt1pause
                        if self.case == 6:
                            self.case = self.ex_order[self.last_pos]
                    elif self.checkVAS is True:
                        self.VASpause += self.VASClock.getTime() - self.VASt1pause
                        elapsed_time = self.pkproxy.get_time(dtime=(self.VASClock.getTime() - self.VASt1pause)) * 1000
                        self.pkproxy.send_tstamp(elapsed_time)
                        self.checkVAS = False
                        self.LSLHldr.send_mrk(typ='VAS', wht=self.checkVAS, it=self.pack.iter - 1)
                        if self.case == 7:
                            self.case = self.ex_order[self.last_pos]
                    else:
                        self.pause = False

                if self.case in [1, 2, 3, 4] and self.start_case is False:
                    elapsed_time = self.pkproxy.start_time() * 1000  # Here the clock resets every time, it's normal!
                    self.pkproxy.send_tstamp(elapsed_time)
                    changed = False
                    self.start_case = True
                    if self.case == 1 and self.VASinit is False and self.VASEnabled is True:
                        self.VASClock.reset()
                        self.VASt1pause = 0
                        self.VASpause = 0
                        self.VASinit = True
                        path = os.getcwd()
                        path = os.path.join(path, f"results\VAS_ID{self.USER_ID}.csv")
                        if self.backup is False or (self.backup is True and os.path.isfile(path) is False):
                            self.VAS_csv.start_VAS(usr=self.USER_ID, back=False)
                        else:
                            self.VAS_csv.start_VAS(usr=self.USER_ID, back=True)
            else:
                pass

            if self.VASEnabled is True and self.case == 1 and self.checkVAS is False and (self.VASClock.getTime() - self.VASpause) >= self.no_vas * self.VAStime * 60:
                self.pkproxy.pause_time()
                self.LSLHldr.send_mrk(typ='VAS', wht=self.checkVAS, it=self.pack.iter - 1)
                self.VASt1pause = self.VASClock.getTime()
                self.case = 7
                self.render()
                self.no_vas += 1
                self.checkVAS = True
                questions.vas_ingame(usr=self.USER_ID, hdlr=self.VAS_csv, iter=exp_step)

            # This charges the next packet or closes the experiment
            if changed:
                self.charged = False
                if (exp_step <= self.total_it-1 and self.case != self.back_case) or (exp_step < self.total_it - 1 and self.backup is True and self.case == self.back_case):
                    exp_step += 1
                    self.duration = self.pack.Time
                    self.delta_t = self.pack.delta_t
                    changed = False
                elif (exp_step == self.total_it and self.case != self.back_case) or (exp_step == self.total_it and self.backup is True and self.case == self.back_case):
                    exp_step += 1
                    self.last_TASK = self.pack.Task
                    self.last_IMGS = deepcopy(self.pack.Imgs)
                    self.duration += 7000
                    self.delta_t = 7000
                    self.pack.Time = self.duration
                    changed = False
                else:
                    if self.case in [2, 3, 4]:
                        self.case = 8
                    elif self.case == 1:
                        self.case = 5  # Thank you
                        self.render()
                        questions.subject_endform(id=self.USER_ID, lang=langue.lang)  # Last set of questions
                    exp_step = 0

            if self.case == 8 and not p_once:
                self.LSLHldr.send_mrk(typ='STP', wht=self.ex_order[self.last_pos])
                elapsed_time = 0
                self.pkproxy.send_tstamp(elapsed_time)
                self.pkproxy.reset_actual_delta()
                self.reset_all()
                p_idx += 1
                p_once = True
            self.update_stim(exp_step, change=False)

            if self.duration != 0 and self.pause is False and self.checkVAS is False:  # we don't want to have updates where we are in waiting
                self.render()
                elapsed_time = self.pkproxy.get_time() * 1000
                self.pkproxy.send_tstamp(elapsed_time)
            else:
                self.render()

            # Mean version
            self.accumulate += self.t.tocvalue()*1000
            self.SRCLatency = self.accumulate/self.cycle - (1/60*1000)


    def request_pkg(self, it,  case=None):
        # Function to retrieve the packet
        if self.pack:
            del self.pack
        self.pack = Packet()  # Reset of the packet
        if it <= self.total_it-1 or it == 0:
            if case is not None:
                self.spack = self.pkproxy.read_data(it=it, case=case)  # This will change the script from where to check
            else:
                self.spack = self.pkproxy.read_data(it=it, case=self.case)  # This will change the script from where to check
            decoded_data = base64.b64decode(self.spack['data'])
            dicts = serpent.loads(decoded_data)
            # load the dicts inside packet structure
            self.pack.iter = dicts['iter']
            self.pack.Tot_iters = dicts['Tot_iters']
            if self.backup is True and self.back_case == self.case:  # you are operating on the current case to restart
                self.total_it = self.pack.Tot_iters - self.back_step  # It will cut down just the actual steps not necessary
            else:
                self.total_it = self.pack.Tot_iters  # Normal case
            self.pack.Time = dicts['Time']
            self.pack.delta_t = dicts['delta_t']
            self.pack.Switch = dicts['Switch']
            self.pack.Task = dicts['Task']
            if self.backup is True and self.inject is False:
                pass
            else:
                self.pack.pImgs = deepcopy(dicts['pImgs'])
            self.pack.Imgs = deepcopy(dicts['Imgs'])
            self.pack.Fils = deepcopy(dicts['Fils'])
            self.pack.Rots = deepcopy(dicts['Rots'])
            self.pack.Corr = deepcopy(dicts['Corr'])
        elif it == self.total_it:
            if self.case in [2,3,4]:
                self.case = 8  # Command the end of phase
            elif self.case == 1:
                self.case = 5

    def send_pkg(self):
        # Function for sending the packet to the server to print
        self.pack.case = self.case
        if self.backup is True and self.case == self.back_case:
            self.pack.Time += self.extra_time
        self.pack.USER_ID = self.USER_ID
        self.pack.INorOUT = 1  # It defines the package from SRCTask
        self.pack.UserType = deepcopy(self.keyLog)
        self.pack.sRT = self.RT
        self.pack.SRCLatency = self.SRCLatency
        if self.case in [2, 3, 4]:
            self.pack.phase = 0
        elif self.case == 1:
            self.pack.phase = 1

        if self.Tnum[0] != 0:
            self.pack.num_ON = 1
            self.pack.ts_num = self.Tnum[0]  # I take the one from the first keypress
            self.pack.te_num = self.Tnum[1] if self.Tnum[1] != 0 else self.Tnum[0]  # I take the one from the last keypress

        self.good_choice += self.count_match()
        self.pack.GoodCh = self.good_choice
        self.Ov_choice += self.count_ones(self.keyLog)
        self.pack.OvCh = self.Ov_choice
        self.Ov_true += self.count_ones(self.pack.Corr)
        self.pack.OvTrue = self.Ov_true
        # Calculate ACC here
        if self.good_choice != 0 and self.Ov_true != 0:
            self.ACC = (self.good_choice/self.Ov_choice)
            self.pack.ACC = self.ACC
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
        if self.case in [1, 2, 4] and self.newpics:
            self.LSLHldr.send_mrk(typ='SND')  # Force Sending
            self.newpics = False
        return

    def reset_all(self):
        self.good_choice = 0
        self.Ov_true = 0
        self.Ov_choice = 0
        self.RT = 0
        self.ACC = 0

    def send_config(self, ans=None):
        if ans.type == 'FULL':
            self.VASEnabled = ans.VAS
            if self.VASEnabled is True:
                self.VAStime = ans.VAS_Time
            self.pkproxy.send_status(case=self.case, nexts=self.nexts, pause=False, langue=ans.lang)
        elif ans.type == 'BACKUP':
            self.backup = True
            if ans.case in [1, 2, 3, 4]:
                # add src config for backup, considering that the pos value of the ex_order should be set accordingly
                self.extra_time = ans.time  # time to add to the packet
                self.back_case = ans.case
                self.case = self.back_case
                self.back_step = ans.step
                self.good_choice = ans.Good_ch  # User good choices
                self.Ov_choice = ans.Ov_ch  # All the user choices
                self.Ov_true = ans.Ov_True  # All the true values
                self.VASEnabled = ans.VAS
                if self.VASEnabled is True:
                    self.VAStime = ans.VAS_Time
                self.last_pos = self.ex_order.index(ans.case)
                self.pkproxy.send_status(type='BACKUP', case=ans.case, step=ans.step, time=ans.time, corwpy=ans.corWPY, ovwpy=ans.OvWPY, nexts=self.nexts, pause=True, langue=ans.lang)
            elif ans.case not in [1, 2, 3, 4]:
                # add src config for backup, considering that the pos value of the ex_order should be set accordingly
                self.extra_time = 0
                if ans.case == -3:
                    self.back_case = 3
                elif ans.case == -2:
                    self.back_case = 4
                elif ans.case in [-1, 0]:
                    self.back_case = 1
                self.last_pos = self.ex_order.index(ans.case)
                self.VASEnabled = ans.VAS
                if self.VASEnabled is True:
                    self.VAStime = ans.VAS_Time
                self.good_choice = ans.Good_ch  # User good choices
                self.Ov_choice = ans.Ov_ch  # All the user choices
                self.Ov_true = ans.Ov_True  # All the true values
                self.back_step = 0
                self.pkproxy.send_status(type='BACKUP', case=ans.case, nexts=self.nexts, corwpy=ans.corWPY, ovwpy=ans.OvWPY, pause=False, langue=ans.lang)
            self.LSLHldr.send_mrk(typ='RST', it=self.back_step)


SRCwin = SRCWindow()
