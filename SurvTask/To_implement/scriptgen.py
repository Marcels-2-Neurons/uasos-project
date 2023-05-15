# scriptgen.py>
# Library used as Script Generator for the experiment
# Imported in settings as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import random
from random import *
from mathandler import NORBd
import numpy as np
global Script

class ScriptGen:
    def __init__(self):
        self.exp_time = 2*60*60*1000  # time in ms
        self.jitter = 500   # jitter time in ms
        self.TIME = []  # time schedule vector 1xSize_exp
        self.SWITCH = []  # Task switch vector 1xSize_exp:
                          # 0-Just at start / 1-Repeat Task / 2-Switch Task Mode / 3-Switch Tasks
        self.TASK = []  # Task type vector 1xSize_exp
                        # 0-4 for the SRC Task, based on NORB Cats / 5-NAVI HDG / 6-NAVI WPY
        self.HDG = []   # HDG Vector: RESERVED FOR NAVI TASK, Random Heading inside here 1xSize_exp
        self.WPY = []   # WPY Vector: RESERVED FOR NAVI TASK, Random Waypoint inside here 1xSize_exp
        self.IMGS = []  # Images Array: RESERVED FOR SRC TASK, Random images here (0-911) 9xSize_exp
        self.FILS = []  # Filters Array: RESERVED FOR SRC TASK, Random Filter here, only for max 3 rand images changed
                        # If less than 3 images are changed, the blank cells will have 'None' value 3xSize_exp
        self.ROTS = []  # Rotations Array: RESERVED FOR SRC TASK, Random rotation here, only for max 3 rand images changed
                        # If less than 3 images are changed, the blank cells will have 'None' value 3xSize_exp
        self.CORS = []  # Correct Array: RESERVED FOR SRC TASK, Correct cells are here 9xSize_exp


    def generate(self):
        self.TIME.append(500) # First iteration

        while self.TIME[-1] < self.exp_time:
            if self.TIME[-1] == 500:
                #  Execute code for first iteration
                self.task_sel()
            else:
                #  Execute remaining code
                self.task_sel()
            self.TIME.append(self.TIME[-1] + 2000 + uniform(-self.jitter,+self.jitter))


    def task_sel(self):
        if self.TIME[-1] == 500: # Initial case
            self.SWITCH.append(0)
            if True: #uniform(0,1) > 0.5: # 50/50 possibility of SRC or NAV
                self.TASK.append(randint(0,4)) # SRC
            else:
                self.TASK.append(randint(5,6)) # NAV
            self.random_imgs()
            self.correct_imgs()
        else:
            self.SWITCH.append(randint(1, 3))
            if self.SWITCH[-1] == 1: # Repeat Task Case
                self.TASK.append(self.TASK[-1])
            elif self.SWITCH[-1] == 2 and self.TASK[-1] in range(0,5,1): # Internal SRC Task Case
                self.TASK.append(choice([x for x in range(0,5) if x != self.TASK[-1]]))
            elif self.SWITCH[-1] == 2 and self.TASK[-1] in range(5,7,1): # Internal NAV Task Case
                self.TASK.append(choice([x for x in range(5,7) if x != self.TASK[-1]]))
            elif self.SWITCH[-1] == 3 and self.TASK[-1] in range(0,5,1): # External SRC to NAV
                self.TASK.append(randint(5,6))
            elif self.SWITCH[-1] == 3 and self.TASK[-1] in range(5,7,1): # External NAV to SRC
                self.TASK.append(randint(0,4))
            self.random_imgs()  # I will generate first a new bunch of imgs, so I can implement the correct function
            self.correct_imgs()


    def random_imgs(self):
        # Function that handles the image generations
        if self.TIME[-1] == 500:
            # Initialize the arrays' vectors
            self.IMGS.append([0,0,0,0,0,0,0,0,0])
            self.FILS.append([0,0,0,0,0,0,0,0,0])
            self.ROTS.append([0,0,0,0,0,0,0,0,0])
            for i in range(0,9):
                self.IMGS[0][i] = randint(0,911)
                while i != 0 and self.IMGS[0][i] in self.IMGS[0][0:i-1]:
                    self.IMGS[0][i] = randint(0,911) # to check if the images are unique

                self.FILS[0][i] = randint(0,7)  # Random Filter sel
                                                # 0-'None',1-'Gaussian',2-'SaltAndPepper',3-'Poisson',4-'Speckle',5-'Blur',6-'Tearing',7-'MPEG'
                self.ROTS[0][i] = randint(0,3)  # Random Rotation
                                                # 0-'Original',1-'90deg CClock',2-'180deg CClock',3-'270deg CClock'
        else:
            self.IMGS.append(self.IMGS[-1].copy())
            self.FILS.append(self.FILS[-1].copy())
            self.ROTS.append(self.ROTS[-1].copy())
            Max = randint(1,3)
            for i in range(0,Max):
                idx = randint(0,8)
                self.IMGS[-1][idx] = randint(0,911)
                while idx==0 and self.IMGS[-1][idx] in self.IMGS[-1][1:idx-1]:
                    self.IMGS[-1][idx] = randint(0, 911)  # to check if the images are unique before 0
                while idx!=0 and self.IMGS[-1][idx] in self.IMGS[-1][0:idx-1]:
                    self.IMGS[-1][idx] = randint(0,911) # to check if the images are unique before idx
                while idx!=8 and self.IMGS[-1][idx] in self.IMGS[-1][idx+1:]:
                    self.IMGS[-1][idx] = randint(0, 911) # to check if the images are unique after idx
                self.FILS[-1][idx] = randint(0,7)
                self.ROTS[-1][idx] = randint(0, 3)


    def correct_imgs(self):
        # Function that handles the recovering of the correct cells
        self.CORS.append([0, 0, 0, 0, 0, 0, 0, 0, 0]) # Switch ON/OFF like
        if self.TASK[-1] in range(0,5,1):
            digit_chk = str(self.TASK[-1])
            for idx, num in enumerate(self.IMGS[-1]):
                if digit_chk in str(NORBd.get_cat(num)):
                    self.CORS[-1][idx] = 1
                else:
                    pass
        else:
            pass



Script = ScriptGen()