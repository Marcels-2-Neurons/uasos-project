# utilscsv.py>
# Library used for work on the output csv files
# Used as utility lib in pyro_server.py
# will hold in listening until the connection is established
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

import csv
import datetime
import fnmatch
import os
import sys

import packet
from packet import *

class vas_utils():
    def __init__(self):
        self.vwriter = None
        self.vas_filepath = None
        self.folder_name = 'results'  # result file directory
        self.path = None
        self.subfolder_name = None
        self.vas_fname = None
        self.USER_ID = None
        self.vas_header = ['exp_iter', 'cognitive_fatigue', 'drowsiness']

    def start_VAS(self, usr, back):
        if self.USER_ID is None:
            self.USER_ID = usr
        self.vas_fname = f'VAS_ID{self.USER_ID}.csv'
        self.subfolder_name = f'ID{self.USER_ID}'
        self.path = os.getcwd()
        self.vas_filepath = os.path.join(self.path, self.folder_name, self.subfolder_name, self.vas_fname)
        if back is False:  # New VAS
            with open(self.vas_filepath, 'w', newline='') as self.vasfile:
                self.vwriter = csv.writer(self.vasfile, delimiter='\t')
                self.vwriter.writerow(self.vas_header)
        else:  # Recover previous VAS
            pass

    def write_VAS(self, answers, usr):
        if self.USER_ID is None:
            self.USER_ID = usr
            self.vas_fname = f'VAS_ID{self.USER_ID}.csv'
            self.subfolder_name = f'ID{self.USER_ID}'
            self.path = os.getcwd()
            self.vas_filepath = os.path.join(self.path, self.folder_name, self.subfolder_name, self.vas_fname)

        with open(self.vas_filepath, 'a', newline='') as self.vasfile:
            self.vwriter = csv.writer(self.vasfile, delimiter='\t')
            self.vwriter.writerow(answers)

class utilscsv:
    def __init__(self):
        # User Random Identifier TODO
        self.USER_ID = None  # User ID obtained from main
        self.twriter = None  # Writer of the training csv
        self.writer = None  # Writer of the current experience csv
        self.path = os.getcwd()  # Working Directory
        self.folder_name = 'results'  # result file directory
        self.subfolder_name = f'ID{self.USER_ID}'
        self.tfilename = None  # Filename for the Training results
        self.filename = None  # Filename for the current experience results
        self.tfile_path = None  # File-path for the Training results
        self.file_path = None  # File-path for the current experience results
        #file handlers
        self.tcsvfile = None  # For Training Phase
        self.csvfile = None  # For experiment phase

        # Standard header
        self.header = ['EXP_CASE', 'TIME', 'SWITCH', 'TASK',
                       'IMG_1', 'IMG_2', 'IMG_3', 'IMG_4', 'IMG_5', 'IMG_6', 'IMG_7', 'IMG_8', 'IMG_9',
                       'FIL_1', 'FIL_2', 'FIL_3', 'FIL_4', 'FIL_5', 'FIL_6', 'FIL_7', 'FIL_8', 'FIL_9',
                       'ROT_1', 'ROT_2', 'ROT_3', 'ROT_4', 'ROT_5', 'ROT_6', 'ROT_7', 'ROT_8', 'ROT_9',
                       'COR_1', 'COR_2', 'COR_3', 'COR_4', 'COR_5', 'COR_6', 'COR_7', 'COR_8', 'COR_9',
                       'USR_1', 'USR_2', 'USR_3', 'USR_4', 'USR_5', 'USR_6', 'USR_7', 'USR_8', 'USR_9',
                       'SRC_RT[ms]', 'Good_Ch', 'Ov_Ch', 'Ov_True', 'num_ON', 'Ts_num[ms]', 'Te_num[ms]',
                       'HDG[deg]', 'WPY', 'WPY_posX', 'WPY_posY', 'NAV_RT[ms]', 'usr_HDG[deg]',
                       'DEV[deg]', 'exp_DIR', 'usr_DIR', 'usr_WPY', 'usr_WPY_posX', 'usr_WPY_posY', 'WPY_corr', 'No_cor_WPY',
                       'No_ov_WPY', 'fstick_ON', 'Ts_fstick[ms]', 'Te_fstick[ms]', 'mouse_ON', 'Ts_mouse[ms]', 'Te_mouse[ms]', 'SRCLatency', 'NAVLatency']

    def close_file(self, phase):
        if phase == 0:  # Training Phase
            self.tcsvfile.close()
        elif phase == 1:  # Current Experiment
            self.csvfile.close()
        return

    def take_files(self, t_file, file):
        self.tfilename = t_file
        self.filename = file
        self.tfile_path = os.path.join(self.path, self.folder_name, self.subfolder_name, self.tfilename)
        self.file_path = os.path.join(self.path, self.folder_name, self.subfolder_name, self.filename)
        return

    def write_line(self, pack: Packet):
        if self.tfile_path is not None or self.file_path is not None:
            if pack.phase == 0:  # Training Phase
                with open(self.tfile_path, 'a', newline='') as self.tcsvfile:
                    self.twriter = csv.writer(self.tcsvfile, delimiter='\t')
                    self.twriter.writerow([pack.case] + [pack.Time] + [pack.Switch] + [pack.Task] +
                                          pack.Imgs + pack.Fils + pack.Rots + pack.Corr +
                                          pack.UserType + [pack.sRT] +
                                          [pack.GoodCh] + [pack.OvCh] + [pack.OvTrue] + [pack.num_ON] +
                                          [pack.ts_num] + [pack.te_num] + [pack.HDG] + [pack.WPY] + [pack.WPYTuple[0]] +
                                          [pack.WPYTuple[1]] + [pack.nRT] + [pack.usrHDG] +
                                          [pack.dev] + [pack.corDIR] + [pack.usrDIR] + [pack.usr_WPY] +
                                          [pack.usr_WPYTuple[0]] + [pack.usr_WPYTuple[1]] + [pack.WPYcorr] + [pack.cor_WPY] +
                                          [pack.Ovcor_WPY] + [pack.fstick_ON] + [pack.ts_fstick] + [pack.te_fstick] +
                                          [pack.mouse_ON] + [pack.ts_mouse] + [pack.te_mouse] + [pack.SRCLatency] + [pack.NAVLatency])

            elif pack.phase == 1:  # Current Experiment
                with open(self.file_path, 'a', newline='') as self.csvfile:
                    self.writer = csv.writer(self.csvfile, delimiter='\t')
                    self.writer.writerow([pack.case] + [pack.Time] + [pack.Switch] + [pack.Task] +
                                          pack.Imgs + pack.Fils + pack.Rots + pack.Corr +
                                          pack.UserType + [pack.sRT] +
                                          [pack.GoodCh] + [pack.OvCh] + [pack.OvTrue] + [pack.num_ON] +
                                          [pack.ts_num] + [pack.te_num] + [pack.HDG] + [pack.WPY] + [pack.WPYTuple[0]] +
                                          [pack.WPYTuple[1]] + [pack.nRT] + [pack.usrHDG] +
                                          [pack.dev] + [pack.corDIR] + [pack.usrDIR] + [pack.usr_WPY] +
                                          [pack.usr_WPYTuple[0]] + [pack.usr_WPYTuple[1]] + [pack.WPYcorr] + [pack.cor_WPY] +
                                          [pack.Ovcor_WPY] + [pack.fstick_ON] + [pack.ts_fstick] + [pack.te_fstick] +
                                          [pack.mouse_ON] + [pack.ts_mouse] + [pack.te_mouse] + [pack.SRCLatency] + [pack.NAVLatency])
        else:
            pass
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
        self.subfolder_name = f'ID{self.USER_ID}'
        self.tfilename = f"res_{current_date}_ID{self.USER_ID}_t.csv"
        self.filename = f"res_{current_date}_ID{self.USER_ID}.csv"
        self.tfile_path = os.path.join(self.path, self.folder_name, self.subfolder_name, self.tfilename)
        f_path = os.path.join(self.path, self.folder_name, self.subfolder_name)
        self.file_path = os.path.join(self.path, self.folder_name, self.subfolder_name, self.filename)
        print("Result file will be saved in: ", f_path)
        print("Have fun, test subject No. ", self.USER_ID)
        self.start_writers()


def writeform(ans=None):
    if ans is not None:
        path = os.getcwd()
        folder_name = 'results'
        subfolder_name = f'ID{ans.ID}'
        filepath = os.path.join(path, folder_name, subfolder_name)
        # Create IDXXX folder
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        file_name = f'data_ID{ans.ID}.csv'
        filename = os.path.join(filepath, file_name)
        with open(filename, 'w', newline='') as datafile:
            dwriter = csv.writer(datafile, delimiter='\t')
            dwriter.writerow(ans.header)
            dwriter.writerow([ans.ID] + [ans.lang] + [ans.age] + [ans.gender] + [ans.degree] + [ans.work] +
                              [ans.total] + [ans.scorewriting] + [ans.scorethrowing] + [ans.scoretoothbrush] +
                              [ans.scorespoon] + [ans.KSS_data] + [ans.SPS_data] + [ans.RSME_data] +
                              [ans.VAS_cognitive] + [ans.VAS_drowsiness])
            datafile.close()
        print(f'Subject ID {ans.ID} data saved in: {filename}')


def write_metadata(ans=None):
    if ans is not None:
        path = os.getcwd()
        folder_name = 'results'
        subfolder_name = f'ID{ans.ID}'
        filepath = os.path.join(path, folder_name, subfolder_name)
        # Create IDXXX folder
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        file_name = f'setup_ID{ans.ID}.dat'
        filename = os.path.join(filepath, file_name)
        # Start of the writing
        with open(filename, 'w') as setup_file:
            setup_file.write('## METADATA FILE - DO NOT CANCEL ##\n')
            setup_file.write(f'ID={ans.ID}\n')
            setup_file.write(f'language={ans.lang}\n')
            setup_file.write(f'VAS={ans.VAS}\n')
            setup_file.write(f'VAS Time={ans.VAS_Time}\n')
            setup_file.write('## END OF METADATA FILE - DO NOT CANCEL ##')

        setup_file.close()


def read_metadata(ans=None):
    #from questions import ans
    path = os.getcwd()
    folder_name = 'results'
    subfolder_name = f'ID{ans.ID}'
    filepath = os.path.join(path, folder_name, subfolder_name)
    # Check IDXXX folder existance
    if not os.path.exists(filepath):
        return False  # Continue the setup process
    file_name = f'setup_ID{ans.ID}.dat'
    filename = os.path.join(filepath, file_name)
    try:
        with open(filename, 'r') as setup_file:
            lines = setup_file.readlines()
            lines = [line.rstrip() for line in lines]
            for idx, line in enumerate(lines):
                if idx in [0, len(lines)-1]:
                    pass
                else:
                    words = line.split('=')
                    if len(words) == 2:
                        key, val = words

                        if key == 'ID':
                            ans.ID = int(val)
                        elif key == 'language':
                            ans.lang = val
                        elif key == 'VAS':
                            if val == 'True':
                                ans.VAS = True
                            else:
                                ans.VAS = False
                        elif key == 'VAS Time' and val != 'None':
                            ans.VAS_Time = int(val)
                        else:
                            pass
    except FileNotFoundError:
        print(f'Metadata of experiment for {ans.ID} not found. Continue standard execution.')
        return False
    except Exception as e:
        print(f'An error occurred: {e}')
        return False
    else:
        print(f'Metadata of experiment for {ans.ID} recovered. Proceed to inject to the last phase/step.')
        return True


def read_results(ans=None):
    path = os.getcwd()
    folder_name = 'results'
    subfolder_name = f'ID{ans.ID}'
    filepath = os.path.join(path, folder_name, subfolder_name)
    no_tfile = 0
    no_main_file = 0
    # Check IDXXX folder existance
    if not os.path.exists(filepath):
        return False  # Continue the setup process

    tfile_pattern = f"res_*_ID{ans.ID}_t.csv"
    file_pattern = f"res_*_ID{ans.ID}.csv"
    t_file = None
    file = None

    for filename in os.listdir(filepath):
        if fnmatch.fnmatch(filename, tfile_pattern):
            t_file = os.path.join(filepath, filename)  # training csv
            ans.t_file = t_file
        elif fnmatch.fnmatch(filename, file_pattern):
            file = os.path.join(filepath, filename)  # main exp csv
            ans.file = file
        else:
            pass

    if t_file is not None and file is not None:
        # Read main exp csv
        with open(file, 'r') as main:
            csv_main = csv.reader(main, delimiter='\t')
            for line in csv_main:
                no_main_file += 1
                last_line = line
            no_main_file = no_main_file - 1  # Remove header
            time = float(last_line[1]) if no_main_file != 0 else 0
            if time < 2*60*60*1000 and no_main_file > 0:
                ans.case = 1
                ans.step = no_main_file
                ans.time = time
                ans.type = 'BACKUP'
                ans.Good_ch = int(last_line[50])
                ans.Ov_ch = int(last_line[51])
                ans.Ov_True = int(last_line[52])
                ans.corWPY = int(last_line[69])
                ans.OvWPY = int(last_line[70])
                return True
            elif no_main_file == 0:
                print(f'Main experiment result file is empty. Check training file')
            else:
                print(f'Experiment of test subject ID {ans.ID} seems complete. Closing the experiment')
                sys.exit()

        src_step = 0
        nav_step = 0
        ov_step = 0

        with open(t_file, 'r') as t_csv:
            csv_train = csv.reader(t_csv, delimiter='\t')
            for line in csv_train:
                no_tfile += 1
                last_line = line
                if no_tfile != 1:
                    if int(last_line[0]) == 2:  # SRC
                        src_step += 1
                    elif int(last_line[0]) == 3:  # NAV
                        nav_step += 1
                    elif int(last_line[0]) == 4:  # OVERALL
                        ov_step += 1

            time = float(last_line[1])
            if time < (10 * 60 * 1000 - 15 * 1000) and int(last_line[0]) == 4:
                # Overall training
                ans.case = 4
                ans.step = ov_step - 1
                ans.time = time
                ans.type = 'BACKUP'
                ans.Good_ch = int(last_line[50])
                ans.Ov_ch = int(last_line[51])
                ans.Ov_True = int(last_line[52])
                ans.corWPY = int(last_line[69])
                ans.OvWPY = int(last_line[70])
                return True
            elif time < (3 * 60 * 1000 - 15 * 1000) and int(last_line[0]) == 3:
                # NAVI training
                ans.case = 3
                ans.step = nav_step - 1
                ans.time = time
                ans.type = 'BACKUP'
                ans.corWPY = int(last_line[69])
                ans.OvWPY = int(last_line[70])
                return True
            elif time >= (3 * 60 * 1000 - 15 * 1000) and int(last_line[0]) == 3:
                ans.case = -2
                ans.step = 0
                ans.time = 0
                ans.type = 'BACKUP'
                return True
            elif time < (3 * 60 * 1000 - 15 * 1000) and int(last_line[0]) == 2:
                # SRC training
                ans.case = 2
                ans.step = src_step - 1
                ans.time = time
                ans.type = 'BACKUP'
                ans.Good_ch = int(last_line[50])
                ans.Ov_ch = int(last_line[51])
                ans.Ov_True = int(last_line[52])
                return True
            elif time >= (3 * 60 * 1000 - 15 * 1000) and int(last_line[0]) == 2:
                ans.case = -3
                ans.step = 0
                ans.time = 0
                ans.type = 'BACKUP'
                return True
            else:
                print(f'Training Experiment of test subject ID {ans.ID} seems complete. Start the main experiment')
                ans.case = -1
                ans.step = 0
                ans.time = 0
                ans.type = 'BACKUP'
                return True

    else:
        print('Results data are corrupted or missing. Continuing standard execution.')
        return False
