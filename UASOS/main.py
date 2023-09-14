# Main of the Surveillance Task Experiment
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
#############################################################################
import sys
import subprocess

# Load necessary modules to run the experiment
reqs_file = 'requirements.txt'
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', reqs_file])
    print('All modules installed. Ready to run!')
except subprocess.CalledProcessError as e:
    print(f'Error while installing modules: {e}')

import questions
from SRCevents import SRCwin
from questions import *

if __name__ == "__main__":
    # Request subject data!
    subject_fullform()
    # Call of the instance SRCTask
    SRCwin.USER_ID = questions.ans.ID  # Now it changes time by time
    SRCwin.setup_complete = True
    SRCwin.run()
