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
        self.phase = 0  # 0 - Training Phase / 1 - Experiment Phase
        # 3 - Ready to write to csv
        # Parameters to send
        self.iter = 0
        self.Tot_iters = 0  # Total No of iterations
        # Time Item
        self.Time = 0
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

        # Outbound Packet Metadata
        # Return Behavioural metrics
        self.UserType = [0 for _ in range(9)]  # User Selection
        self.SRCLatency = 0  # Latency on the SRCTask graphics runtime
        self.RT = 0  # Reaction Time
        self.TTS = 0  # Time to Switch (From Numpad to Flightstick and viceversa)
        self.ACC = 0  # Actual accuracy
        self.GoodCh = 0  # Good User Choices
        self.OvCh = 0  # Overall User Choices
        self.OvTrue = 0  # Overall Correct Images

        # These 2 are for the Time to Switch: works only on case 3
        self.Tnum = 0  # Clock Time of the first numpad keypress / last numpad keypress
        self.Tstick = 0  # Clock Time of the last fstick stroke / first fstick stroke
        # ----------

        self.NAVLatency = 0  # Latency on the NAVTask graphics runtime


class cClock(object):  # Common Clock object for syncronizing the tasks
    def __init__(self):
        self.time = core.Clock()
        self.reset = False

    def reset_time(self):
        if not self.reset:
            self.time.reset()
            self.reset = True

    def get_time(self):
        return self.time.getTime()