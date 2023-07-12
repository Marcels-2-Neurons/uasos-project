# lslmarkers.py>
# Library used for LSL Markers stream
# Imported in SRCevents and NAVevents as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

from pylsl import StreamInfo, StreamOutlet


class lslmarkers():
    def __init__(self, type_m=None):
        self.marker = None
        self.bsample = []
        # Example Marker: TYP-WHT-A-B
        # TYP : it's the type of the marker, Image, Heading, Waypoint, Usage of controls or Response
        # WHT : What has been sent, 00X if Position in a matrix, XXX for a heading in deg, LXX (letter and 2 digits)
        # for the waypoint
        # A: Which category is the update (1-src people, 4-src vehicles,5-nav heading, 6- nav waypoint)
        # B: Is the update TGT or No-TGT? (0-No TGT, 1-TGT) if TYP is IMG/HDG/WPY

        self.type = {
            'IMG': 'IMG',  # New Image in the matrix
            'HDG': 'HDG',  # New Heading requested
            'WPY': 'WPY',  # New Waypoint requested
            'RES': 'RES',  # Response of the user in the matrix
            'FLT': 'FLT',  # Use of flightstick
            'MOV': 'MOV',  # Movement of trackball
            'VAS': 'VAS',  # Questionnaire done, in this case I will send VAS-000-0-0
            'SRT': 'SRT',  # Start, I will send SRT-000-0-0
            'STP': 'STP',  # Stop, I will send STP-000-0-0
            'PSE': 'PSE'  # Pause
        }
        # I consider a closed period after 100 ms from the last action on a device
        # TODO HDG channel streaming in real-time with LSL

        self.img_pos = {1: '007',
                        2: '008',
                        3: '009',
                        4: '004',
                        5: '005',
                        6: '006',
                        7: '001',
                        8: '002',
                        9: '003'}

        streamtitle = {'SRC': 'SRCStream',
                       'NAV': 'NAVStream'}

        self.size_slist = 9
        self.info = StreamInfo(streamtitle[type_m], 'Markers', self.size_slist, 0, 'string', 'myuidw43536')

        self.outlet = StreamOutlet(self.info)

    def send_mrk(self, typ, wht=None, A=None, B=None, it=None, end=True):

        if A is None:
            A = '00'
        if B is None:
            B = 0
        if it is None:
            it = '0000'
        if typ == 'SND':  # Force sending
            for _ in range(0, 9 - len(self.bsample)):
                self.bsample.append(' ')
            self.outlet.push_sample(self.bsample)
            self.bsample.clear()
            return

        # String wht handling here
        if isinstance(wht, int) and (typ == 'IMG' or typ == 'RES'):
            what = self.img_pos[wht]
        elif isinstance(wht, int) and typ == 'HDG':
            if wht in range(0, 10):
                what = f'00{wht}'
            elif wht in range(10, 100):
                what = f'0{wht}'
            else:
                what = str(wht)
        elif isinstance(wht, int) and (typ == 'SRT' or typ == 'STP'):  # Definition of which phase we start/stop
            if wht == 2:  # SRC TRAIN PHASE
                what = 'SRC'
            elif wht == 3:  # NAVI TRAIN PHASE
                what = 'NAV'
            elif wht == 4:  # OVERALL TRAINING
                what = 'OVR'
            elif wht == 1:  # MAIN EXPERIMENT
                what = 'MEX'
        elif isinstance(wht, bool) and typ == 'PSE':
            if wht is True:
                what = 'SRT'
            elif wht is False:
                what = 'STP'
        elif wht is not None:
            what = wht
        else:
            what = '000'

        # iteration treating
        if it in range(0, 10):
            iter = f'000{it}'
        elif it in range(10, 100):
            iter = f'00{it}'
        elif it in range(100, 1000):
            iter = f'0{it}'
        else:
            iter = str(it)

        sample = f'{self.type[typ]}-{iter}-{what}-{str(A)}-{str(B)}'
        self.bsample.append(sample)

        if end and len(self.bsample) == 3:  # Batch method to send more than one marker (ex. on IMG load)
            for _ in range(0, 6):
                self.bsample.append(' ')
            self.outlet.push_sample(self.bsample)
            self.bsample.clear()
        elif end and len(self.bsample) < 3:  # Placeholders to send anyway the packet
            for _ in range(0, 9 - len(self.bsample)):
                self.bsample.append(' ')
            self.outlet.push_sample(self.bsample)
            self.bsample.clear()
        else:
            return

    def close_mrk(self):
        self.outlet.push_sample(['CLS-0000-000-0-0', ' ', ' '])
        return
