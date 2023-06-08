# input.py>
# Library used for user Input (Numpad/Flight Stick)
# Imported in events as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
from psychopy import event

# Still to implement:
# Flight Stick input code, considering also increasing speed of translation/rotation with respect of angle of flight stick
# Translation on 2 axis for Waypoint Navigation, Rotation by inclining the stick at left or right for Heading Navigation


def get_num_keys():
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

    keys = event.getKeys(keyList=key_map.keys())
    for key in keys:
        if key in key_map and key.isnumeric():
            return int(key_map[key])
        else:
            return key_map[key]

    return None

# Here must be added the Flight Stick input code
