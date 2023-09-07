# lslmarkers.py>
# Library used for LSL Markers stream
# Imported in SRCevents and NAVevents as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import pylsl
from pylsl import StreamInfo, StreamOutlet


class lslmarkers:
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
            'UDG': 'UDG',  # User choice on Heading
            'WPY': 'WPY',  # New Waypoint requested
            'UPY': 'UPY',  # User choice on Waypoint
            'RES': 'RES',  # Response of the user in the matrix
            'FLT': 'FLT',  # Use of flightstick
            'MOV': 'MOV',  # Movement of trackball
            'VAS': 'VAS',  # Questionnaire done, in this case I will send VAS-000-0-0
            'SRT': 'SRT',  # Start, I will send SRT-000-0-0
            'BRK': 'BRK',  # Break, when press esc button - BRK-000-0-0
            'CLS': 'CLS',  # Close, at end of experiment
            'RST': 'RST',  # Reset, I will send RST-000-0-0
            'STP': 'STP',  # Stop, I will send STP-000-0-0
            'PSE': 'PSE'  # Pause
        }
        # I consider a closed period after 100 ms from the last action on a device

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

        self.size_slist = 12
        pylsl.local_clock()
        if type_m == 'SRC':
            self.info = StreamInfo(streamtitle[type_m], 'Markers', self.size_slist, pylsl.IRREGULAR_RATE, 'string', 'uasossrcmrks')
        if type_m == 'NAV':
            self.info = StreamInfo(streamtitle[type_m], 'Markers', self.size_slist,  pylsl.IRREGULAR_RATE, 'string', 'uasosnavmrks')

        self.outlet = StreamOutlet(self.info)

    def send_mrk(self, typ, wht=None, A=None, B=None, it=None, cut_seconds=None, end=True):
        # TODO CONTINUE FOR WPY, FLT, MOV, UPY, UDG
        if A is None:
            A = '00'
        if B is None:
            B = 0
        if it is None:
            it = '0000'
        if typ == 'SND':  # Force sending
            for _ in range(0, self.size_slist - len(self.bsample)):
                self.bsample.append(' ')
            if cut_seconds is None:
                self.outlet.push_sample(self.bsample, pylsl.local_clock())
            else:
                self.outlet.push_sample(self.bsample, pylsl.local_clock() - cut_seconds)  # minus the seconds of cut_seconds[s]
            self.bsample.clear()
            return

        # String wht handling here
        if isinstance(wht, int) and (typ == 'IMG' or typ == 'RES'):
            what = self.img_pos[wht]
        elif isinstance(wht, int) and (typ == 'HDG' or typ == 'UDG'):
            if wht in range(0, 10):
                what = f'00{wht}'
            elif wht in range(10, 100):
                what = f'0{wht}'
            else:
                what = str(wht)
        elif typ == 'WPY' or typ == 'UPY':
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
        elif isinstance(wht, bool) and (typ == 'PSE' or typ == 'VAS' or typ == 'FLT' or typ == 'MOV'):
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
            if cut_seconds is None:
                self.outlet.push_sample(self.bsample, pylsl.local_clock())
            else:
                self.outlet.push_sample(self.bsample, pylsl.local_clock()-cut_seconds)  # minus the seconds of cut_seconds[s]
            self.bsample.clear()
        elif end and len(self.bsample) < 3:  # Placeholders to send anyway the packet
            for _ in range(0, self.size_slist - len(self.bsample)):
                self.bsample.append(' ')
            if cut_seconds is None:
                self.outlet.push_sample(self.bsample, timestamp=pylsl.local_clock())
            else:
                self.outlet.push_sample(self.bsample, timestamp=pylsl.local_clock() - cut_seconds)  # minus the seconds of cut_seconds[s]
            self.bsample.clear()
        else:
            return

    def close_mrk(self):
        self.outlet.push_sample(['CLS-0000-000-0-0', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], timestamp=pylsl.local_clock())
        return


class lslchannel:
    def __init__(self, name=None, channel_names=None, channel_units=None):
        # Define Stream Info
        self.ch = []
        self.stream_name = name
        self.stream_type = "StreamData"
        if channel_names is not None and channel_units is not None:
            self.channel_count = len(channel_names)
        self.sampling_rate = 0  # Not fixed
        self.channel_format = 'float32'

        # Create Stream Info
        info = StreamInfo(name=self.stream_name,type=self.stream_type,channel_count=self.channel_count,nominal_srate=0,channel_format=self.channel_format)

        # Add channel Info
        if channel_names is not None and channel_units is not None:
            for i in range(0, len(channel_names)):
                self.ch.append(info.desc().append_child('channels').append_child('channel'))
                self.ch[i].append_child_value('label', channel_names[i])
                self.ch[i].append_child_value('unit', channel_units[i])
                self.ch[i].append_child_value('type', self.channel_format)

        # Create Stream Outlet
        self.outlet = StreamOutlet(info)

    def push_it(self, vals=None):
        if vals is not None and len(vals) == self.channel_count:
            self.outlet.push_sample(vals)
            return
        else:
            print(f'Error, no. of values incorrect. No. values: {len(vals)} / No. channels: {self.channel_count}')
            return

