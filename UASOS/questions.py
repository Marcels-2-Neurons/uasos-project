# questions.py>
# Library used to request the question forms to the test subject
# Imported in main as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import re
import sys

from PyQt5.QtWidgets import QWidget, QSlider, QRadioButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, \
    QPushButton, QStyleOptionSlider, QStyle, QButtonGroup, QApplication
from PyQt5.QtGui import QPainter, QPixmap, QIcon, QIntValidator, QFontMetrics, QFont
from PyQt5.QtCore import Qt, QPoint, QRect
from local import langue
from utilscsv import *
from settings import set

global ans


class answers():
    def __init__(self):
        self.f_done = 0
        self.err = None
        self.type = 'FULL'
        self.lang = 'fr'
        self.ID = None
        self.forms = [None, None, None, None, None, None, None]
        # Demographics data
        self.age = None
        self.gender = None
        self.degree = None
        self.work = None
        # EHI data
        self.total = None
        self.scorewriting = None
        self.scorethrowing = None
        self.scoretoothbrush = None
        self.scorespoon = None
        # KSS data
        self.KSS_data = None
        # SPS data
        self.SPS_data = None
        # RSME data
        self.RSME_data = None
        # VAS data
        self.VAS_cognitive = None
        self.VAS_drowsiness = None
        self.header = ['ID','lang','age','gender','degree','work','EHI_tot','scorewriting','scorethrowing',
                  'scoretoothbrush','scorespoon','KSS_data','SPS_data','RSME_data','VAS_cognitive','VAS_drowsiness']

class QVRadioButton(QRadioButton):
    def __init__(self, label, value):
        super().__init__(label)
        self.value = value


class QLSlider(QWidget):
    def __init__(self, minimum, maximum, interval=1, tickinterval=None, orientation=Qt.Horizontal,
                 labels=None, positions=None, parent=None, offset=None, style=None):
        super(QLSlider, self).__init__(parent=parent)
        # Levels is necessary if we don't pass custom labels
        levels = range(minimum, maximum + interval, interval)
        if labels is not None:
            if not isinstance(labels, (tuple, list)):
                raise Exception("<labels> is a list or tuple.")
            if len(labels) != len(positions):
                raise Exception("Size of <labels> doesn't match positions.")
            self.levels = list(zip(positions, labels))
        else:
            self.levels = list(zip(levels, map(str, levels)))

        if orientation == Qt.Horizontal:
            self.layout = QVBoxLayout(self)
            self.layout.setAlignment(Qt.AlignTop)
        elif orientation == Qt.Vertical:
            self.layout = QHBoxLayout(self)
            self.layout.setAlignment(Qt.AlignLeft)
        else:
            raise Exception("<orientation> wrong.")

        # gives some space to print labels
        self.left_margin = 10
        self.top_margin = 10
        self.right_margin = 10
        self.bottom_margin = 10
        # Offset of the labels
        if orientation == Qt.Horizontal:
            if offset is not None:
                if offset > 65:
                    self.offset = offset
            elif offset is None:
                self.offset = 65
            else:
                self.offset = 65
        else:
            if offset is not None:
                if offset > 60:
                    self.offset = offset
            elif offset is None:
                self.offset = 60
            else:
                self.offset = 60

        self.layout.setContentsMargins(self.left_margin, self.top_margin,
                                       self.right_margin, self.bottom_margin)

        self.sl = QSlider(orientation, self)
        if style is not None:
            self.style = style
            self.sl.setStyleSheet(self.style)
        else:
            self.style = None

        if tickinterval is not None:
            self.sl.setTickInterval(tickinterval)

        self.sl.setMinimum(minimum)
        self.sl.setMaximum(maximum)
        self.sl.setValue(minimum)

        if orientation == Qt.Horizontal:
            self.sl.setTickPosition(QSlider.TicksBelow)
            self.sl.setMinimumWidth(300)  # just to make it easier to read
        else:
            self.sl.setTickPosition(QSlider.TicksRight)
            self.sl.setMinimumHeight(300)  # just to make it easier to read

        self.sl.setSingleStep(1)

        self.layout.addWidget(self.sl)

    def paintEvent(self, e):
        super(QLSlider, self).paintEvent(e)

        style = self.sl.style()
        painter = QPainter(self)
        st_slider = QStyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation = self.sl.orientation()
        st_slider.dims = [self.geometry().width(), self.geometry().height()]
        if self.sl.orientation() == Qt.Horizontal:
            st_slider.ruler = self.sl.mapFromParent(QPoint(self.sl.rect().left(), self.sl.rect().bottom()))
            st_slider.rulxy = [-st_slider.ruler.x(), st_slider.ruler.y()]
        else:
            st_slider.ruler = self.sl.mapFromParent(QPoint(self.sl.rect().right(), self.sl.rect().bottom()))
            st_slider.rulxy = [-st_slider.ruler.x(), st_slider.ruler.y()]
        st_slider.offset = self.offset

        length = style.pixelMetric(QStyle.PM_SliderLength, st_slider, self.sl)
        available = style.pixelMetric(QStyle.PM_SliderSpaceAvailable, st_slider, self.sl)

        # Set font Style
        font = QFont()
        if self.style is not None:
            font = QFont()
            f_family = re.search(r'font-family: ([^;]+)', self.style).group(1)
            f_size = int(re.search(r'font-size: (\d+)', self.style).group(1))
            font.setFamily(f_family)
            font.setPixelSize(f_size)
            painter.setFont(font)
        else:
            font = QFont("Arial", 12)

        for v, v_str in self.levels:

            # get the size of the label
            rect = painter.drawText(QRect(), Qt.TextDontPrint, v_str)

            if self.sl.orientation() == Qt.Horizontal:
                # I assume the offset is half the length of slider, therefore
                # + length//2
                x_loc = QStyle.sliderPositionFromValue(self.sl.minimum(),
                                                       self.sl.maximum(), v, available) + length // 2

                # left bound of the text = center - half of text width + L_margin
                left = x_loc - rect.width() // 2 + self.left_margin
                bottom = - st_slider.rulxy[1] + self.offset

                # enlarge margins if clipping
                if v == self.sl.minimum():
                    if left <= 0:
                        self.left_margin = rect.width() // 2 - x_loc
                    if self.bottom_margin <= rect.height():
                        self.bottom_margin = rect.height()

                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

                if v == self.sl.maximum() and rect.width() // 2 >= self.right_margin:
                    self.right_margin = rect.width() // 2
                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

            else:
                y_loc = QStyle.sliderPositionFromValue(self.sl.minimum(),
                                                       self.sl.maximum(), v, available, upsideDown=True)

                bottom = y_loc + length // 2 + rect.height() // 2 + self.top_margin // 2 - 2
                # there is a 3 px offset that I can't attribute to any metric

                left = st_slider.rulxy[0] + st_slider.offset
                if left <= 0:
                    self.left_margin = rect.width() + 2
                    self.layout.setContentsMargins(self.left_margin,
                                                   self.top_margin, self.right_margin,
                                                   self.bottom_margin)

            pos = QPoint(left, bottom)
            painter.drawText(pos, v_str)
            # Calculate the width of the text box
            f_metrics = QFontMetrics(font)
            max_h = 0
            max_w = 0
            if self.sl.orientation() == Qt.Horizontal:
                t_box = f_metrics.boundingRect(v_str).height()
                t_height = t_box + 20
                if (st_slider.dims[1] + t_height) > self.height():
                    self.resize(self.width(), st_slider.dims[1] + t_height)
                else:
                    pass
            else:
                t_box = f_metrics.boundingRect(v_str).width()
                t_width = t_box + 20
                if (st_slider.dims[0] + t_width) > self.width():
                    self.resize(st_slider.dims[0] + t_width, self.height())
                else:
                    pass

        return


class QLang(QWidget):
    # TODO: Add Icon
    def __init__(self):
        super().__init__()

        font = "Calibri"
        Ttype = "bold"
        Tsize: int = 18
        tsize: int = 14
        self.titleconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {Tsize}px"
        self.textconfig = f"font-family: {font}; font-size: {tsize}px"

        if 'ans' in locals() or 'ans' in globals():
            pass
        else:
            ans = answers()

        self.setWindowTitle("Select Language")
        self.setWindowIcon(QIcon("./props/isae_logo.png"))
        self.title = QLabel("ISAE CNE - Bienvenue")
        self.title.setStyleSheet(self.titleconfig)
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setFixedSize(335, 201)
        # Country Flags for the languages
        self.ID_label = QLabel(langue.get_string("ID_request"))
        self.ID_label.setStyleSheet(self.textconfig)
        self.ID_box = QLineEdit()
        self.IDval = QIntValidator()
        self.ID_box.setValidator(self.IDval)
        self.ID_box.setFixedSize(100, 25)
        self.ID_box.setStyleSheet(self.textconfig)
        self.box = QHBoxLayout()
        self.box.addWidget(self.ID_label)
        self.box.addWidget(self.ID_box)
        self.wbox = QWidget()
        self.wbox.setLayout(self.box)

        self.fr_FR = QIcon(QPixmap("./props/fr_FR.png"))
        self.en_US = QIcon(QPixmap("./props/en_US.png"))
        self.it_IT = QIcon(QPixmap("./props/it_IT.png"))
        # Create the labels with icons
        self.lbl_fr = QLabel()
        self.lbl_fr.setPixmap(self.fr_FR.pixmap(100, 100))
        self.lbl_fr.mousePressEvent = self.on_fr_FR_click

        self.lbl_en = QLabel()
        self.lbl_en.setPixmap(self.en_US.pixmap(100, 100))
        self.lbl_en.mousePressEvent = self.on_en_US_click

        self.lbl_it = QLabel()
        self.lbl_it.setPixmap(self.it_IT.pixmap(100, 100))
        self.lbl_it.mousePressEvent = self.on_it_IT_click

        # Create a vertical layout
        flay = QHBoxLayout()
        flay.addWidget(self.lbl_fr)
        flay.addWidget(self.lbl_en)
        flay.addWidget(self.lbl_it)
        wflay = QWidget()
        wflay.setLayout(flay)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.wbox)
        layout.addWidget(wflay)

        self.setLayout(layout)

    def on_fr_FR_click(self, event):
        if not self.ID_box.text():
            pass
        else:
            ans.lang = 'fr'
            ans.ID = int(self.ID_box.text())
            langue.set_language(ans.lang)
            ans.f_done = 1
            self.hide()


    def on_en_US_click(self, event):
        if not self.ID_box.text():
            pass
        else:
            ans.lang = 'en'
            ans.ID = int(self.ID_box.text())
            langue.set_language(ans.lang)
            ans.f_done = 1
            self.hide()


    def on_it_IT_click(self, event):
        if not self.ID_box.text():
            pass
        else:
            ans.lang = 'it'
            ans.ID = int(self.ID_box.text())
            langue.set_language(ans.lang)
            ans.done = 1
            self.hide()

    def closeEvent(self, e):
        ans.err = 0
        e.accept()


class QDemo(QWidget):
    # TODO: Add Icon
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Demographics Form")
        self.setWindowIcon(QIcon("./props/isae_logo.png"))
        if ans.lang == 'en' or ans.lang == 'fr':
            self.setFixedSize(600, 600)
            self.space = 180
        elif ans.lang == 'it':
            self.setFixedSize(500, 600)
            self.space = 130

        font = "Calibri"
        Ttype = "bold"
        Tsize: int = 18
        tsize: int = 14
        self.titleconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {Tsize}px"
        self.textconfig = f"font-family: {font}; font-size: {tsize}px"

        self.gencheck = []
        self.degcheck = []
        self.workcheck = []
        self.layout = QVBoxLayout()

        self.title = QLabel(langue.get_string("demo_Title"))
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setStyleSheet(self.titleconfig)
        self.layout.addWidget(self.title)

        qDemos = [langue.get_string("demo_AGE"), langue.get_string("demo_gender"),
                  langue.get_string("demo_degree"), langue.get_string("demo_work")]

        qbut = langue.get_string("OK")

        q_gender = [langue.get_string("Male"), langue.get_string("Female"), langue.get_string("Undefined")]

        q_degree = [langue.get_string("HighSchool"), langue.get_string("Apprenticeship"),
                    langue.get_string("Bachelors"),
                    langue.get_string("Masters"), langue.get_string("PhD")]

        q_work = [langue.get_string("Student"), langue.get_string("Employed"), langue.get_string("Unemployed"),
                  langue.get_string("Other")]

        list = [QVBoxLayout() for _ in range(3)]
        wlist = [QWidget() for _ in range(3)]
        box = [QHBoxLayout() for _ in range(4)]
        wbox = [QWidget() for _ in range(4)]

        for idx, ltext in enumerate(qDemos):
            label = QLabel(ltext)
            label.setStyleSheet(self.textconfig)
            # label.resize(label.sizeHint())
            label.setAlignment(Qt.AlignLeft)
            box[idx].addWidget(label)

            if idx == 0:
                box[idx].setContentsMargins(9, 10, self.space, 10)
                self.age_field = QLineEdit()
                self.aval = QIntValidator()
                self.age_field.setValidator(self.aval)
                self.age_field.setFixedSize(100, 20)
                self.age_field.textChanged.connect(self.checkInput)
                self.age_field.setStyleSheet(self.textconfig)
                box[idx].addWidget(self.age_field)
            elif idx == 1:
                for lgen in q_gender:
                    optg = QVRadioButton(lgen, lgen)
                    optg.setStyleSheet(self.textconfig)
                    optg.toggled.connect(self.checkInput)
                    self.gencheck.append(optg)
                    list[idx - 1].addWidget(optg)
            elif idx == 2:
                for ldegree in q_degree:
                    optd = QVRadioButton(ldegree, ldegree)
                    optd.setStyleSheet(self.textconfig)
                    optd.toggled.connect(self.checkInput)
                    self.degcheck.append(optd)
                    list[idx - 1].addWidget(optd)
            elif idx == 3:
                for lwork in q_work:
                    optw = QVRadioButton(lwork, lwork)
                    optw.setStyleSheet(self.textconfig)
                    optw.toggled.connect(self.checkInput)
                    self.workcheck.append(optw)
                    list[idx - 1].addWidget(optw)

            wlist[idx - 1].setLayout(list[idx - 1])
            box[idx].addWidget(wlist[idx - 1])
            wbox[idx].setLayout(box[idx])
            self.layout.addWidget(wbox[idx])

        self.qOK = QPushButton(qbut)
        self.qOK.setEnabled(False)
        self.qOK.mousePressEvent = self.on_OK_click
        self.butlay = QHBoxLayout()
        self.wbutlay = QWidget()
        self.qOK.setFixedSize(100, 25)
        self.qOK.setStyleSheet(self.textconfig)
        self.butlay.addStretch(300)
        self.butlay.addWidget(self.qOK)
        self.wbutlay.setLayout(self.butlay)
        self.layout.addWidget(self.wbutlay)
        self.setLayout(self.layout)

    def checkInput(self):
        isAgeFilled = bool(self.age_field.text())
        g = False
        d = False
        w = False
        for opt in self.gencheck:
            if opt.isChecked():
                g = True
        for opt in self.degcheck:
            if opt.isChecked():
                d = True
        for opt in self.workcheck:
            if opt.isChecked():
                w = True

        self.qOK.setEnabled(isAgeFilled and g and d and w)

    def on_OK_click(self, event):
        ans.age = int(self.age_field.text())
        for opt in self.gencheck:
            if opt.isChecked():
                ans.gender = opt.value
                break
        for opt in self.degcheck:
            if opt.isChecked():
                ans.degree = opt.value
                break
        for opt in self.workcheck:
            if opt.isChecked():
                ans.work = opt.value
                break
        ans.f_done = 2
        self.hide()

    def closeEvent(self, e):
        ans.err = 0
        e.accept()


class QEHI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EHI Form")
        self.setWindowIcon(QIcon("./props/isae_logo.png"))
        if ans.lang == 'it' or ans.lang == 'fr':
            self.setFixedSize(800, 320)
        elif ans.lang == 'en':
            self.setFixedSize(750, 320)

        # Font Selection
        font = "Calibri"
        Ttype = "bold"
        Tsize: int = 18
        tsize: int = 14
        self.titleconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {Tsize}px"
        self.textconfig = f"font-family: {font}; font-size: {tsize}px"
        # Layout
        self.layout = QVBoxLayout()
        # Set Title
        self.title = QLabel(langue.get_string("EHI_Title"))
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setStyleSheet(self.titleconfig)
        self.layout.addWidget(self.title)
        # Set question
        self.quest = QLabel(langue.get_string("EHI_question"))
        self.quest.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.quest.setStyleSheet(self.textconfig)
        self.layout.addWidget(self.quest)
        # Set Column labels
        self.bigbox = QHBoxLayout()
        self.wbigbox = QWidget()
        self.ylabsBox = [QVBoxLayout() for _ in range(6)]
        self.wylabsBox = [QWidget() for _ in range(6)]
        clabels = [langue.get_string(f"EHI_c{5 - (i)}") for i in range(5)]
        rlabels = [langue.get_string(f"EHI_r{i + 1}") for i in range(4)]
        qbut = langue.get_string("OK")
        self.qracks = [QButtonGroup(), QButtonGroup(), QButtonGroup(), QButtonGroup()]
        # Column Labels on 0 - Hands
        for idx in range(5):
            if idx == 0:
                self.ylabsBox[0].addSpacing(30)
            else:
                label = QLabel(rlabels[idx - 1])
                label.setStyleSheet(self.textconfig)
                self.ylabsBox[0].addWidget(label)
                # self.ylabsBox[0].addSpacing(10)
        # Each question now
        for cidx in range(5):
            for pos in range(5):
                if pos == 0:
                    label = QLabel(clabels[cidx])
                    label.setStyleSheet(self.textconfig)
                    self.ylabsBox[cidx + 1].addWidget(label, alignment=Qt.AlignCenter)
                    self.ylabsBox[cidx + 1].addSpacing(20)
                else:
                    opt = QVRadioButton("", 5 - cidx)
                    opt.setProperty("Value", 5-cidx)
                    opt.toggled.connect(self.checkInput)
                    self.qracks[pos-1].addButton(opt)
                    self.ylabsBox[cidx + 1].addWidget(opt, alignment=Qt.AlignCenter)
                    self.ylabsBox[cidx + 1].addSpacing(10)
        # Put in the Widget Containers
        for i in range(6):
            self.wylabsBox[i].setLayout(self.ylabsBox[i])
            self.bigbox.addWidget(self.wylabsBox[i])
        self.wbigbox.setLayout(self.bigbox)
        self.layout.addWidget(self.wbigbox)

        self.qOK = QPushButton(qbut)
        self.qOK.setEnabled(False)
        self.qOK.mousePressEvent = self.on_OK_click
        self.butlay = QHBoxLayout()
        self.wbutlay = QWidget()
        self.qOK.setFixedSize(100, 25)
        self.qOK.setStyleSheet(self.textconfig)
        self.butlay.addStretch(300)
        self.butlay.addWidget(self.qOK)
        self.wbutlay.setLayout(self.butlay)
        self.layout.addWidget(self.wbutlay)
        self.setLayout(self.layout)

    def checkInput(self):
        q = [False, False, False, False]
        for i in range(4):  # columns
            if self.qracks[i].checkedButton() is not None:
                q[i] = True

        self.qOK.setEnabled(all(q))

    def on_OK_click(self, event):
        ans.scorewriting = self.qracks[0].checkedButton().property("Value")
        ans.scorethrowing = self.qracks[1].checkedButton().property("Value")
        ans.scoretoothbrush = self.qracks[2].checkedButton().property("Value")
        ans.scorespoon = self.qracks[3].checkedButton().property("Value")

        ans.total = ans.scorewriting+ans.scorethrowing+ans.scoretoothbrush+ans.scorespoon
        ans.f_done = 3
        self.hide()

    def closeEvent(self, e):
        ans.err = 0
        e.accept()


class QKSS(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("KSS Form")
        self.setWindowIcon(QIcon("./props/isae_logo.png"))
        if ans.lang == 'fr':
            self.setFixedSize(580, 400)
        if ans.lang == 'it':
            self.setFixedSize(530, 400)
        elif ans.lang == 'en':
            self.setFixedSize(480, 400)

        font = "Calibri"
        Ttype = "bold"
        Tsize: int = 18
        tsize: int = 14
        self.titleconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {Tsize}px"
        self.textconfig = f"font-family: {font}; font-size: {tsize}px"

        self.layout = QVBoxLayout()
        # Set Title
        self.title = QLabel(langue.get_string("KSS_Title"))
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setStyleSheet(self.titleconfig)
        self.layout.addWidget(self.title)
        # Set question
        self.quest = QLabel(langue.get_string("KSS_question"))
        self.quest.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.quest.setStyleSheet(self.textconfig)
        self.layout.addWidget(self.quest)

        self.nqst = QVBoxLayout()
        self.qst = QVBoxLayout()
        self.opts = []
        self.wnqst = QWidget()
        self.wqst = QWidget()
        self.bigbox = QHBoxLayout()
        self.wbigbox = QWidget()

        for idx in range(9):
            lbl = QLabel(f"{idx+1}")
            lbl.setStyleSheet(self.textconfig)
            self.nqst.addWidget(lbl)
            opt = QVRadioButton(langue.get_string(f"KSS_{idx+1}"),idx+1)
            opt.setStyleSheet(self.textconfig)
            opt.toggled.connect(self.checkInput)
            self.opts.append(opt)
            self.qst.addWidget(opt, alignment=Qt.AlignLeft)
        self.wnqst.setLayout(self.nqst)
        self.wqst.setLayout(self.qst)

        self.bigbox.addWidget(self.wnqst)
        self.bigbox.addWidget(self.wqst)
        self.wbigbox.setLayout(self.bigbox)

        self.layout.addWidget(self.wbigbox)

        qbut = langue.get_string("OK")
        self.qOK = QPushButton(qbut)
        self.qOK.setEnabled(False)
        self.qOK.mousePressEvent = self.on_OK_click
        self.butlay = QHBoxLayout()
        self.wbutlay = QWidget()
        self.qOK.setFixedSize(100, 25)
        self.qOK.setStyleSheet(self.textconfig)
        self.butlay.addStretch(300)
        self.butlay.addWidget(self.qOK)
        self.wbutlay.setLayout(self.butlay)
        self.layout.addWidget(self.wbutlay)
        self.setLayout(self.layout)

    def checkInput(self):
        check = False
        for idx in range(9):
            if self.opts[idx].isChecked():
                check = True
                break

        self.qOK.setEnabled(check)

    def on_OK_click(self, event):
        for idx in range(9):
            if self.opts[idx].isChecked():
                ans.KSS_data = self.opts[idx].value
                break
        ans.f_done = 4
        self.hide()


class QSPS(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SPS Form")
        self.setWindowIcon(QIcon("./props/isae_logo.png"))
        if ans.lang == 'fr':
            self.setFixedSize(410, 300)
        if ans.lang == 'it':
            self.setFixedSize(430, 300)
        elif ans.lang == 'en':
            self.setFixedSize(470, 300)

        font = "Calibri"
        Ttype = "bold"
        Tsize: int = 18
        tsize: int = 14
        self.titleconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {Tsize}px"
        self.textconfig = f"font-family: {font}; font-size: {tsize}px"

        self.layout = QVBoxLayout()
        # Set Title
        self.title = QLabel(langue.get_string("SPS_Title"))
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setStyleSheet(self.titleconfig)
        self.layout.addWidget(self.title)
        # Set question
        self.quest = QLabel(langue.get_string("SPS_question"))
        self.quest.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.quest.setStyleSheet(self.textconfig)
        self.layout.addWidget(self.quest)

        self.nqst = QVBoxLayout()
        self.qst = QVBoxLayout()
        self.opts = []
        self.wnqst = QWidget()
        self.wqst = QWidget()
        self.bigbox = QHBoxLayout()
        self.wbigbox = QWidget()

        for idx in range(7):
            lbl = QLabel(f"{idx+1}")
            lbl.setStyleSheet(self.textconfig)
            self.nqst.addWidget(lbl)
            opt = QVRadioButton(langue.get_string(f"SPS_{idx+1}"), idx+1)
            opt.setStyleSheet(self.textconfig)
            opt.toggled.connect(self.checkInput)
            self.opts.append(opt)
            self.qst.addWidget(opt, alignment=Qt.AlignLeft)
        self.wnqst.setLayout(self.nqst)
        self.wqst.setLayout(self.qst)

        self.bigbox.addWidget(self.wnqst)
        self.bigbox.addWidget(self.wqst)
        self.wbigbox.setLayout(self.bigbox)

        self.layout.addWidget(self.wbigbox)

        qbut = langue.get_string("OK")
        self.qOK = QPushButton(qbut)
        self.qOK.setEnabled(False)
        self.qOK.mousePressEvent = self.on_OK_click
        self.butlay = QHBoxLayout()
        self.wbutlay = QWidget()
        self.qOK.setFixedSize(100, 25)
        self.qOK.setStyleSheet(self.textconfig)
        self.butlay.addStretch(300)
        self.butlay.addWidget(self.qOK)
        self.wbutlay.setLayout(self.butlay)
        self.layout.addWidget(self.wbutlay)
        self.setLayout(self.layout)

    def checkInput(self):
        check = False
        for idx in range(7):
            if self.opts[idx].isChecked():
                check = True
                break

        self.qOK.setEnabled(check)

    def on_OK_click(self, event):
        for idx in range(7):
            if self.opts[idx].isChecked():
                ans.SPS_data = self.opts[idx].value
                break
        ans.f_done = 5
        self.hide()

    def closeEvent(self, e):
        ans.err = 0
        e.accept()

class QRSME(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RSME Form")
        self.setWindowIcon(QIcon("./props/isae_logo.png"))
        # if ans.lang == 'fr':
        #     self.setFixedSize(410, 600)
        # if ans.lang == 'it':
        #     self.setFixedSize(430, 600)
        # elif ans.lang == 'en':
        #     self.setFixedSize(430, 600)

        font = "Calibri"
        Ttype = "bold"
        Tsize: int = 18
        tsize: int = 14
        self.titleconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {Tsize}px"
        self.textconfig = f"font-family: {font}; font-size: {tsize}px"

        self.layout = QHBoxLayout()
        # Set Title
        self.title = QLabel(langue.get_string("RSME_Title"))
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setStyleSheet(self.titleconfig)
        # Set question
        self.quest = QLabel(langue.get_string("RSME_question"))
        self.quest.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.quest.setStyleSheet(self.textconfig)

        self.Rbox = QVBoxLayout()
        self.wbox = QWidget()

        # Define slider
        pos_labels = [2, 13, 25, 37, 57, 71, 85, 102, 112]
        labels = ["- "+langue.get_string(f"RSME_l{k + 1}") for k in range(9)]
        self.slider = QLSlider(0, 150, 1, labels=labels, positions=pos_labels, orientation=Qt.Vertical, tickinterval=10, style=self.textconfig)
        self.slider.sl.valueChanged.connect(self.checkInput)
        self.slbox = QHBoxLayout()
        self.slbox.addWidget(self.slider)
        self.wslbox = QWidget()
        self.wslbox.setFixedSize(self.slider.width()-350, self.slider.height())
        self.wslbox.setLayout(self.slbox)
        self.layout.addWidget(self.wslbox)

        self.Rbox.addWidget(self.title)
        self.Rbox.addWidget(self.quest)

        qbut = langue.get_string("OK")
        self.qOK = QPushButton(qbut)
        self.qOK.setEnabled(False)
        self.qOK.mousePressEvent = self.on_OK_click
        self.qOK.setFixedSize(100, 25)
        self.qOK.setStyleSheet(self.textconfig)
        self.Rbox.addWidget(self.qOK)
        self.wbox.setLayout(self.Rbox)
        self.layout.addWidget(self.wbox)
        self.setLayout(self.layout)

    def checkInput(self):
        self.qOK.setEnabled(True)

    def on_OK_click(self, event):
        ans.RSME_data = self.slider.sl.value()
        ans.f_done = 6
        self.hide()

    def closeEvent(self, e):
        ans.err = 0
        e.accept()


class QVAS(QWidget):
    def __init__(self):
        super().__init__()
        self.checks = [False, False] # Check Purpose

        self.setWindowTitle("VAS Form")
        self.setWindowIcon(QIcon("./props/isae_logo.png"))
        # if ans.lang == 'fr':
        #     self.setFixedSize(410, 600)
        # if ans.lang == 'it':
        #     self.setFixedSize(430, 600)
        # elif ans.lang == 'en':
        #     self.setFixedSize(430, 600)

        font = "Calibri"
        Ttype = "bold"
        htype = "italic"
        Tsize: int = 18
        tsize: int = 14
        self.titleconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {Tsize}px"
        self.qconfig = f"font-family: {font}; font-weight: {Ttype}; font-size: {tsize}px"
        self.hintsconfig = f"font-family: {font}; font-style: {htype}; font-size: {tsize}px"
        self.textconfig = f"font-family: {font}; font-size: {tsize}px"

        self.layout = QVBoxLayout()
        # Set Title
        self.title = QLabel(langue.get_string("VAS_Title"))
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title.setStyleSheet(self.titleconfig)
        # Set question
        self.quest = QLabel(langue.get_string("VAS_question"))
        self.quest.setAlignment(Qt.AlignTop)
        self.quest.setStyleSheet(self.qconfig)
        # Set hints
        self.hint1 = QLabel(langue.get_string("VAS_hint1"))
        self.hint2 = QLabel(langue.get_string("VAS_hint2"))
        self.hint1.setAlignment(Qt.AlignTop)
        self.hint2.setAlignment(Qt.AlignTop)
        self.hint1.setStyleSheet(self.hintsconfig)
        self.hint2.setStyleSheet(self.hintsconfig)

        # Set slider titles
        self.sltitle1 = QLabel(langue.get_string("VAS_hl1"))
        self.sltitle2 = QLabel(langue.get_string("VAS_hl2"))
        self.sltitle1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.sltitle2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.sltitle1.setStyleSheet(self.textconfig)
        self.sltitle2.setStyleSheet(self.textconfig)

        # Set Sliders
        labels = [langue.get_string("VAS_low"), langue.get_string("VAS_high")]
        pos_labels = [0, 100]
        self.slid1 = QLSlider(0, 100, 1, labels=labels, positions=pos_labels, orientation=Qt.Horizontal,
                              tickinterval=100, style=self.textconfig)
        self.slid2 = QLSlider(0, 100, 1, labels=labels, positions=pos_labels, orientation=Qt.Horizontal,
                              tickinterval=100, style=self.textconfig)
        self.slid1.sl.valueChanged.connect(lambda: self.checkInput(0))
        self.slid2.sl.valueChanged.connect(lambda: self.checkInput(1))

        # Set OK button
        qbut = langue.get_string("OK")
        self.qOK = QPushButton(qbut)
        self.qOK.setEnabled(False)
        self.qOK.clicked.connect(self.on_OK_click)
        self.qOK.setFixedSize(100, 25)
        self.qOK.setStyleSheet(self.textconfig)

        # Add everything
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.quest)
        self.layout.addWidget(self.hint1)
        self.layout.addWidget(self.hint2)
        self.layout.addWidget(self.sltitle1)
        self.layout.addWidget(self.slid1)
        self.layout.addWidget(self.sltitle2)
        self.layout.addWidget(self.slid2)
        self.layout.addWidget(self.qOK)
        self.setLayout(self.layout)

    def checkInput(self, slide):
        if slide in [0, 1]:
            self.checks[slide] = True
        self.qOK.setEnabled(all(self.checks))

    def on_OK_click(self):
        ans.VAS_cognitive = self.slid1.sl.value()
        ans.VAS_drowsiness = self.slid2.sl.value()
        ans.f_done = 7
        self.hide()

    def closeEvent(self, e):
        ans.err = 0
        e.accept()


def subject_fullform():
    app = QApplication(sys.argv)
    while ans.f_done != 8 and ans.err is None:
        if ans.f_done == 0 and ans.forms[0] is None:
            ans.forms[0] = QLang()
            ans.forms[0].show()
        elif ans.f_done == 1 and ans.forms[1] is None:
            ans.forms[1] = QDemo()
            ans.forms[1].show()
        elif ans.f_done == 2 and ans.forms[2] is None:
            ans.forms[2] = QEHI()
            ans.forms[2].show()
        elif ans.f_done == 3 and ans.forms[3] is None:
            ans.forms[3] = QKSS()
            ans.forms[3].show()
        elif ans.f_done == 4 and ans.forms[4] is None:
            ans.forms[4] = QSPS()
            ans.forms[4].show()
        elif ans.f_done == 5 and ans.forms[5] is None:
            ans.forms[5] = QRSME()
            ans.forms[5].show()
        elif ans.f_done == 6 and ans.forms[6] is None:
            ans.forms[6] = QVAS()
            ans.forms[6].show()
        elif ans.f_done == 7:
            writeform(ans)
            ans.f_done = 8
            app.quit()
        app.processEvents()

    if ans.err is not None:
        # I close everything
        set.close = True



ans = answers()
