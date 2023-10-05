# NAVevents.py>
# Library used for the graphical cycle of NAVIGATION TASK in the program
# Imported in Main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
# Author: Nhat Tien PHAN - INSA
###################################################################
import math
import os
from random import randint
import numpy as np
import pyglet

import input

import Pyro4 as pyro
pyro.config.COMPRESSION = True
pyro.config.DETAILED_TRACEBACK = True
pyro.config.SOCK_REUSE = True

from psychopy import visual, core, event
import serpent
import base64
from packet import Packet
from lslmarkers import *
from pytictoc import TicToc

from settings import set
from flightdir import flightdir

global NAVwin


class NAVWindow(visual.Window):
    def __init__(self):

        if len(set.mon) == 2:
            width, height = set.wsize[0]  # (720, 407)

            super(NAVWindow, self).__init__(size=(width, height), screen=set.NAVwin, fullscr=set.Fullscreen, color=(-1, -1, -1),
                                            allowGUI=True, title='UASOS: Navigation Task')
            iconFile = os.path.join("./imgs/isae_logo.png")
            icon = pyglet.image.load(filename=iconFile)
            self.winHandle.set_icon(icon)
        else:
            width, height = set.wsize[0]
            super(NAVWindow, self).__init__(size=(width, height), screen=0, fullscr=set.Fullscreen, color=(-1, -1, -1),
                                            allowGUI=True, title='UASOS: Navigation Task')
            iconFile = os.path.join("./imgs/isae_logo.png")
            icon = pyglet.image.load(filename=iconFile)
            self.winHandle.set_icon(icon)

        self.alive = True
        self.case = -5
        self.nexts = 99
        self.pause = False
        self.total_it = 0

        self.spack = None
        self.phase = 0
        self.pack = Packet()

        self.type_w = 'NAV'  # Window Type
        self.FDir = flightdir(self, type_m=self.type_w)
        self.LSLHldr = lslmarkers(type_m=self.type_w)
        self.NAVCh = lslchannel(name='HDGStream', channel_names=['Fdir HDG', 'Drone HDG'], channel_units=['deg', 'deg'])
        self.HDG = 0
        self.WPY = ['', (0, 0)]
        self.selected = False  # Flag for clicked WPY
        self.usr_WPY = ['', (0, 0)]  # Example WPY for init
        self.x_wpy = 0
        self.y_wpy = 0
        self.needleHDG = 0
        self.nHDG = 0
        self.dev = 0
        self.usr_nHDG = 0  # User-commanded nHDG
        self.cor_dir = -2  # -1 left/1 right the correct dir/-2 not available
        self.usr_dir = 0  # user direction given
        self.map_y = 0
        self.map_x = 0
        self.fs = input.fstick()
        self.mouse = event.Mouse(visible=False, win=self)  # newPos=(0,0)
        self.last_fs = None  # Last value from FlightStick
        self.langue = 'fr'
        self.l_config = False
        self.ts_fstick = None
        self.te_fstick = None
        self.ts_mouse = None
        self.te_mouse = None
        self.exp_step = 0
        self.RT = 0
        self.cycle = 0
        self.accumulate = 0.0
        # Timers
        self.t = TicToc()
        self.RTt = TicToc()

        self.devices = [False, False]  # 0 - Mouse used, 1 - Fstick used
        self.max_dir = 0
        self.cor_WPY = 0
        self.ov_WPY = 0
        self.WPYcorr = -1  # WPY correct 1 / not correct 0
        self.pos_updated = False  # Flag to not operate the position update more than once
        self.WPY_dHDG = [-45, -23, +23, +45, -68, -45, +45, +68, -113, -135, +135, +113, -135, -158, +158, +135]
        self.fake_wpy = 'M13'

        self.toll = 0.1
        self.dTIME = 3
        self.mvHDG = 16 * (np.pi / 180)  # Based on MQ-1 Turn Time: 22s (WarThunder)
        self.dir = 0
        self.scale = 2
        self.delay_taken = False
        self.NAVLatency = 0
        self.duration = 0
        self.last_TASK = 0

        self.backup = False
        self.inject = False
        self.back_step = 0
        self.back_case = -5
        self.extra_time = 0

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

    def update_stim(self, change, exp_it, mode=None):
        import NAVstimuli as stim
        # REMEMBER THE ERROR: NEVER REUSE TOO MUCH THE TEXTSTIMs
        # They will not change, if you change often or rapidly the text inside, use more objects!
        # Link: https://discourse.psychopy.org/t/failing-to-update-text-element-via-code-snippets/26796
        if change:
            OK = False
            if stim.map.mrk.alive is True:
                stim.map.mrk.disable_marker()
            if self.pack.Task in [5, 6]:
                self.FDir.led_on()
                self.FDir.item_change(self.pack.Task)
                if self.pack.Task == 5:
                    stim.map.get_labels(x=self.map_x % 5824, y=self.map_y % 5824)

                    self.LSLHldr.send_mrk(typ='HDG', wht=self.pack.HDG, B=1, it=exp_it)
                    self.fake_wpy = self.get_rand_WPY(self.map_x, self.map_y)
                    self.LSLHldr.send_mrk(typ='WPY', wht=self.fake_wpy, B=0, it=exp_it)
                    stim.map.HDG_Ttxt.text = f'{self.pack.HDG}'
                    stim.map.WPY_Ftxt.text = self.fake_wpy
                if self.pack.Task == 6:
                    stim.map.get_labels(x=self.x_wpy % 5824, y=self.y_wpy % 5824)  # Update the frozen labels for the wpy selection
                    hdg = self.get_rand_HDG(round(self.HDG))
                    # x = deepcopy(stim.map.x_lbls)  # DEBUG
                    # y = deepcopy(stim.map.y_lbls)  # DEBUG
                    while not OK:  # Crosscheck of existance of WPY in the map
                        self.WPY = self.pkproxy.gen_WPY_instant(x_lbl=stim.map.x_lbls, y_lbl=stim.map.y_lbls, it=exp_it, case=self.case)
                        OK = self.check_WPY(x_lbls=stim.map.x_lbls, y_lbls=stim.map.y_lbls, WPY=self.WPY[0], WPY_tuple=self.WPY[1])
                    stim.map.HDG_Ftxt.text = f'{hdg}'
                    stim.map.WPY_Ttxt.text = self.WPY[0]
                    self.LSLHldr.send_mrk(typ='HDG', wht=hdg, B=0, it=exp_it)
                    self.LSLHldr.send_mrk(typ='WPY', wht=self.WPY[0], B=1, it=exp_it)
                    self.ov_WPY += 1
            else:
                stim.map.get_labels(x=self.map_x % 5824, y=self.map_y % 5824)
                hdg = self.get_rand_HDG(round(self.HDG))
                self.fake_wpy = self.get_rand_WPY(self.map_x, self.map_y)
                stim.map.HDG_Ftxt.text = f'{hdg}'
                stim.map.WPY_Ftxt.text = self.fake_wpy
                self.LSLHldr.send_mrk(typ='WPY', wht=self.fake_wpy, B=0)
                self.LSLHldr.send_mrk(typ='HDG', wht=hdg, B=0)
                self.FDir.item_change(0)
                self.FDir.led_off()

        if self.pack.Task == 6:
            stim.update_map(self.map_x, self.map_y, self.HDG, self.x_wpy, self.y_wpy, freeze=True)
        else:
            stim.update_map(self.map_x, self.map_y, self.HDG)

    def on_draw(self):
        self.render()

    def render(self):
        from NAVstimuli import map
        if self.case in [1, 3, 4]:
            map.draw(task=self.pack.Task)
            if self.case in [3, 4]:  # Only for training phase
                if self.pack.Task == 5:
                    if self.cor_dir == -2 or self.usr_dir == -2:
                        self.FDir.make_na()
                    elif self.cor_dir != -2 and self.usr_dir != -2:
                        if self.cor_dir == self.usr_dir:
                            self.FDir.make_correct()
                        else:
                            self.FDir.make_wrong()
                else:
                    self.FDir.make_na()
                self.FDir.hdg_devv.text = f'{round(self.dev)}°'
                self.FDir.RT_val.text = f'{round(self.RT)} ms'
                self.FDir.Good_tgtv.text = f'{self.cor_WPY}'
                self.FDir.Total_tgtv.text = f'{self.ov_WPY}'
            self.FDir.draw(case=self.case, nexts=self.nexts)
            if abs(self.needleHDG) < 0.1:
                map.mrk.disable_marker()
        elif self.case not in [1, 3, 4]:
            self.nexts = self.FDir.draw(case=self.case, nexts=self.nexts)
        else:
            pass
        self.flip()
        self.getFutureFlipTime()
        self.check_status()  # Just to let survive the server: it's a harsh way

    def run(self):
        import NAVstimuli as stim

        self.check_status()
        if self.backup is False:
            self.request_pkg(it=0, case=3 if self.back_case is None else self.back_case)  # request first iteration ever
            self.exp_step = 1
        if self.backup is True:
            self.request_pkg(it=1, case=self.back_case)
            self.exp_step = 2
        stim.draw_map()
        self.mouse.getPos()
        # All the clocks here will be unified in the core clock of Pyro Server
        elapsed_time = -1
        self.exp_step = 1
        pack = [2, 3, 4, 1]
        p_idx = 0
        p_once = False
        once = False  # For blocking a current freezing of the coords
        changed = False
        self.duration = self.pack.Time  # msec
        react_once = False  # Reaction clock flag
        press_once = False  # Mouse click just once
        self.ts_mouse = 0  # Start mouse usage timestamp
        self.te_mouse = 0  # End mouse usage timestamp
        self.ts_fstick = 0  # Start mouse usage timestamp
        self.te_fstick = 0  # End mouse usage timestamp
        print('NAVWin Charged')
        while self.alive:
            self.t.tic()
            self.cycle += 1
            if self.backup is True and self.inject is False:
                if self.case in [1, 2, 3, 4]:
                    p_idx = pack.index(self.case)
                elif self.case == -4:  # SRC
                    p_idx = pack.index(2)
                elif self.case == -3:  # NAV
                    p_idx = pack.index(3)
                elif self.case == -2:  # OV
                    p_idx = pack.index(4)
                elif self.case in [-1, 0]:  # main
                    p_idx = pack.index(1)
                if self.back_step != 0:
                    self.request_pkg(it=1, case=pack[p_idx])
                else:
                    self.request_pkg(it=0, case=pack[p_idx])
                self.exp_step = 2 if self.back_step != 0 else 1
                self.duration = self.pack.Time
                self.update_stim(change=True, exp_it=self.exp_step)
                if self.case in [1, 2, 3, 4]:
                    self.case = 6
                    self.pause = True
                self.inject = True

            # Update of the packet
            if elapsed_time >= self.duration and self.case in [1, 3, 4] and self.exp_step <= self.total_it:
                self.last_TASK = self.pack.Task
                self.send_pkg()  # I send the packet here!
                #-- RESET PARAMS
                self.reset_params()
                #-- RESET PARAMS
                # -- mouse reset --
                check = self.mouse.getPos()
                t_check = (check[0], check[1])
                if t_check != stim.map.mouse_pos:
                    self.mouse.setVisible(visible=False)
                    self.mouse.setPos(stim.map.mouse_pos)  # mouse reset
                    self.mouse.setVisible(visible=False)
                # -- mouse reset --
                self.request_pkg(self.exp_step)
                self.last_TASK = self.pack.Task
                self.duration = self.pack.Time
                if self.pack.Task == 6 and not once:  # Freezing the coordinates
                    self.x_wpy = self.map_x
                    self.y_wpy = self.map_y
                    stim.map.get_labels(x=self.x_wpy % 5824, y=self.y_wpy % 5824)  # Update the frozen labels for the wpy selection
                    once = True
                # Reset timers
                self.RTt.tic()
                changed = True if self.case != 8 else False
                react_once = False
                press_once = False
            else:
                pass

            # Controls of the experiment
            if self.case in [1, 3, 4]:
                if self.exp_step != 0 and changed is True:
                    self.update_stim(change=True, exp_it=self.exp_step-1)
                    self.render()
                elif self.exp_step == 0 and changed is True:
                    self.update_stim(change=True, exp_it=self.exp_step)
                    self.render()
                self.pos_updated = False
                # Add Trackball
                if self.mouse.mouseMoved():
                    if self.devices[1] is True:
                        self.devices[1] = False
                    if self.devices[0] is False:
                        self.ts_mouse = self.pkproxy.check_tstamp()
                        self.devices[0] = True
                        self.LSLHldr.send_mrk(typ='MOV', wht=self.devices[0], it=self.pack.iter - 1)
                    self.mouse.setVisible(visible=True)
                    self.te_mouse = self.pkproxy.check_tstamp()
                else:
                    if self.mouse.getPressed()[0] and press_once is False:
                        for i in range(0, 16):
                            if self.mouse.isPressedIn(stim.map.tiles[i].rect) is True:
                                # -- React Time
                                self.RT = self.RTt.tocvalue()*1000 if react_once is False else self.RT
                                react_once = True
                                press_once = True
                                # -- React Time
                                pos = stim.map.tiles[i].rect.pos
                                self.te_mouse = self.pkproxy.check_tstamp()
                                self.sel_WPY(x_lbls=stim.map.x_lbls, y_lbls=stim.map.y_lbls, WPY_tuple=stim.map.tiles[i].value, WPY=self.WPY)
                                if self.exp_step != 0:
                                    self.LSLHldr.send_mrk(typ='UPY', wht=self.usr_WPY[0], B=self.WPYcorr, it=self.exp_step - 1)
                                else:
                                    self.LSLHldr.send_mrk(typ='UPY', wht=self.usr_WPY[0], B=self.WPYcorr, it=self.exp_step)
                                self.selected = True
                                stim.map.mrk.set_pos(x=pos[0], y=pos[1])
                                self.nHDG = round(self.HDG + self.WPY_dHDG[i]) % 360
                                self.needleHDG = round(self.WPY_dHDG[i])
                                stim.update_needle(self.needleHDG)
                                break
                    stim.update_needle(self.needleHDG)
                    if self.pkproxy.check_tstamp() - self.te_mouse > 600 and press_once is False:  # 2 sec delay
                        self.te_mouse = self.pkproxy.check_tstamp() - 600
                        # Send here lsl marker with its -0.6s timestamp
                        if self.devices[0] is True:
                            self.devices[0] = False
                            self.LSLHldr.send_mrk(typ='MOV', wht=self.devices[0], it=self.pack.iter - 1, cut_seconds=0.6)


                # Add FlightStick
                if self.fs.get_finput(0.2) is True:
                    # -- React Time
                    self.RT = self.RTt.tocvalue()*1000 if react_once is False else self.RT
                    react_once = True
                    # -- React Time
                    if self.devices[0] is True:
                        self.devices[0] = False
                        stim.map.mrk.disable_marker()
                    if self.devices[1] is False:
                        self.ts_fstick = self.pkproxy.check_tstamp()
                        self.devices[1] = True
                        self.LSLHldr.send_mrk(typ='FLT', wht=self.devices[1], it=self.pack.iter - 1)
                    # Fstick is working
                    self.needleHDG = round(self.needleHDG + self.fs.deg)
                    self.nHDG = round(self.HDG + self.needleHDG) % 360
                    self.usr_nHDG = self.nHDG
                    #-- Catch the nHDG in the packet transmission
                    if abs(self.fs.deg) > abs(self.max_dir):
                        self.max_dir = self.fs.deg
                        self.dir = int(math.copysign(1, self.max_dir))
                        # -- Catch the direction
                        self.usr_dir = self.dir
                    stim.update_needle(self.needleHDG)
                else:
                    if self.devices[1] is True:
                        self.te_fstick = self.pkproxy.check_tstamp()
                        if self.pack.Task == 5:
                            self.dev = (self.pack.HDG - self.usr_nHDG) # % 180
                        self.devices[1] = False
                        self.LSLHldr.send_mrk(typ='FLT', wht=self.devices[1], it=self.pack.iter - 1)
                        self.LSLHldr.send_mrk(typ='UDG', wht=self.usr_nHDG, it=self.pack.iter - 1)
                    if abs(self.nHDG-self.HDG) < self.toll and self.devices[1] is False:
                        # Reset Condition
                        self.dir = 0
                        self.max_dir = 0.0
                    if self.pkproxy.check_tstamp() - self.te_fstick > 0.5 and self.pos_updated is False and stim.map.mrk.alive is False:
                        self.pos_updated = self.get_pos(x=self.map_x, y=self.map_y, HDG=self.HDG, nHDG=self.nHDG,
                                                        dir=self.dir, dt=10, dTIME=self.dTIME)
                        stim.update_needle(self.needleHDG)


                if self.pos_updated is False and stim.map.mrk.alive is False:
                    self.pos_updated = self.get_pos(x=self.map_x, y=self.map_y, HDG=self.HDG, nHDG=self.HDG,
                                                    dir=0, dt=10, dTIME=self.dTIME)
                elif self.pos_updated is False and stim.map.mrk.alive is True:
                    self.pos_updated = self.get_pos(x=self.map_x, y=self.map_y, HDG=self.HDG, nHDG=self.nHDG,
                                                    dir=0, dt=10, dTIME=self.dTIME)

                self.NAVCh.push_it([self.nHDG, self.HDG])

            # This charges the next packet or closes the experiment
                if changed:
                    if (self.exp_step <= self.total_it - 1 and self.case != self.back_case) or (self.exp_step < self.total_it - 1 and self.backup is True and self.case == self.back_case):
                        self.exp_step += 1
                        changed = False
                        once = False
                        p_once = False
                    elif (self.exp_step == self.total_it and self.case != self.back_case) or (self.exp_step == self.total_it and self.backup is True and self.case == self.back_case):
                        self.exp_step += 1
                        self.last_TASK = self.pack.Task
                        self.duration += 7000
                        self.pack.Time = self.duration
                        changed = False
                        once = False
                    else:  # Override of the stop condition
                        if self.case in [2, 3, 4]:
                            self.case = 8
                        elif self.case == 1:
                            self.case = 5  # Thank you

            if self.case == 8 and not p_once:
                self.exp_step = 0
                self.delay_taken = False
                elapsed_time = 0
                self.reset_all()
                p_idx += 1
                self.request_pkg(self.exp_step, pack[p_idx])
                self.duration = self.pack.Time
                self.update_stim(change=False, exp_it=self.exp_step)
                self.exp_step = 1
                self.RTt.tic()
                p_once = True

            self.update_stim(change=False, exp_it=self.exp_step)
            if self.duration != 0 and self.pause is False:  # we don't want to have updates where we are in waiting
                self.render()
                elapsed_time = self.pkproxy.check_tstamp()  #self.pkproxy.get_time() * 1000 - self.NAVLatency  # Cleaned of the latency build-up
            else:
                self.render()

            # Mean version
            self.accumulate += self.t.tocvalue()*1000  # Accumulate the time for cycle
            self.NAVLatency = self.accumulate/self.cycle - (1/60*1000)

    def get_rand_WPY(self, x, y):
        from NAVstimuli import map

        seed1 = randint(0, 3)
        seed2 = randint(0, 3)

        # # Generate the waypoint from the randomized value
        if map.y_lbls[seed2] in range(1, 10):
            numWPY = f'0{map.y_lbls[seed2]}'
        else:
            numWPY = f'{map.y_lbls[seed2]}'

        return map.x_lbls[seed1]+numWPY

    def get_rand_HDG(self, HDG):
        nHDG = int(HDG)
        while nHDG == int(HDG):
            nHDG = randint(0, 35)*10
        return nHDG

    def get_pos(self, x, y, HDG, nHDG, dir, dt, dTIME, V=313/3.6, call=None):
        # Objective: from last iteration (or from iteration 0), calculate the x,y coords and HDG in the fastest way possible
        # Enter: Aeronautical HDG
        # CONVERT TO MATH HEADING
        # Exit: Aeronautical HDG
        # Pos 0 - x, Pos 1 - y, Pos 2 - HDG
        # Acquire the turn speed
        vdHDG = self.calc_vHDG(HDG, nHDG, dir, dTIME)
        # Define the speed components
        u = V * np.cos(self.mathHDG(HDG) * np.pi / 180)
        v = V * np.sin(self.mathHDG(HDG) * np.pi / 180)
        # Calculate the positions
        x = x + u * dt/1000 * self.scale
        y = y + v * dt/1000 * self.scale
        # Calculate the HDG
        HDG = HDG + (vdHDG[0] * (dt/1000)) * (180 / np.pi)
        # Pack it up
        self.map_x = x
        self.map_y = y
        self.HDG = HDG % 360
        self.needleHDG -= (vdHDG[0] * (dt/1000)) * (180 / np.pi)
        return True

    # COMPLETE WHEN TIEN WILL FINISH

    def calc_vHDG(self, HDG, nHDG, dir, dTIME):
        # Enter Aeronautical Heading
        # pos 0 - vHDG, pos 1 - dHDG
        # Needs rework to acquire the direction of the stick
        rdHDG = (nHDG - HDG) % 360  # Right turn dHDG
        ldHDG = (360 - rdHDG)  # Left turn dHDG

        if dir < 0:  # Case Left Turn
            dHDG = ldHDG
            vHDG = - self.mvHDG #(dHDG * (np.pi / 180)) / abs(dTIME)
        elif dir > 0:  # Case Right Turn
            dHDG = rdHDG
            vHDG = self.mvHDG #(dHDG * (np.pi / 180)) / abs(dTIME)
        else:  # Straight flight or WPY mode
            if abs(nHDG - HDG) > self.toll:  # WPY Case
                if rdHDG > ldHDG: # Go left
                    dHDG = ldHDG
                    vHDG = - self.mvHDG #(dHDG * (np.pi / 180)) / abs(dTIME)
                else:  # Go right
                    dHDG = rdHDG
                    vHDG = self.mvHDG #(dHDG * (np.pi / 180)) / abs(dTIME)
            else:  # Straight flight
                dHDG = 0
                vHDG = 0

        if abs(vHDG) > self.mvHDG:
            if vHDG < 0:
                vHDG = -self.mvHDG
            elif vHDG > 0:
                vHDG = self.mvHDG

        out_vHDG = [vHDG, dHDG]  # The direction is inside here
        return out_vHDG

    def mathHDG(self, HDG):
        return 90 - HDG

    def check_status(self):
        from NAVstimuli import map
        from local import langue
        # Function that checks the Pyro Server status
        stat = self.pkproxy.check_status()
        dec_stat = base64.b64decode(stat['data'])
        d_stat = serpent.loads(dec_stat)
        # load the status
        if d_stat['init'] is not False and d_stat['case'] is not None:
            self.case = d_stat['case']
            if d_stat['type'] == 'BACKUP' and self.backup is False:
                self.back_step = d_stat['step']
                self.extra_time = d_stat['time']
                self.cor_WPY = d_stat['corWPY'] if d_stat['corWPY'] is not None else 0
                self.ov_WPY = d_stat['OvWPY'] if d_stat['OvWPY'] is not None else 0
                if self.case in [1, 2, 3, 4]:
                    self.back_case = self.case
                elif self.case == -3:
                    self.back_case = 3
                elif self.case == -2:
                    self.back_case = 4
                elif self.case in [-1, 0]:
                    self.back_case = 1
                self.backup = True
            self.nexts = d_stat['nexts']
            self.pause = d_stat['pause']
            if d_stat['langue'] != 'fr' and not self.l_config:
                self.langue = d_stat['langue']
                langue.set_language(lang=self.langue)
                self.FDir.update_graphics(type_m='NAV')
                self.l_config = True

        # send back the current status
        self.pkproxy.send_status(HDG=self.HDG, x_lbl=map.x_lbls, y_lbl=map.y_lbls)

        return

    def request_pkg(self, it: int, case=None):
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
            if self.backup is True and self.case == self.back_case:
                self.pack.Tot_iters = dicts['Tot_iters'] - self.back_step
            else:
                self.pack.Tot_iters = dicts['Tot_iters']
            self.total_it = self.pack.Tot_iters
            self.pack.Time = dicts['Time']
            self.pack.delta_t = dicts['delta_t']
            self.pack.Switch = dicts['Switch']
            self.pack.Task = dicts['Task']
            self.pack.HDG = dicts['HDG']
            if self.pack.Task == 5:
                self.cor_dir = self.check_dir(nHDG=self.pack.HDG, HDG=self.nHDG)
        elif it == self.total_it:
            if self.case in [2, 3, 4]:
                self.case = 8  # Command the end of phase
            elif self.case == 1:
                self.case = 5

    def send_pkg(self):
        # Function for sending the packet to the server to print
        if self.backup is True and self.case == self.back_case:
            self.pack.Time += self.extra_time
        self.pack.INorOUT = 2  # It defines the package from SRCTask
        self.pack.nRT = self.RT
        self.pack.NAVLatency = self.NAVLatency
        self.pack.case = self.case
        if self.case in [2, 3, 4]:
            self.pack.phase = 0
        elif self.case == 1:
            self.pack.phase = 1

        if self.ts_fstick != 0 and self.te_fstick != 0:
            self.pack.fstick_ON = 1  # Fstick used 1 / Not used 0
            self.pack.ts_fstick = self.ts_fstick  # Clock Time of the last fstick stroke / first fstick stroke
            self.pack.te_fstick = self.te_fstick
            if self.backup is True and self.case == self.back_case:
                self.pack.ts_fstick += self.extra_time
                self.pack.te_fstick += self.extra_time
            self.pack.usrHDG = self.usr_nHDG  # Just will show the HDG as integer
            self.pack.usrDIR = self.usr_dir  # User Direction

            if self.pack.HDG != -1:
                self.pack.dev = (self.pack.HDG - self.usr_nHDG) % 180  # -180/+180 range
            else:
                self.pack.dev = 'NaN'
        self.pack.corDIR = self.cor_dir

        if self.WPY[1] != (0, 0) and self.pack.Task == 6:
            self.pack.WPY = self.WPY[0]
            self.pack.WPYTuple = self.WPY[1]

        if self.ts_mouse != 0 and self.te_mouse != 0:
            self.pack.mouse_ON = 1  # Mouse used 1 / Not used 0
            self.pack.ts_mouse = self.ts_mouse  # Clock Time of the mouse movement
            self.pack.te_mouse = self.te_mouse
            if self.backup is True and self.case == self.back_case:
                self.pack.ts_mouse += self.extra_time
                self.pack.te_mouse += self.extra_time
            if self.usr_WPY[1] != (0, 0):
                self.pack.usr_WPY = self.WPY[0]  # None if not selected, value if selected
                self.pack.usr_WPYTuple = self.WPY[1]

        self.pack.WPYcorr = self.WPYcorr  # -1 Not Answered / 0 Wrong / 1 Correct
        self.pack.cor_WPY = self.cor_WPY  # No of correct WPY
        self.pack.Ovcor_WPY = self.ov_WPY  # No of shown WPYs

        # Send the packet
        out_pkg = serpent.dumps(self.pack)
        self.pkproxy.thread_send(out_pkg)

    def reset_all(self):
        import NAVstimuli as stim
        self.HDG = 0
        self.nHDG = 0
        self.cor_WPY = 0
        self.ov_WPY = 0
        self.last_TASK = 0
        self.duration = 0
        self.NAVLatency = 0
        self.needleHDG = 0
        self.map_x = 0
        self.map_y = 0
        stim.update_needle(self.needleHDG)
        self.update_stim(change=False, exp_it=0)
        self.pkproxy.send_status(HDG=self.HDG)

    def check_WPY(self, x_lbls, y_lbls, WPY_tuple, WPY):
        cWPY = f"{x_lbls[WPY_tuple[0]-1]}{y_lbls[WPY_tuple[1]-1]}"
        if cWPY == WPY:
            return True
        else:
            return False

    def sel_WPY(self, x_lbls, y_lbls, WPY_tuple, WPY):
        # Function that will compose the WPY based on clicked tile, it should have also LSL Marker send
        self.usr_WPY[0] = f"{x_lbls[WPY_tuple[0]-1]}{y_lbls[WPY_tuple[1]-1]}"
        self.usr_WPY[1] = WPY_tuple
        if self.usr_WPY[0] == WPY[0]:
            self.WPYcorr = 1
            self.cor_WPY += 1
            return True
        else:
            self.WPYcorr = 0
            return False

    def check_dir(self, nHDG, HDG):
        if self.pack.Task == 5:
            if nHDG > HDG:
                aHDG = round(nHDG - HDG)
                bHDG = round((360 - nHDG) + HDG)
                if aHDG < bHDG:
                    return 1
                elif aHDG == 180 or bHDG == 180:
                    return 0
                else:
                    return -1

            elif nHDG < HDG:
                aHDG = round(HDG - nHDG)
                bHDG = round((360 - HDG) + nHDG)
                if aHDG < bHDG:
                    return -1
                elif aHDG == 180 or bHDG == 180:
                    return 0
                else:
                    return 1
        else:
            return -2

    def reset_params(self):
        self.usr_dir = -2
        self.RT = 0
        self.usr_nHDG = 0
        self.dev = 0
        self.usr_WPY = ['', (0, 0)]
        self.ts_mouse = 0
        self.te_mouse = 0
        self.ts_fstick = 0
        self.te_fstick = 0
        self.devices = [False, False]
        self.cor_dir = -2
        self.WPYcorr = -1
        # for navigation purposes
        self.max_dir = 0.0
        return


NAVwin = NAVWindow()
