# input.py>
# Library used for user Input (Numpad/Flight Stick)
# Imported in events as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import pygame.joystick
from psychopy.hardware import keyboard
import pysticks
import numpy as np


class keyBoard():
    def __init__(self):
        self.kbHandler = keyboard.Keyboard()
        # About the RT that new keyboard component gives
        # link: https://discourse.psychopy.org/t/cant-use-the-new-keyboard-component-from-psychtoolbox/7634
    def get_num_keys(self):
        # Get key event: Generate a Keylog function
        key_map = {  # 0 is not allowed as Input
            'num_1': '6',
            'num_2': '7',
            'num_3': '8',
            'num_4': '3',
            'num_5': '4',
            'num_6': '5',
            'num_7': '0',
            'num_8': '1',
            'num_9': '2',
            's': 's',
            'escape': 'escape'
        }

        keys = self.kbHandler.getKeys(keyList=key_map.keys(), clear=True)
        out_pkg = [None, None]
        for key in keys:
            if key.name in key_map and key.name.isnumeric():
                out_pkg = [int(key_map[key.name]), key.rt]
                return out_pkg
            else:
                out_pkg = [key_map[key.name], key.rt]
                return out_pkg

        return out_pkg


# Here must be added the Flight Stick input code
class fstick():
    def __init__(self):
        # Init the necessary variable for the class
        self.joy_hdlr = None  # Handler of the Joystick
        self.joy_id = None  # ID of the Joystick
        self.deadband = None  # Deadzone of the flightstick Axis-0
        self.n_axes = None  # It will hold all the axes available
        self.n_buttons = None  # Same, but for the buttons
        self.rad = 0.0  # Variable for the angle of the joystick, in radians
        self.deg = 0.0  # Variable for the angle of the joystick, in degrees
        self.v_rad = 0.0  # Variable for the speed commanded by of the joystick, in rad/s
        self.v_deg = 0.0  # Variable for the speed commanded by of the joystick, in rad/s
        self.max_turn_deg = 16.0  # deg/s
        self.max_turn_rad = self.max_turn_deg*(np.pi/180)
        self.weights = None  # IF WE WANT: Vector for calibrating the rate of turning of the compass when commanded by joystick
        self.startup()

    def startup(self):
        # Init the variables here
        self.joy_id = pysticks.get_controller()
        self.joy_hdlr = pysticks.Controller
        # I assume only a single controller in my experiment
        if self.joy_id:
            print('Flight Stick found.')
        elif not self.joy_id:
            print('Flight Stick not found. Check connection')
            return

        # Set the deadend, from https://gamepad-tester.com/ I notice the max deadend of our Logitech should be 0.06
        self.deadband = 0.27  # Standard is 0.05, but we should balance it in the pretest
        self.joy_id.STICK_DEADBAND = self.deadband  # This will refuse all the command from [-self.deadband,self.deadband]

    def enable_fs(self):
        if self.joy_id is None:
            self.joy_id = pysticks.get_controller()

    def disable_fs(self):
        if self.joy_id is not None:
            self.joy_id.joystick.quit()
            pygame.display.quit()
            self.joy_id = None


    def get_finput(self, dtime):
        # get input data
        if self.joy_id:
            self.joy_hdlr.update(self.joy_id)
            joy_data = self.joy_hdlr.getRoll(self.joy_id)
            if joy_data is not None:
                a0_val = joy_data  # We are interested only in Axis-0
                # this value is between [-1,1], but we need to exclude the deadzone and convert to angle
                # Speeds
                self.v_deg = a0_val*self.max_turn_deg
                self.v_rad = a0_val*self.max_turn_rad
                # Angles
                self.deg = self.v_deg*dtime
                self.rad = self.v_rad*dtime
                if abs(a0_val) > self.deadband:
                    return True
