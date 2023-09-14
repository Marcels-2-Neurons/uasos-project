# scriptgen_old2.py>
# Library used as Script Generator for the experiment
# Imported in settings as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import csv
from random import *
import time
from mathandler import NORBd
from copy import *
import numpy as np

global script


# Still to implement:
# Randomization of the angles/grid sectors cases Heading and Waypoint
# Batch mode from csv file


class ScriptGen:
    def __init__(self, phase='MAIN', exclude=-1):
        from settings import set
        self.exp_time = 2 * 60 * 60 * 1000  # time in ms
        self.it_time = 3500  # average iteration time in ms (it was 625 ms)
        self.jitter = 375  # jitter time in ms

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
        self.durs = []
        self.max_no_correct = 4  # Max number of correct images
        self.NAV_to_SRC = []  # Array in which we store all the position of where we have a return to SRC
        self.purge = False  # Trigger for maximize changes to reduce targets
        self.Max = 0  # Potential no of changes
        self.locp = []  # location vector of people
        self.locv = []  # location vector of vehicles
        self.CORSt = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # last correct iteration in case of NAV
        self.threshold = 0.03
        self.dev_per = 0
        self.mode_sel = 'BATCH'  # 'BATCH'
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
            self.exp_time = set.exp_time_main  # time in ms
            self.mode_sel = 'BATCH'
            self.it_time = set.it_time  # average iteration time in ms (it was 625 ms)
            self.jitter = set.jitter  # jitter time in ms
            self.T = [0.34, 0.33, 0.33]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.25, 0.25, 0.25, 0.25]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS
        elif phase == 'SRC_TRAIN':  # The Time Training Phase
            self.exp_time = set.exp_time_srct  # 3 mins time in ms
            self.mode_sel = 'BATCH'
            self.it_time = set.it_time  # average iteration time in ms (it was 625 ms)
            self.jitter = set.jitter  # jitter time in ms
            self.T = [0.5, 0.5, 0.0]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.5, 0.5, 0.0, 0.0]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS
        elif phase == 'NAVI_TRAIN':  # The Navigation Training Phase
            self.exp_time = set.exp_time_navt  # 3 mins time in ms
            self.mode_sel = 'BATCH'
            self.it_time = set.it_time  # average iteration time in ms (it was 625 ms)
            self.jitter = set.jitter  # jitter time in ms
            self.T = [0.5, 0.5, 0.0]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.0, 0.0, 0.5, 0.5]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS
        elif phase == 'OV_TRAIN':  # The complete training phase
            self.exp_time = set.exp_time_ovt  # 10 mins time in ms
            self.mode_sel = 'BATCH'
            self.threshold = 0.03
            self.train_maxtime = set.exp_time_ovt  # 20 mins in ms, it can be changed
            self.it_time = set.it_time  # average iteration time in ms (it was 625 ms)
            self.jitter = set.jitter  # jitter time in ms
            self.T = [0.34, 0.33, 0.33]  # REPEAT TASK/INTERNAL TASK SWITCH/EXTERNAL TASK SWITCH
            self.ST = [0.25, 0.25, 0.25, 0.25]  # SEARCH PEOPLE/SEARCH VEHICLES/FLY BY HEADING/FLY BY WAYPOINTS

        # Parameters for the simulation
        # self.V = 313/3.6  # Cruise speed in m/s
        # self.mvHDG = 16*(np.pi/180) # Based on MQ-1 Turn Time: 22s (WarThunder)
        # self.map_size = 13  # Half size of the map. in km
        # self.sq_len = 26  # Dimension of the square in km
        # self.scale = 1/1000  # Scale 1 cell 1000 meters
        # self.ratio = (2*self.map_size)/(self.sq_len*1000)  # NEEDS REWRITE! It should change to relative position in the map

        self.generate()  # I call in __init__ the generation, so at startup the routine will be launched

    def generate(self):
        # adaptation for using debug and batch modes
        global val_m  # recall of the global value inside
        if self.mode_sel == 'DEBUG':
            # self.threshold = 0.05

            self.gen_time()
            self.task_sorting()
            # these steps will not be made for NAVI_TRAIN
            if self.phase != 'NAVI_TRAIN':
                self.generate_imgs()
                self.final_cor_chk()
            else:
                pass  # TODO I will add here the HDG and WPY generation
        elif self.mode_sel == 'BATCH':  # TODO ADD THE NEW SCRIPTS DSETS
            if self.phase == 'MAIN' or self.phase == 'OV_TRAIN':
                scriptsDb = "./scripts/scripts_dset.csv"
            elif self.phase == 'SRC_TRAIN':
                scriptsDb = "./scripts/scripts_SRC_train.csv"
            elif self.phase == 'NAVI_TRAIN':
                scriptsDb = "./scripts/scripts_NAVI_train.csv"

            with open(scriptsDb, "r", newline="") as scriptsDb:
                reader = csv.reader(scriptsDb, delimiter='\t')
                n_rows = len(list(reader))
                scriptsDb.seek(0)  # Return the reader index at start
                dim = round(n_rows / 3)
                if self.exclude != -1:
                    sel_script = self.exclude
                    while sel_script == self.exclude:
                        sel_script = randint(0, dim - 1)
                else:
                    sel_script = randint(0, dim - 1)
                    self.exclude = sel_script
                for i, row in enumerate(reader):
                    if i == 3 * sel_script:
                        self.TIME = [float(value) for value in row]
                    elif i == (3 * sel_script + 1):
                        self.SWITCH = [int(value) for value in row]
                    elif i == (3 * sel_script + 2):
                        self.TASK = [int(value) for value in row]
                        break
                    else:
                        pass

            if self.phase == 'OV_TRAIN':
                for idx, val in enumerate(self.TIME):
                    if val >= self.train_maxtime:
                        cut_now = idx
                        vec1 = deepcopy(self.TIME[:cut_now])
                        vec2 = deepcopy(self.SWITCH[:cut_now])
                        vec3 = deepcopy(self.TASK[:cut_now])
                        # clean the vectors
                        self.TIME.clear()
                        self.SWITCH.clear()
                        self.TASK.clear()
                        # Reapply the values
                        self.TIME = deepcopy(vec1)
                        self.SWITCH = deepcopy(vec2)
                        self.TASK = deepcopy(vec3)
                        print(f'Training vector cut down to {cut_now} elements')
                        break

            # Fill out the vector of return to SEARCH position
            for i in range(0, len(self.SWITCH)):
                self.HDG.append(-1)
                self.WPY.append("NaN")
                self.WPY_tuple.append((-1, -1))
                if self.SWITCH[i] == 3 and self.TASK[i] in [1, 4]:
                    self.NAV_to_SRC.append(i)

            if self.phase != 'NAVI_TRAIN':
                self.generate_imgs()
                self.final_cor_chk()
            elif self.phase != 'SRC_TRAIN':
                # TODO This is to generate the NAVI Requests
                pass

            # Calculate durations
            self.calc_durations()
            return

    def generate_batch(self, n_thread):
        self.gen_time()
        check = self.task_sorting(n_thread)
        if check:
            return True
        elif not check:
            return False

    def calc_durations(self):
        for i in range(0, len(self.TIME)-1):
            self.durs.append(self.TIME[i+1] - self.TIME[i])
        self.durs.append(7000)
        return

    def gen_time(self):
        self.TIME.append(250)
        tot_time = self.TIME[-1]
        iter = 1
        residual = 1e-4

        while tot_time < self.exp_time:
            try_time = self.TIME[-1] + self.it_time + uniform(-self.jitter, +self.jitter)
            if ((try_time) / (
                    iter + 1)) - self.it_time <= residual:  # Condition where we check that the mean is maintained at it_time
                self.TIME.append(try_time)
                tot_time = try_time
                iter = iter + 1

    def task_sorting(self, n_thr=-1):
        Tval = [1, 2, 3]
        STval = [1, 4, 5, 6]
        occurrences = np.zeros((3, 4))
        ST_max = np.zeros((3, 4))
        # self.threshold = 0.03
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
        # For DEBUG Purpose
        # print("SWITCH", "\t", "1", "\t", "4", "\t", "5", "\t", "6")
        # for i in range(0,3):
        #    print(i+1,"\t\t",occurrences[i][0],"\t",occurrences[i][1],"\t",occurrences[i][2],"\t",occurrences[i][3])

    def generate_imgs(self):
        i = 0  # counter of the position in the vector
        change = 0 if self.TASK[0] in [5, 6] else -1  # position of the NAV_to_SRC vector
        aval_img = [4, 4]  # 0-People, 1-Vehicle
        # Initialization
        # self.IMGS.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.FILS.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.ROTS.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.CORS.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        # Execution of the task
        while i != len(self.TIME):
            valid = False

            if i == 0:  # Case - Start event
                self.IMGS.append([])
                while not valid:
                    for j in range(0, 9):

                        # Define if Navigation or Search task at start
                        if self.TASK[i] == 1:
                            av = aval_img[0]
                        elif self.TASK[i] == 4:
                            av = aval_img[1]
                        elif self.TASK[i] in [5, 6]:
                            next: int = self.NAV_to_SRC[change]
                            if self.TASK[next] == 1:
                                av = aval_img[0]
                            elif self.TASK[next] == 4:
                                av = aval_img[1]

                        dice = choices([True, False], weights=[0.25 * av, 0.25 * (4 - av)])[0]
                        # dice = choices([True, False], weights=[0.125 * av, 0.125 * (4 + (4 - av))])[0]
                        # Dice that will select if it should be selected a target or no

                        if dice:  # Case TRUE: I have to add a target
                            check = False
                            while not check:  # Recursive loop until target
                                self.IMGS[i].append(randint(0, 971))  # random select
                                done = self.check_correct(iter=i, idx=j, num=self.IMGS[i][j], mode=self.TASK[i]) if \
                                    self.TASK[i] in [1, 4] \
                                    else self.check_correct(iter=i, idx=j, num=self.IMGS[i][j], mode=self.TASK[next])
                                # Change with implementation of sorting of the available cases
                                if done in [1, 2, 3] and len(self.IMGS[i]) == len(set(self.IMGS[i])):  # Case Targets
                                    if done == 1:
                                        if aval_img[0] > 0:
                                            aval_img[0] -= 1
                                            check = True
                                        else:
                                            del self.IMGS[i][j]
                                            check = False
                                    elif done == 2:
                                        if aval_img[1] > 0:
                                            aval_img[1] -= 1
                                            check = True
                                        else:
                                            del self.IMGS[i][j]
                                            check = False
                                    elif done == 3:
                                        if aval_img[0] > 0 and aval_img[1] > 0:
                                            aval_img[0] -= 1
                                            aval_img[1] -= 1
                                            check = True
                                        else:
                                            del self.IMGS[i][j]
                                            check = False
                                elif done in [4, 5, 6] or len(self.IMGS[i]) != len(
                                        set(self.IMGS[i])):  # Case Non-Target
                                    del self.IMGS[i][j]
                                    check = False


                        elif not dice:
                            check = False
                            while not check:  # Recursive loop until target
                                check = False
                                self.IMGS[i].append(randint(0, 971))  # random select
                                done = self.check_correct(iter=i, idx=j, num=self.IMGS[i][j], mode=self.TASK[i]) if \
                                    self.TASK[i] in [1, 4] \
                                    else self.check_correct(iter=i, idx=j, num=self.IMGS[i][j], mode=self.TASK[next])
                                if done in [4, 5, 6] and len(self.IMGS[i]) == len(set(self.IMGS[i])):  # Case Targets
                                    if done == 4:
                                        if aval_img[1] > 0:
                                            aval_img[1] -= 1
                                            check = True
                                        else:
                                            del self.IMGS[i][j]
                                            check = False
                                    elif done == 5:
                                        if aval_img[0] > 0:
                                            aval_img[0] -= 1
                                            check = True
                                        else:
                                            del self.IMGS[i][j]
                                            check = False
                                    elif done == 6:
                                        check = True

                                elif done in [1, 2, 3] or len(self.IMGS[i]) != len(set(self.IMGS[i])):  # Case Targets
                                    del self.IMGS[i][j]
                                    check = False

                        # Apply Filters and Rotations
                        self.FILS[i][j] = randint(0, 7)  # Random Filter sel
                        # 0-'None',1-'Gaussian',2-'SaltAndPepper',3-'Poisson',4-'Speckle',5-'Blur',6-'Tearing',7-'MPEG'
                        self.ROTS[i][j] = randint(0, 3)  # Random Rotation
                        # 0-'Original',1-'90deg CClock',2-'180deg CClock',3-'270deg CClock'

                    # Case of starting with Navi - Save last iter and clean the CORS vector
                    if self.TASK[i] in [5, 6]:
                        self.CORSt = deepcopy(self.CORS[i])
                        self.CORS[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

                    if self.TASK[i] in [1, 4]:  # This is when I have Search Task, it validates
                        if self.CORS[i].count(1) <= 4:
                            valid = True
                        else:
                            del self.IMGS[i]  # flush the data
                    else:
                        if self.CORSt.count(1) <= 4:
                            valid = True
                        else:
                            del self.IMGS[i]

            elif i != 0 and self.TASK[i] in [1, 4]:  # Search Case
                # Initialization of the FILS and ROTS vectors for this iteration
                self.FILS.append(deepcopy(self.FILS[i - 1]))
                self.ROTS.append(deepcopy(self.ROTS[i - 1]))

                self.Max = randint(1, 3)  # Normal selection of random No of changes
                purge_p = True if len(self.locp) > 4 else False
                purge_v = True if len(self.locv) > 4 else False

                while not valid:
                    self.IMGS.append(deepcopy(self.IMGS[i - 1]))  # copy the last iteration for proceeding the change
                    # Check the actual availabilities
                    aval_img[0] = 4 - len(self.locp)
                    aval_img[1] = 4 - len(self.locv)

                    vec_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                    for _ in range(0, self.Max if not (purge_p or purge_v) else 3):
                        # selection of the pool where to choose the index
                        if not (purge_p or purge_v):
                            idx = choice(vec_idx)
                        elif purge_p and purge_v:
                            del vec_idx
                            vec_idx = list(set(self.locv + self.locp))
                            idx = choice(vec_idx)
                        elif purge_p:
                            del vec_idx
                            vec_idx = deepcopy(self.locp)
                            idx = choice(vec_idx)
                        elif purge_v:
                            del vec_idx
                            vec_idx = deepcopy(self.locv)
                            idx = choice(vec_idx)

                        av = aval_img[0] if self.TASK[i] == 1 else aval_img[1]
                        dice = choices([True, False], weights=[0.25 * av, 0.25 * (4 - av)])[0]
                        # dice = choices([True, False], weights=[0.125 * av, 0.125 * (4 + (4 - av))])[0]
                        # Dice that will select if it should be selected a target or not
                        if dice:
                            check = False
                            while not check:  # Recursive loop until target
                                last_val = self.IMGS[i][idx]
                                self.IMGS[i][idx] = randint(0, 971)  # random select
                                done = self.check_correct(iter=i, idx=idx, num=self.IMGS[i][idx], mode=self.TASK[i])
                                # Change with implementation of sorting of the available cases
                                if done in [1, 2, 3] and len(self.IMGS[i]) == len(set(self.IMGS[i])):  # Case Targets
                                    if done == 1:
                                        if aval_img[0] > 0:
                                            aval_img[0] -= 1
                                            del vec_idx[
                                                vec_idx.index(idx)]  # remove the changed index from the candidates
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 2:
                                        if aval_img[1] > 0:
                                            aval_img[1] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 3:
                                        if aval_img[0] > 0 and aval_img[1] > 0:
                                            aval_img[0] -= 1
                                            aval_img[1] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                elif done in [4, 5, 6] or len(self.IMGS[i]) != len(
                                        set(self.IMGS[i])):  # Case Non-Target
                                    self.IMGS[i][idx] = last_val
                                    check = False

                        elif not dice:
                            check = False
                            while not check:  # Recursive loop until target
                                last_val = self.IMGS[i][idx]
                                self.IMGS[i][idx] = randint(0, 971)  # random select
                                done = self.check_correct(iter=i, idx=idx, num=self.IMGS[i][idx], mode=self.TASK[i])
                                # Change with implementation of sorting of the available cases
                                if done in [4, 5, 6] and len(self.IMGS[i]) == len(
                                        set(self.IMGS[i])):  # Case Non-Targets
                                    if done == 4:
                                        if aval_img[1] > 0:
                                            aval_img[1] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 5:
                                        if aval_img[0] > 0:
                                            aval_img[0] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 6:
                                        del vec_idx[vec_idx.index(idx)]
                                        check = True

                                elif done in [1, 2, 3] or len(self.IMGS[i]) != len(set(self.IMGS[i])):  # Case Targets
                                    self.IMGS[i][idx] = last_val
                                    check = False
                        # Apply Filters and Rotations
                        self.FILS[i][idx] = randint(0, 7)  # Random Filter sel
                        # 0-'None',1-'Gaussian',2-'SaltAndPepper',3-'Poisson',4-'Speckle',5-'Blur',6-'Tearing',7-'MPEG'
                        self.ROTS[i][idx] = randint(0, 3)  # Random Rotation
                        # 0-'Original',1-'90deg CClock',2-'180deg CClock',3-'270deg CClock'

                    # Validation Process
                    if self.CORS[i].count(1) <= 4:
                        valid = True
                    else:
                        self.IMGS[i] = deepcopy(self.IMGS[i - 1])

            elif i != 0 and self.TASK[i] in [5, 6]:  # Navigation Case
                # Initialization of the FILS and ROTS vectors for this iteration
                self.FILS.append(deepcopy(self.FILS[i - 1]))
                self.ROTS.append(deepcopy(self.ROTS[i - 1]))
                if self.TASK[i - 1] in [1, 4] and self.SWITCH[i] == 3:  # Checks the External Switch case
                    change += 1

                next: int = self.NAV_to_SRC[change] if change <= len(self.NAV_to_SRC) - 1 else self.NAV_to_SRC[
                    len(self.NAV_to_SRC) - 1]  # I send to people, it is not so important

                self.Max = randint(1, 3)  # Normal selection of random No of changes
                purge_p = True if len(self.locp) > 4 else False
                purge_v = True if len(self.locv) > 4 else False

                while not valid:
                    self.IMGS.append(deepcopy(self.IMGS[i - 1]))  # copy the last iteration for proceeding the change
                    # Check the actual availabilities
                    aval_img[0] = 4 - len(self.locp)
                    aval_img[1] = 4 - len(self.locv)
                    vec_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8]

                    for _ in range(0, self.Max if not (purge_p or purge_v) else 3):
                        # selection of the pool where to choose the index
                        if not (purge_p or purge_v):
                            idx = choice(vec_idx)
                        elif purge_p and purge_v:
                            del vec_idx
                            vec_idx = list(set(self.locv + self.locp))
                            idx = choice(vec_idx)
                        elif purge_p:
                            del vec_idx
                            vec_idx = deepcopy(self.locp)
                            idx = choice(vec_idx)
                        elif purge_v:
                            del vec_idx
                            vec_idx = deepcopy(self.locv)
                            idx = choice(vec_idx)

                        av = aval_img[0] if self.TASK[next] == 1 else aval_img[1]
                        dice = choices([True, False], weights=[0.25 * av, 0.25 * (4 - av)])[0]
                        # dice = choices([True, False], weights=[0.125 * av, 0.125 * (4 + (4 - av))])[0]
                        # Dice that will select if it should be selected a target or not

                        if dice:
                            check = False
                            while not check:  # Recursive loop until target
                                last_val = self.IMGS[i][idx]
                                self.IMGS[i][idx] = randint(0, 971)  # random select

                                done = self.check_correct(iter=i, idx=idx, num=self.IMGS[i][idx], mode=self.TASK[next])
                                # Change with implementation of sorting of the available cases
                                if done in [1, 2, 3] and len(self.IMGS[i]) == len(set(self.IMGS[i])):  # Case Targets
                                    if done == 1:
                                        if aval_img[0] > 0:
                                            aval_img[0] -= 1
                                            del vec_idx[
                                                vec_idx.index(idx)]  # remove the changed index from the candidates
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 2:
                                        if aval_img[1] > 0:
                                            aval_img[1] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 3:
                                        if aval_img[0] > 0 and aval_img[1] > 0:
                                            aval_img[0] -= 1
                                            aval_img[1] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                elif done in [4, 5, 6] or len(self.IMGS[i]) != len(
                                        set(self.IMGS[i])):  # Case Non-Target
                                    self.IMGS[i][idx] = last_val
                                    check = False

                        elif not dice:
                            check = False
                            while not check:  # Recursive loop until target
                                last_val = self.IMGS[i][idx]
                                self.IMGS[i][idx] = randint(0, 971)  # random select

                                done = self.check_correct(iter=i, idx=idx, num=self.IMGS[i][idx], mode=self.TASK[next])
                                # Change with implementation of sorting of the available cases
                                if done in [4, 5, 6] and len(self.IMGS[i]) == len(
                                        set(self.IMGS[i])):  # Case Non-Targets
                                    if done == 4:
                                        if aval_img[1] > 0:
                                            aval_img[1] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 5:
                                        if aval_img[0] > 0:
                                            aval_img[0] -= 1
                                            del vec_idx[vec_idx.index(idx)]
                                            check = True
                                        else:
                                            self.IMGS[i][idx] = last_val
                                            check = False
                                    elif done == 6:
                                        del vec_idx[vec_idx.index(idx)]
                                        check = True

                                elif done in [1, 2, 3] or len(self.IMGS[i]) != len(set(self.IMGS[i])):  # Case Targets
                                    self.IMGS[i][idx] = last_val
                                    check = False

                        # Apply Filters and Rotations
                        self.FILS[i][idx] = randint(0, 7)  # Random Filter sel
                        # 0-'None',1-'Gaussian',2-'SaltAndPepper',3-'Poisson',4-'Speckle',5-'Blur',6-'Tearing',7-'MPEG'
                        self.ROTS[i][idx] = randint(0, 3)  # Random Rotation
                        # 0-'Original',1-'90deg CClock',2-'180deg CClock',3-'270deg CClock'

                    # Case Navi - Save last iter and clean the CORS vector
                    if self.TASK[i] in [5, 6]:
                        self.CORSt = deepcopy(self.CORS[i])
                        self.CORS[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

                    # Validation Process
                    if self.CORSt.count(1) <= 4:
                        valid = True
                    else:
                        self.IMGS[i] = deepcopy(self.IMGS[i - 1])

            if i == len(self.TIME) - 1:  # For Debug
                print('No. Time Steps', i + 1)
            i += 1

    def check_correct(self, iter=-1, idx=0, num=0, mode=0):  # This time the check is per-value, for cleariness purpose
        digit_chk = str(mode)
        # Check corrector vector alloc
        if len(self.CORS) != iter + 1:
            self.CORS.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        else:
            pass

        if digit_chk in NORBd.get_cat(num):
            self.CORS[iter][idx] = 1
            if mode == 1 and self.find('1', NORBd.get_cat(num)) == 1:  # Case people
                self.look_tgts(iter)  # Function to update the location tables
                return 1
            elif mode == 4 and self.find('4', NORBd.get_cat(num)) == 1:  # Case vehicle
                self.look_tgts(iter)
                return 2
            elif (mode == 4 or mode == 1) and (
                    self.find('1', NORBd.get_cat(num)) + self.find('4', NORBd.get_cat(num))) == 2:  # Case both
                self.look_tgts(iter)
                return 3
        else:
            self.CORS[iter][idx] = 0
            if mode == 1 and self.find('4', NORBd.get_cat(num)) == 1:  # Case vehicle
                self.look_tgts(iter)
                return 4
            elif mode == 4 and self.find('1', NORBd.get_cat(num)) == 1:  # Case people
                self.look_tgts(iter)
                return 5
            elif (self.find('1', NORBd.get_cat(num)) + self.find('4', NORBd.get_cat(num))) == 0:  # Case no targets
                self.look_tgts(iter)
                return 6

    def look_tgts(self, iter):
        if len(self.IMGS[iter]) == 9:  # always update the location vectors if the length is full
            self.locp = [idx for idx, val in enumerate(self.IMGS[iter]) if self.find('1', NORBd.get_cat(val)) == 1]
            self.locv = [idx for idx, val in enumerate(self.IMGS[iter]) if self.find('4', NORBd.get_cat(val)) == 1]

    def find(self, char, str):
        return 1 if str.find(char) != -1 else 0

    def final_cor_chk(self):
        # It overrides only the CORS vectors to guarantee that the targets are completely found
        for row in range(len(self.IMGS)):
            if self.TASK[row] in [1, 4]:
                digit_chk = str(self.TASK[row])
                for pic in range(len(self.IMGS[row])):
                    if digit_chk in NORBd.get_cat(self.IMGS[row][pic]):
                        self.CORS[row][pic] = 1
                    else:
                        self.CORS[row][pic] = 0
            else:
                self.CORS[row] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            if self.count_occurrences(self.CORS[row]) > 4:
                print('[WARNING] At step ', row, ' the no. of targets are > 4')

    def count_occurrences(self, vector):
        count = 0
        for element in vector:
            if element == 1:
                count += 1
        return count

    # NAV TASK ITERATIVE METHOD HERE, IT WILL BE CALLED FROM PYROSERVER AT EVERY FRAME!
    # NO BORDERS METHOD, WE WILL TRY TO CYCLE THE MAP
    def sel_HDG(self, HDG):
        # Enter Aeronautical HDG and Returns Aeronautical Heading
        # I should save the correct direction of the HDG turn
        nHDG = HDG
        while nHDG == HDG:
            nHDG = randint(0, 35)*10  # Every 10°
        return nHDG

    def sel_cell(self, x_lbl=None, y_lbl=None):
        # Enter Aeronautical HDG and Returns Aeronautical Heading
        # Change it following the px dimension of the map image
        # w_img = 11684
        # h_img = 11684
        out_WPY = [None, None]
        # pos 0 - WPY string, pos 1 - HDG float
        # x_coord = (w_img / 4 + x) / (225)
        # y_coord = (h_img / 4 - y) / (225)

        seed1 = randint(0, 3)
        seed2 = randint(0, 3)
        seed = (seed1+1, seed2+1)

        # Generate the waypoint from the randomized value
        # It needs a circular vector
        if y_lbl[seed2] in range(1, 10):
            numWPY = f'0{y_lbl[seed2]}'
        else:
            numWPY = f'{y_lbl[seed2]}'

        out_WPY[0] = x_lbl[seed1] + numWPY
        out_WPY[1] = seed

        return out_WPY

    def get_pos(self, x, y, HDG, nHDG, dir, dt, dTIME, V=313 / 3.6):
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
        x = x + u * dt * self.scale
        y = y + v * dt * self.scale
        # Calculate the HDG
        HDG = HDG + (vdHDG[0] * dt) * (180 / np.pi)
        # Pack it up
        out_pos = [x, y, HDG]
        return out_pos

    # COMPLETE WHEN TIEN WILL FINISH

    def calc_vHDG(self, HDG, nHDG, dir, dTIME):
        # Enter Aeronautical Heading
        # pos 0 - vHDG, pos 1 - dHDG
        # Needs rework to acquire the direction of the stick
        rdHDG = (nHDG - HDG) % 360  # Right turn dHDG
        ldHDG = (360 - rdHDG)  # Left turn dHDG

        if dir < 0:  # Case Left Turn
            dHDG = ldHDG
            vHDG = - (dHDG * (np.pi / 180)) / abs(dTIME)
        elif dir > 0:  # Case Right Turn
            dHDG = rdHDG
            vHDG = (dHDG * (np.pi / 180)) / abs(dTIME)

        # dHDG = (((nHDG-HDG)+180) % 360) - 180
        # vHDG = (dHDG * (np.pi/180))/abs(dTIME)

        if abs(vHDG) > self.mvHDG:
            if vHDG < 0:
                vHDG = -self.mvHDG
            elif vHDG > 0:
                vHDG = self.mvHDG

        out_vHDG = [vHDG, dHDG]  # The direction is inside here
        return out_vHDG

    def mathHDG(self, HDG):
        return 90 - HDG


script = ScriptGen(phase='MAIN')
script_s = ScriptGen(phase='SRC_TRAIN')
script_n = ScriptGen(phase='NAVI_TRAIN')
script_ov = ScriptGen(phase='OV_TRAIN', exclude=script.exclude)  # So we are sure that script and script_ov will not share the same script
