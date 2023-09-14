# packet.py>
# Library used for defining the packet structure
# Imported on pyro_server.py, SRCTask and NAVTask
# will hold in listening until the connection is established
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
from psychopy import core


class Packet(object):
    def __init__(self):
        self.USER_ID = 0
        self.INorOUT = -1  # O - Inbound for the task / 1 - Outbound from the SRCTask / 2 - Outbound from the NAVTask
        self.phase = 0  # Phase 0 will write on csv training, Phase 1 will write on final csv
        self.case = 0  # Case 2 - SRC Train / 3 - NAV Train / 4 - Overall Train / 1 - Main Experiment
        # Parameters to send
        self.iter = 0
        self.Tot_iters = 0  # Total No of iterations
        # Time Item
        self.Time = 0
        self.delta_t = 0
        # Switch Iter
        self.Switch = 0
        # Task Iter
        self.Task = 0
        # Image Vector
        self.pImgs = [0 for _ in range(9)]  # Previous Iteration Image Set
        self.Imgs = [0 for _ in range(9)]
        # Filters Vector
        self.Fils = [0 for _ in range(9)]
        # Rotations Vector
        self.Rots = [0 for _ in range(9)]
        # Correct Vector
        self.Corr = [0 for _ in range(9)]

        # NAV Items
        self.HDG = -1
        self.WPY = ""
        self.WPYTuple = (0, 0)

        # Outbound Packet Metadata
        self.UserType = [0 for _ in range(9)]  # User Selection
        self.SRCLatency = 0  # Latency on the SRCTask graphics runtime
        self.sRT = 0  # SRC Reaction Time
        self.ACC = 0  # Actual accuracy
        self.GoodCh = 0  # Good User Choices
        self.OvCh = 0  # Overall User Choices
        self.OvTrue = 0  # Overall Correct Images
        self.num_ON = 0  # Numpad used 1 / Not used 0
        self.ts_num = 0  # Clock Time of the first numpad keypress
        self.te_num = 0  # Clock Time of the last numpad keypress

        # Metrics for the NAVTask
        self.NAVLatency = 0  # Latency on the NAVTask graphics runtime
        self.nRT = 0  # NAV Reaction Time
        self.fstick_ON = 0  # Fstick used 1 / Not used 0
        self.ts_fstick = 0  # Clock Time of the last fstick stroke / first fstick stroke
        self.te_fstick = 0
        self.mouse_ON = 0  # Mouse used 1 / Not used 0
        self.ts_mouse = 0  # Clock Time of the mouse movement
        self.te_mouse = 0
        self.usrHDG = -1  # Just will show the HDG as integer
        self.usrDIR = -2  # USER CHOICE: -1 left/1 right the correct dir/ 0 invariant (180 case)/ -2 not answered
        self.corDIR = 0  # CORRECT CHOICE: -1 left/1 right the correct dir
        self.dev = 'NaN'  # deviation from current requested HDG
        self.usr_WPY = "None"  # None if not selected, value if selected
        self.usr_WPYTuple = (0, 0)
        self.WPYcorr = -1  # -1 Not Answered / 0 Wrong / 1 Correct
        self.cor_WPY = 0  # No of correct WPY
        self.Ovcor_WPY = 0  # No of shown WPYs
        # ----------


class cClock(object):  # Common Clock object for syncronizing the tasks
    def __init__(self):
        self.time = core.Clock()
        self.delta = 0
        self.pause = False
        self.reset = False
        self.resetc = 0
        self.deadline = -1  # For stopping the Overall Training

    def reset_time(self):
        # TODO figure the restart of the clock object when passing to another experiment phase
        if self.reset is False and self.resetc == 0:  # Clock Init case
            self.delta = 0
            self.time.reset()
            self.resetc += 1  # Reset counter
            self.reset = True
        elif self.resetc != 0:  # Pause situation
            self.delta += self.time.getTime()
            self.time.reset()
            self.resetc += 1  # Reset counter
            self.reset = True

    def get_time(self, pause=False, dtime=0):
        if pause is True and self.pause is False:
            self.pause = True
            self.reset_time()
        elif pause is False and self.pause is True:
            self.time.reset()
            self.pause = False
        if self.reset is True:
            self.reset = False
        if dtime != 0:
            self.delta += dtime
        return self.delta + self.time.getTime()

    def pause_time(self):
        self.delta = self.get_time(pause=True)
        self.pause = True  # This will trigger the reset at the reprise

class status(object):
    def __init__(self):
        self.init = False
        self.type = 'FULL'
        self.case = None
        self.step = 0
        self.time = 0
        self.backup = None
        self.langue = 'fr'
        self.nexts = None
        self.pause = None
        self.HDG = None
        self.corWPY = None
        self.OvWPY = None
        self.x_lbl = None
        self.y_lbl = None
