# pyro_server.py>
# Library used for opening Pyro4 server that will hold the script
# generated by scriptgen.py
# It starts from SRCTask as separated instance, SRCTask and NAVTask
# will hold in listening until the connection is established
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
# import os
# os.environ["PYRO_STORAGE "] = "./logs/"
# os.environ["PYRO_LOGFILE"] = "PyroLog.log"
# os.environ["PYRO_LOGLEVEL"] = "DEBUG"

import Pyro4 as pyro
pyro.config.SERVERTYPE = 'multiplex'
pyro.config.COMPRESSION = True
pyro.config.DETAILED_TRACEBACK = True
pyro.config.SOCK_REUSE = True

import serpent
import base64
import threading
import psutil
from utilscsv import *
from copy import *
from packet import *
from scriptgen import script, script_s, script_n, script_ov


@pyro.expose
class PyroServer:
    def __init__(self):
        # initialize just the values but not start the server on init for now
        # Solve TIMEOUT issue:

        self.timeout_value = 86400  # 1yr in seconds

        self.server_up = False
        self.scr_dir = [script, script_s, script_n, script_ov]
        # Main important experiment status data
        self.case = None
        self.step = 0
        self.time = 0
        self.langue = 'fr'
        self.nexts = 99
        self.HDG = 0
        self.corWPY = 0
        self.OvWPY = 0
        self.x_lbl = None
        self.y_lbl = None
        self.pause = None
        self.USER_ID = None
        self.status = status()

        self.file = None
        self.t_file = None
        self.backup = None
        self.type = 'FULL'

        self.MlastPacket = Packet()
        self.SRClastPacket = Packet()
        self.NAVlastPacket = Packet()
        self.clock = cClock()
        self.exp_time = 0
        self.SRCPackOUT = False
        self.NAVPackOUT = False  # Init as both False, for now the NAV Packet is faked as arrived
        self.csv_prt = utilscsv()

        while not self.server_up:
            if len(self.scr_dir) != 0:  # It somehow waits the generation of the objects
                self.daemon = pyro.Daemon()
                self.uri = self.daemon.register(self)
                self.name_src = pyro.locateNS()
                self.name_src.register("pyro_svr", self.uri)

                self.server_up = True
                self.daemon.requestLoop()

    @pyro.expose
    def set_USER_info(self, USER_ID, new=True):
        self.csv_prt.USER_ID = USER_ID
        self.USER_ID = USER_ID
        if new is True:
            self.csv_prt.setup_out()
        else:
            self.csv_prt.take_files(t_file=self.t_file, file=self.file)
        return

    @pyro.expose
    def load_files(self, t_file=None, file=None):
        self.t_file = t_file
        self.file = file
        return

    @pyro.expose
    def close(self, phase):
        # self.daemon.shutdown()
        # if phase == 0:  # Close both result files
        #     self.csv_prt.close_file(0)
        #     self.csv_prt.close_file(1)
        # elif phase == 1:  # Close the last result file remained
        #     self.csv_prt.close_file(1)

        for proc in psutil.process_iter():
            if proc.name() == 'pyro4-ns.exe':
                proc.terminate()
                print('Pyro4 server terminated')
                return

    @pyro.expose
    def check_status(self):
        return serpent.dumps(self.status)

    @pyro.expose
    def send_status(self, type=None, case=None, step=None, time=None, backup=False, nexts=None, corwpy=None, ovwpy=None, pause=None, langue=None, HDG=None, x_lbl=None, y_lbl=None):
        self.status.init = True
        if type is not None:
            self.type = type
            self.status.type = type
        if case is not None:
            self.case = case
            self.status.case = case
        if step is not None:
            self.step = step
            self.status.step = step
        if time is not None:
            self.time = time
            self.status.time = time
        if backup is not None:
            self.backup = backup
            self.status.backup = backup
        if corwpy is not None:
            self.corWPY = corwpy
            self.status.corWPY = corwpy
        if ovwpy is not None:
            self.OvWPY = ovwpy
            self.status.OvWPY = ovwpy
        if langue is not None:
            self.langue = langue
            self.status.langue = langue
        if nexts is not None:
            self.nexts = nexts
            self.status.nexts = nexts
        if pause is not None:
            self.pause = pause
            self.status.pause = pause
        if HDG is not None:
            self.HDG = HDG
            self.status.HDG = HDG
        if x_lbl is not None:
            self.x_lbl = x_lbl
            self.status.x_lbl = x_lbl
        if y_lbl is not None:
            self.y_lbl = y_lbl
            self.status.y_lbl = y_lbl
        return True

    @pyro.expose
    def send_tstamp(self, tstamp):
        self.exp_time = tstamp
        return

    @pyro.expose
    def check_tstamp(self):
        return self.exp_time

    @pyro.expose
    def start_time(self):
        self.clock.reset_time()
        self.reset_actual_delta()
        return self.clock.get_time()
    # Remember: I'm seeing these function from the Task point of view

    @pyro.expose
    def get_time(self, dtime=0):
        return self.clock.get_time(dtime=dtime)

    @pyro.expose
    def get_actual_delta(self):
        return self.clock.delta

    @pyro.expose
    def reset_actual_delta(self):
        self.clock.delta = 0

    def pause_time(self):
        self.clock.pause_time()
        return

    @pyro.expose
    def read_data(self, it: int, case=None):  # Here I should implement the difference in the lines to read
        if self.case is None or self.case != case:  # At init
            self.case = case
        # read line from server
        out_pack = Packet()
        out_pack.INorOUT = 0  # Inbound for the task
        out_pack.iter = it
        # writing of the pack selection in base on the phase
        if case == 1 or case in [-1, 0]:  # MAIN PHASE
            ph = 0
        elif case == 2 or case in [-5, -4]:  # SEARCH PHASE
            ph = 1
        elif case == 3 or case == -3:  # NAVI PHASE
            ph = 2
        elif case == 4 or case == -2:  # OVERALL PHASE
            ph = 3
        else:
            ph = 1  # Initial case
        out_pack.Tot_iters = len(self.scr_dir[ph].TIME)
        out_pack.Time = self.scr_dir[ph].TIME[it]
        out_pack.delta_t = self.scr_dir[ph].durs[it]
        out_pack.Switch = self.scr_dir[ph].SWITCH[it]
        out_pack.Task = self.scr_dir[ph].TASK[it]
        out_pack.case = None
        # SRC Data
        if self.case in [1, 2, 4, -5, -4, -1, -2]:
            out_pack.Imgs = deepcopy(self.scr_dir[ph].IMGS[it])
            out_pack.Fils = deepcopy(self.scr_dir[ph].FILS[it])
            out_pack.Rots = deepcopy(self.scr_dir[ph].ROTS[it])
            out_pack.Corr = deepcopy(self.scr_dir[ph].CORS[it])
        else:
            pass
        # NAVI Data
        # Generating HDG or WPY
        if self.scr_dir[ph].TASK[it] == 5:  # HDG
            self.scr_dir[ph].HDG[it] = self.scr_dir[ph].sel_HDG(HDG=self.HDG)
            self.scr_dir[ph].WPY[it] = 'N/A'  # Placeholder value
        elif self.scr_dir[ph].TASK[it] == 6:  # WPY
            self.scr_dir[ph].HDG[it] = -1  # Placeholder value
            # WPY = self.scr_dir[ph].sel_cell(x_lbl=self.x_lbl, y_lbl=self.y_lbl)
            # self.scr_dir[ph].WPY[it] = WPY[0]
            # self.scr_dir[ph].WPY_tuple[it] = WPY[1]
        else:
            self.scr_dir[ph].HDG[it] = -1  # Placeholder value
            self.scr_dir[ph].WPY[it] = 'N/A'  # Placeholder value
        out_pack.HDG = self.scr_dir[ph].HDG[it]
        # out_pack.WPY = self.scr_dir[ph].WPY[it]

        if it != 0 and (it < out_pack.Tot_iters and self.case != 6) and self.case in [1,2,4]:  # Exclude ending and pause cases
            out_pack.pImgs = deepcopy(self.scr_dir[ph].IMGS[it-1])

        elif it == out_pack.Tot_iters:  # add deadline for the overall training here
            out_pack.case = 8  # I REQUEST THE CALL FOR END
        elif self.case == 6:
            out_pack.case = 6  # Pause is then commanded!
            pass

        return serpent.dumps(out_pack)

    @pyro.expose
    def gen_WPY_instant(self, x_lbl, y_lbl, it, case=None):
        # writing of the pack selection in base on the phase
        if case == 1:  # MAIN PHASE
            ph = 0
        elif case == 2:  # SEARCH PHASE
            ph = 1
        elif case == 3:  # NAVI PHASE
            ph = 2
        elif case == 4:  # OVERALL PHASE
            ph = 3
        else:
            ph = 1  # Initial case
        WPY = self.scr_dir[ph].sel_cell(x_lbl=x_lbl, y_lbl=y_lbl)
        self.scr_dir[ph].WPY[it] = WPY[0]
        self.scr_dir[ph].WPY_tuple[it] = WPY[1]
        return WPY

    @pyro.expose
    def thread_send(self, in_pack):
        threading.Thread(target=self.send_data, args=(in_pack,)).start()  # this will generate a separate thread, avoiding stops
        return

    def send_data(self, inbound_pack):
        # send behavioral pack, remember to add the base64 decoding
        wrk_pack = Packet()
        dec_inpack = base64.b64decode(inbound_pack['data'])
        w_pack = serpent.loads(dec_inpack)

        # restructure the packet in the custom class
        wrk_pack.INorOUT = w_pack['INorOUT']  # Inbound for the task
        wrk_pack.Time = w_pack['Time']
        wrk_pack.Switch = w_pack['Switch']
        wrk_pack.Task = w_pack['Task']
        wrk_pack.phase = w_pack['phase']
        if wrk_pack.INorOUT == 1:
            self.SRCPackOUT = True  # Packet arrived from SRCTask
        elif wrk_pack.INorOUT == 2:
            self.NAVPackOUT = True  # Packet arrived from NAVTask

        wrk_pack.case = w_pack['case']
        self.case = w_pack['case']

        # if self.case == 2:  # Only SRC
        #     self.NAVPackOUT = True
        # elif self.case == 3:  # Only NAV
        #     self.SRCPackOUT = True

        wrk_pack.iter = w_pack['iter']
        wrk_pack.Tot_iters = w_pack['Tot_iters']
        if wrk_pack.INorOUT == 1:
            wrk_pack.Imgs = deepcopy(w_pack['Imgs'])
            wrk_pack.Fils = deepcopy(w_pack['Fils'])
            wrk_pack.Rots = deepcopy(w_pack['Rots'])
            wrk_pack.Corr = deepcopy(w_pack['Corr'])

            wrk_pack.UserType = deepcopy(w_pack['UserType'])
            wrk_pack.sRT = w_pack['sRT']
            wrk_pack.SRCLatency = w_pack['SRCLatency']
            wrk_pack.num_ON = w_pack['num_ON']  # Numpad used 1 / Not used 0
            wrk_pack.ts_num = w_pack['ts_num']
            wrk_pack.te_num = w_pack['te_num']
            wrk_pack.GoodCh = w_pack['GoodCh']
            wrk_pack.OvCh = w_pack['OvCh']
            wrk_pack.OvTrue = w_pack['OvTrue']
            wrk_pack.ACC = w_pack['ACC']
        elif wrk_pack.INorOUT == 2:
            # Missing other NAV params
            wrk_pack.HDG = w_pack['HDG']
            wrk_pack.WPY = w_pack['WPY']
            wrk_pack.WPYTuple = w_pack['WPYTuple']
            wrk_pack.NAVLatency = w_pack['NAVLatency']
            wrk_pack.nRT = w_pack['nRT']
            wrk_pack.fstick_ON = w_pack['fstick_ON']  # Fstick used 1 / Not used 0
            wrk_pack.ts_fstick = w_pack['ts_fstick']  # Clock Time of the last fstick stroke / first fstick stroke
            wrk_pack.te_fstick = w_pack['te_fstick']
            wrk_pack.mouse_ON = w_pack['mouse_ON']  # Mouse used 1 / Not used 0
            wrk_pack.ts_mouse = w_pack['ts_mouse']  # Clock Time of the mouse movement
            wrk_pack.te_mouse = w_pack['te_mouse']
            wrk_pack.usrHDG = w_pack['usrHDG']  # Just will show the HDG as integer
            wrk_pack.usrDIR = w_pack['usrDIR']  # USER CHOICE: -1 left/1 right the correct dir/ 0 invariant (180 case)/ -2 not answered
            wrk_pack.corDIR = w_pack['corDIR']  # CORRECT CHOICE: -1 left/1 right the correct dir
            wrk_pack.dev = w_pack['dev']  # deviation from current requested HDG
            wrk_pack.usr_WPY = w_pack['usr_WPY']  # None if not selected, value if selected
            wrk_pack.usr_WPYTuple = w_pack['usr_WPYTuple']
            wrk_pack.WPYcorr = w_pack['WPYcorr']  # -1 Not Answered / 0 Wrong / 1 Correct
            wrk_pack.cor_WPY = w_pack['cor_WPY']  # No of correct WPY
            wrk_pack.Ovcor_WPY = w_pack['Ovcor_WPY']  # No of shown WPYs

        if wrk_pack.INorOUT == 1:
            del self.SRClastPacket
            self.SRClastPacket = deepcopy(wrk_pack)  # Packet arrived from SRCTask
        elif wrk_pack.INorOUT == 2:
            del self.NAVlastPacket
            self.NAVlastPacket = deepcopy(wrk_pack)  # Packet arrived from NAVTask

        if (self.SRCPackOUT and self.NAVPackOUT) or self.case in [2, 3]:  # XOR condition
            if (self.SRClastPacket.iter == self.NAVlastPacket.iter) or self.case in [2, 3]:
                #print(f'VERIFIED: GO TO MERGE ITER {self.SRClastPacket.iter if self.case != 3 else self.NAVlastPacket.iter}')
                self.merge_packs()  # Executing as separate thread
            else:
                pass #DEBUG PRETEST
                #print(f'ERROR: ITER ARE NOT EQUAL SRC: {self.SRClastPacket.iter} NAV: {self.NAVlastPacket.iter}')
        else: pass
        return

    def merge_packs(self):
        # Reinit the packet
        del self.MlastPacket
        self.MlastPacket = Packet()
        # Copy of the data
        if self.case != 3:
            self.MlastPacket.iter = self.SRClastPacket.iter
            self.MlastPacket.Tot_iters = self.SRClastPacket.Tot_iters
            self.MlastPacket.phase = self.SRClastPacket.phase
            self.MlastPacket.case = self.SRClastPacket.case
            self.MlastPacket.Time = self.SRClastPacket.Time
            self.MlastPacket.Switch = self.SRClastPacket.Switch
            self.MlastPacket.Task = self.SRClastPacket.Task
        else:
            self.MlastPacket.iter = self.NAVlastPacket.iter
            self.MlastPacket.Tot_iters = self.NAVlastPacket.Tot_iters
            self.MlastPacket.phase = self.NAVlastPacket.phase
            self.MlastPacket.case = self.NAVlastPacket.case
            self.MlastPacket.Time = self.NAVlastPacket.Time
            self.MlastPacket.Switch = self.NAVlastPacket.Switch
            self.MlastPacket.Task = self.NAVlastPacket.Task

        # SRC Params
        if self.MlastPacket.case != 3:
            self.MlastPacket.Imgs = deepcopy(self.SRClastPacket.Imgs)
            self.MlastPacket.Fils = deepcopy(self.SRClastPacket.Fils)
            self.MlastPacket.Rots = deepcopy(self.SRClastPacket.Rots)
            self.MlastPacket.Corr = deepcopy(self.SRClastPacket.Corr)
            self.MlastPacket.UserType = deepcopy(self.SRClastPacket.UserType)
        self.MlastPacket.SRCLatency = self.SRClastPacket.SRCLatency
        self.MlastPacket.sRT = self.SRClastPacket.sRT
        self.MlastPacket.num_ON = self.SRClastPacket.num_ON
        self.MlastPacket.ts_num = self.SRClastPacket.ts_num  # Clock Time of the first numpad keypress
        self.MlastPacket.te_num = self.SRClastPacket.te_num  # Clock Time of the last numpad keypress
        self.MlastPacket.ACC = self.SRClastPacket.ACC
        self.MlastPacket.GoodCh = self.SRClastPacket.GoodCh
        self.MlastPacket.OvCh = self.SRClastPacket.OvCh
        self.MlastPacket.OvTrue = self.SRClastPacket.OvTrue
        # NAV Params
        self.MlastPacket.HDG = self.NAVlastPacket.HDG
        self.MlastPacket.WPY = self.NAVlastPacket.WPY
        self.MlastPacket.WPYTuple = self.NAVlastPacket.WPYTuple
        self.MlastPacket.NAVLatency = self.NAVlastPacket.NAVLatency  # Latency on the NAVTask graphics runtime
        self.MlastPacket.nRT = self.NAVlastPacket.nRT  # NAV Reaction Time
        self.MlastPacket.fstick_ON = self.NAVlastPacket.fstick_ON  # Fstick used 1 / Not used 0
        self.MlastPacket.ts_fstick = self.NAVlastPacket.ts_fstick  # Clock Time of the last fstick stroke / first fstick stroke
        self.MlastPacket.te_fstick = self.NAVlastPacket.te_fstick
        self.MlastPacket.mouse_ON = self.NAVlastPacket.mouse_ON  # Mouse used 1 / Not used 0
        self.MlastPacket.ts_mouse = self.NAVlastPacket.ts_mouse # Clock Time of the mouse movement
        self.MlastPacket.te_mouse = self.NAVlastPacket.te_mouse
        self.MlastPacket.usrHDG = self.NAVlastPacket.usrHDG  # Just will show the HDG as integer
        self.MlastPacket.usrDIR = self.NAVlastPacket.usrDIR  # USER CHOICE: -1 left/1 right the correct dir/ 0 invariant (180 case)/ -2 not answered
        self.MlastPacket.corDIR = self.NAVlastPacket.corDIR  # CORRECT CHOICE: -1 left/1 right the correct dir
        self.MlastPacket.dev = self.NAVlastPacket.dev  # deviation from current requested HDG
        self.MlastPacket.usr_WPY = self.NAVlastPacket.usr_WPY  # None if not selected, value if selected
        self.MlastPacket.usr_WPYTuple = self.NAVlastPacket.usr_WPYTuple
        self.MlastPacket.WPYcorr = self.NAVlastPacket.WPYcorr  # -1 Not Answered / 0 Wrong / 1 Correct
        self.MlastPacket.cor_WPY = self.NAVlastPacket.cor_WPY  # No of correct WPY
        self.MlastPacket.Ovcor_WPY = self.NAVlastPacket.Ovcor_WPY  # No of shown WPYs

        # Add routine to write on csv on separate process
        self.csv_prt.write_line(self.MlastPacket)

        # Reset Flags
        self.SRCPackOUT = False
        self.NAVPackOUT = False

        return


pyro_svr = PyroServer()
