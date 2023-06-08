# packet.py>
# Library used for defining the packet structure
# Imported on pyro_server.py, SRCTask and NAVTask
# will hold in listening until the connection is established
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

class Packet(object):
    def __init__(self):
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
        # Return Behavioural metrics: TODO
