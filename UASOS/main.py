# Main of the Surveillance Task Experiment
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
#############################################################################
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import questions
# from settings import set
from SRCevents import SRCwin
from questions import *


if __name__ == "__main__":
    # Request subject data!
    subject_fullform()
    # Call of the instance SRCTask
    SRCwin.USER_ID = questions.ans.ID  # Now it changes time by time
    SRCwin.run()
