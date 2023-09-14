# scriptgen_old2.py>
# Library used as Script Generator for the experiment
# Imported in settings as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
from random import *
import time

import numpy as np


class ScriptGen:
    def __init__(self, phase='MAIN', exclude=-1):
        self.exp_time = 2 * 60 * 60 * 1000  # time in ms
        self.it_time = 6000  # average iteration time in ms (it was 625 ms)
        self.jitter = 750  # jitter time in ms

        self.TIME = []  # time schedule vector 1xSize_exp
        self.SWITCH = []  # Task switch vector 1xSize_exp:
        # 0-Just at start / 1-Repeat Task / 2-Switch Task Mode / 3-Switch Tasks
        self.TASK = []  # Task type vector 1xSize_exp
        # 0-4 for the SRC Task, based on NORB Cats / 5-NAVI HDG / 6-NAVI WPY
        self.HDG = []  # HDG Vector: RESERVED FOR NAVI TASK, Random Heading inside here 1xSize_exp
        self.WPY = []  # WPY Vector: RESERVED FOR NAVI TASK, Random Waypoint inside here 1xSize_exp
        self.WPY_tuple = []  # Coordinates of the WPY correct marker
        self.IMGS = []  # Images Array: RESERVED FOR SRC TASK, Random images here (0-911) 9xSize_exp
        self.FILS = []  # Filters Array: RESERVED FOR SRC TASK, Random Filter here, only for max 3 rand images changed
        # If less than 3 images are changed, the blank cells will have 'None' value 3xSize_exp
        self.ROTS = []  # Rotations Array: RESERVED FOR SRC TASK, Random rotation here, only for max 3 rand images changed
        # If less than 3 images are changed, the blank cells will have 'None' value 3xSize_exp
        self.CORS = []  # Correct Array: RESERVED FOR SRC TASK, Correct cells are here 9xSize_exp
        self.max_no_correct = 4  # Max number of correct images
        self.NAV_to_SRC = []  # Array in which we store all the position of where we have a return to SRC
        self.purge = False  # Trigger for maximize changes to reduce targets
        self.Max = 0  # Potential no of changes
        self.locp = []  # location vector of people
        self.locv = []  # location vector of vehicles
        self.CORSt = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # last correct iteration in case of NAV
        self.threshold = 0.05
        self.dev_per = 0
        self.mode_sel = 'DEBUG'  # 'BATCH' / 'DEBUG'
        # Probability Table for the Task Cases - Condition Balancing
        # ______________________________________________________________________________________
        # |                |   SRC - 1 25% |   SRC - 4 25% |   FLY - HDG 25% |   FLY - WPT 25% |
        # | REPEAT-1 33%   |    8.25%      |     8.25%     |     8.25%       |      8.25%      |
        # | INTERNAL-2 33% |    8.25%      |     8.25%     |     8.25%       |      8.25%      |
        # | EXTERNAL-3 33% |    8.25%      |     8.25%     |     8.25%       |      8.25%      |
        # ______________________________________________________________________________________
        # Parameters definition
        self.phase = phase
        self.exclude = exclude
        # Probability Table for the Task Cases - Condition Balancing
        # ______________________________________________________________________________________
        # |                |   SRC - 1 25% |   SRC - 4 25% |   FLY - HDG 25% |   FLY - WPT 25% |
        # | REPEAT-1 33%   |    8.25%      |     8.25%     |     8.25%       |      8.25%      |
        # | INTERNAL-2 33% |    8.25%      |     8.25%     |     8.25%       |      8.25%      |
        # | EXTERNAL-3 33% |    8.25%      |     8.25%     |     8.25%       |      8.25%      |
        # ______________________________________________________________________________________
        # Profile settings
        if phase == 'MAIN':  # The experiment
            self.exp_time = 2 * 60 * 60 * 1000  # time in ms
            self.mode_sel = 'DEBUG'
            self.it_time = 7000  # average iteration time in ms (it was 625 ms)
            self.jitter = 1000  # jitter time in ms
            self.T = [0.34, 0.33, 0.33]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.25, 0.25, 0.25, 0.25]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS
        elif phase == 'SRC_TRAIN':  # The Time Training Phase
            self.exp_time = 3 * 60 * 1000  # 3 mins time in ms
            self.mode_sel = 'DEBUG'
            self.it_time = 7000  # average iteration time in ms (it was 625 ms)
            self.jitter = 1000  # jitter time in ms
            self.T = [0.5, 0.5, 0.0]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.5, 0.5, 0.0, 0.0]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS
        elif phase == 'NAVI_TRAIN':  # The Navigation Training Phase
            self.exp_time = 3 * 60 * 1000  # 3 mins time in ms
            self.mode_sel = 'DEBUG'
            self.it_time = 7000  # average iteration time in ms (it was 625 ms)
            self.jitter = 1000  # jitter time in ms
            self.T = [0.5, 0.5, 0.0]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.0, 0.0, 0.5, 0.5]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS
        elif phase == 'OV_TRAIN':  # The complete training phase (Not working well!)
            self.exp_time = 20 * 60 * 1000  # 20 mins time in ms
            self.mode_sel = 'DEBUG'
            self.threshold = 0.05
            self.train_maxtime = 20*60*1000  # 20 mins in ms, it can be changed
            self.it_time = 7000  # average iteration time in ms (it was 625 ms)
            self.jitter = 1000  # jitter time in ms
            self.T = [0.34, 0.33, 0.33]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.25, 0.25, 0.25, 0.25]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS

        # self.generate()  # I call in __init__ the generation, so at startup the routine will be launched

    def generate(self):
        # adaptation for using debug and batch modes
        if self.mode_sel == 'DEBUG':
            self.gen_time()
            self.task_sorting()

    def generate_batch(self, n_thread):
        self.gen_time()
        check = self.task_sorting(n_thread)
        if check:
            return True
        elif not check:
            return False

    def gen_time(self):
        self.TIME.append(250)
        tot_time = self.TIME[-1]
        iter = 1
        residual = 1e-4

        while tot_time < self.exp_time:
            try_time = self.TIME[-1] + self.it_time + uniform(-self.jitter, +self.jitter)
            if (try_time / (iter + 1)) - self.it_time <= residual:  # Condition where we check that the mean is maintained at it_time
                self.TIME.append(try_time)
                tot_time = try_time
                iter = iter + 1

    def task_sorting(self, n_thr=-1):
        Tval = [1, 2, 3]
        STval = [1, 4, 5, 6]
        ST_max = np.zeros((3, 4))
        min_d = 100
        self.dev_per = 0

        for i in range(0, 3):
            actual_its = 0  # so we check if we overflow the occurrences
            for j in range(0, 4):
                ST_max[i][j] = round(self.T[i] * self.ST[j] * (len(self.TIME) - 1))
                actual_its += ST_max[i][j]
            k = 4
            while actual_its != round(self.T[i] * (len(self.TIME) - 1)):  # We will first try redux the number of change
                k -= 1  # external task to repeat until convergence
                if actual_its > round(self.T[i] * (len(self.TIME) - 1)):  # considering the actual probability
                    ST_max[i][k] = ST_max[i][k] - 1
                    actual_its -= 1
                elif actual_its < round(self.T[i] * (len(self.TIME) - 1)):
                    ST_max[i][k] = ST_max[i][k] + 1
                    actual_its += 1
                if k == 0:
                    k = 4

        k = 0
        CONVERGE = False
        broken = False
        start = time.time()
        while not CONVERGE:

            self.SWITCH = []
            self.TASK = []
            occurrences = np.zeros((3, 4))
            for _ in range(len(self.TIME) - 1):
                if not self.SWITCH and not self.TASK:
                    els = choices(Tval, self.T)[0]
                    elt = choices(STval, self.ST)[0]
                    self.SWITCH.append(els)
                    self.TASK.append(elt)
                    occurrences[Tval.index(els)][STval.index(elt)] += 1
                else:
                    self.SWITCH.append(choices(Tval, self.T)[0])
                    last = self.SWITCH[-1]
                    if last == 1:
                        self.TASK.append(self.TASK[-1])
                        occurrences[Tval.index(1)][STval.index(self.TASK[-1])] += 1
                    elif last == 2:
                        if self.TASK[-1] == 1:
                            self.TASK.append(4)
                            occurrences[Tval.index(2)][STval.index(4)] += 1
                        elif self.TASK[-1] == 4:
                            self.TASK.append(1)
                            occurrences[Tval.index(2)][STval.index(1)] += 1
                        elif self.TASK[-1] == 5:
                            self.TASK.append(6)
                            occurrences[Tval.index(2)][STval.index(6)] += 1
                        elif self.TASK[-1] == 6:
                            self.TASK.append(5)
                            occurrences[Tval.index(2)][STval.index(5)] += 1
                    elif last == 3:
                        if self.TASK[-1] == 1 or self.TASK[-1] == 4:
                            elt = choices(STval[2:4], self.ST[2:4])[0]
                            self.TASK.append(elt)
                            occurrences[Tval.index(3)][STval.index(elt)] += 1
                        else:
                            elt = choices(STval[0:2], self.ST[0:2])[0]
                            self.TASK.append(elt)
                            occurrences[Tval.index(3)][STval.index(elt)] += 1

            acc_matrix = abs(occurrences - ST_max)
            max_dev = 0
            for i in range(len(acc_matrix)):
                for j in range(len(acc_matrix[i])):
                    if acc_matrix[i][j] > max_dev:
                        max_dev = acc_matrix[i][j]
                        row = i
                        col = j
            self.dev_per = (max_dev / occurrences[row][col])
            if min_d > self.dev_per:
                min_d = self.dev_per
            if self.dev_per <= self.threshold:
                CONVERGE = True
            elif self.phase == 'SRC_TRAIN' or self.phase == 'OV_TRAIN':
                CONVERGE = True

            if k == 3000:
                if n_thr == -1:
                    print('Convergence Failed, Repeat.')
                else:
                    print('Convergence Failed on Thread ', n_thr, ', Repeat.')
                broken = True
                break
            k += 1

        # Apply the first case
        self.SWITCH.insert(0, 0)
        if self.SWITCH[1] == 1:
            self.TASK.insert(0, self.TASK[0])
        elif self.SWITCH[1] == 2:
            if self.TASK[0] == 1:
                self.TASK.insert(0, 4)
            elif self.TASK[0] == 4:
                self.TASK.insert(0, 1)
            elif self.TASK[0] == 5:
                self.TASK.insert(0, 6)
            elif self.TASK[0] == 6:
                self.TASK.insert(0, 5)
        elif self.SWITCH[1] == 3:
            if self.TASK[0] == 1 or self.TASK[0] == 4:
                self.TASK.insert(0, choices(STval[2:4], self.ST[2:4])[0])
            else:
                self.TASK.insert(0, choices(STval[0:2], self.ST[0:2])[0])

        # Fill out the vector of return to SEARCH position
        for i in range(0, len(self.SWITCH)):
            if self.SWITCH[i] == 3 and self.TASK[i] in [1, 4]:
                self.NAV_to_SRC.append(i)

        if broken:
            print("Min Deviation obtained: ", "{:.3f}".format(min_d * 100), " %")
            return False
        elif not broken:
            if n_thr != -1:
                print('# From Thread: ', n_thr)
            print("Vector ultimated in ", "{:.3f}".format(time.time() - start), " sec, after ", k, " iterations.")
            print("Deviation: ", "{:.3f}".format(self.dev_per * 100), " %")
            return True
