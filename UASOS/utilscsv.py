# utilscsv.py>
# Library used for work on the output csv files
# Used as utility lib in pyro_server.py
# will hold in listening until the connection is established
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

import csv
import datetime
import os

import packet
from packet import *

class utilscsv:
    def __init__(self):
        # User Random Identifier TODO
        self.USER_ID = None  # User ID obtained from main
        self.twriter = None  # Writer of the training csv
        self.writer = None  # Writer of the current experience csv
        self.path = os.getcwd()  # Working Directory
        self.folder_name = 'results'  # result file directory
        self.tfilename = None  # Filename for the Training results
        self.filename = None  # Filename for the current experience results
        self.tfile_path = None  # File-path for the Training results
        self.file_path = None  # File-path for the current experience results
        #file handlers
        self.tcsvfile = None # For Training Phase
        self.csvfile = None # For experiment phase

        # Standard header
        self.header = ['TIME', 'SWITCH', 'TASK',
                       'IMG_1', 'IMG_2', 'IMG_3', 'IMG_4', 'IMG_5', 'IMG_6', 'IMG_7', 'IMG_8', 'IMG_9',
                       'FIL_1', 'FIL_2', 'FIL_3', 'FIL_4', 'FIL_5', 'FIL_6', 'FIL_7', 'FIL_8', 'FIL_9',
                       'ROT_1', 'ROT_2', 'ROT_3', 'ROT_4', 'ROT_5', 'ROT_6', 'ROT_7', 'ROT_8', 'ROT_9',
                       'COR_1', 'COR_2', 'COR_3', 'COR_4', 'COR_5', 'COR_6', 'COR_7', 'COR_8', 'COR_9',
                       'USR_1', 'USR_2', 'USR_3', 'USR_4', 'USR_5', 'USR_6', 'USR_7', 'USR_8', 'USR_9',
                       'LATENCY', 'RT', 'TTS', 'Good_Ch', 'Ov_Ch', 'Ov_True']
        # TODO: Add full NAVTask Metrics

    def close_file(self, phase):
        if phase == 0:  # Training Phase
            self.tcsvfile.close()
        elif phase == 1:  # Current Experiment
            self.csvfile.close()
        return

    def write_line(self, pack: Packet):
        if pack.phase == 0:  # Training Phase
            with open(self.tfile_path, 'a', newline='') as self.tcsvfile:
                self.twriter = csv.writer(self.tcsvfile, delimiter='\t')
                self.twriter.writerow([pack.Time] + [pack.Switch] + [pack.Task] +
                                    pack.Imgs + pack.Fils + pack.Rots + pack.Corr +
                                    pack.UserType + [pack.SRCLatency] + [pack.RT] +
                                    [pack.TTS] + [pack.GoodCh] + [pack.OvCh] + [pack.OvTrue])
            # TODO: Add full NAVTask Metrics
        elif pack.phase == 1:  # Current Experiment
            with open(self.file_path, 'w', newline='') as self.csvfile:
                self.writer = csv.writer(self.csvfile, delimiter='\t')
                self.writer.writerow([pack.Time] + [pack.Switch] + [pack.Task] +
                                    pack.Imgs + pack.Fils + pack.Rots + pack.Corr +
                                    pack.UserType + [pack.SRCLatency] + [pack.RT] +
                                    [pack.TTS] + [pack.GoodCh] + [pack.OvCh] + [pack.OvTrue])
            # TODO: Add full NAVTask Metrics
        return

    def start_writers(self):
        # This function starts the writer pointers
        with open(self.tfile_path, 'w', newline='') as self.tcsvfile:
            self.twriter = csv.writer(self.tcsvfile, delimiter='\t')
            # Write header
            self.twriter.writerow(self.header)

        with open(self.file_path, 'w', newline='') as self.csvfile:
            self.writer = csv.writer(self.csvfile, delimiter='\t')
            # Write header
            self.writer.writerow(self.header)

    def setup_out(self):
        # I set the filename and filepath here
        current_date = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        self.tfilename = f"res_{current_date}_ID{self.USER_ID}_t.csv"
        self.filename = f"res_{current_date}_ID{self.USER_ID}.csv"
        self.tfile_path = os.path.join(self.path, self.folder_name, self.tfilename)
        f_path = os.path.join(self.path, self.folder_name)
        self.file_path = os.path.join(self.path, self.folder_name, self.filename)
        print("Result file will be saved in: ", f_path)
        self.start_writers()
