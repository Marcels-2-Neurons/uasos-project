# flightdir.py>
# Library used for Flight Director drawing and execution
# Imported in events as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################
import os
from typing import Tuple
from psychopy import visual
from settings import *


class Colors:
    green: Tuple[int, int, int] = [0, 255, 0]
    dgreen: Tuple[int, int, int] = [15, 88, 10]  # Hex: 0F580A
    black: Tuple[int, int, int] = [0, 0, 0]
    red: Tuple[int, int, int] = [255, 0, 0]
    white: Tuple[int, int, int] = [255, 255, 255]
    # From Vintage PC Color Palettes
    lgray: Tuple[int, int, int] = [190, 190, 190]  # Hex: BEBEBE
    gray: Tuple[int, int, int] = [146, 147, 147]  # Hex: 929393
    dgray: Tuple[int, int, int] = [55, 55, 56]  # Hex: 373738


class flightdir:
    def __init__(self, win=None, type_m=None, x=0, y=0, width=0, height=0):
        from local import langue
        from settings import set
        self.type = type_m
        self.win = win
        self.correct_lang = False
        self.border = visual.Rect(win, pos=(x, y),
                                  size=(width, height),
                                  fillColor=Colors.lgray,
                                  opacity=1.0,
                                  colorSpace='rgb255')
        self.face = visual.Rect(win, pos=(x, y),
                                size=(width, height),
                                fillColor=Colors.gray,
                                opacity=1.0,
                                colorSpace='rgb255')
        self.screen = visual.Rect(win, pos=(x, y),
                                  size=(width, height),
                                  fillColor=Colors.dgray,
                                  opacity=1.0,
                                  colorSpace='rgb255')
        self.led = visual.Circle(win, pos=(x, y),
                                 size=(width, height),
                                 fillColor=Colors.dgreen,
                                 opacity=1.0,
                                 colorSpace='rgb255')
        if self.type == 'SRC':
            title_str = langue.get_string('SEARCH')
            item_str = langue.get_string('NONE')
        elif self.type == 'NAV':
            title_str = langue.get_string('NAVIGATE')
            item_str = langue.get_string('NONE')

        hold_str = langue.get_string('HOLD')
        self.forms_str = langue.get_string('FORM')  # For now I put the forms string as self
        self.noscreen_str = langue.get_string('NOT_ACTIVE')
        ty_str = langue.get_string('THANK_YOU')
        pause_str = langue.get_string('PAUSE')
        self.slide_path = ".\\tutorial"
        self.s_final_pth = None
        self.slide_loc = None

        self.text_src = visual.TextStim(win=win, name='text_src',
                                        text=title_str,
                                        font='Arial',
                                        pos=(x, y), height=0.1, wrapWidth=None, ori=0.0,
                                        color=Colors.white, colorSpace='rgb255', bold=True,
                                        languageStyle='LTR',
                                        depth=0.0)

        self.text_item = visual.TextStim(win=win, name='text_item',
                                         text=item_str,
                                         font='Arial',
                                         pos=(x, y), height=0.07, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)

        self.hold_text = visual.TextStim(win=win, name='hold_txt',
                                         text=hold_str,
                                         font='Arial',
                                         pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)
        self.form_txt = visual.TextStim(win=win, name='form_txt',
                                         text=self.forms_str,
                                         font='Arial',
                                         pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)
        self.noscreen_txt = visual.TextStim(win=win, name='noscreen_txt',
                                        text=self.noscreen_str,
                                        font='Arial',
                                        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                        color=Colors.white, colorSpace='rgb255', bold=True,
                                        languageStyle='LTR',
                                        depth=0.0)
        self.thank_you = visual.TextStim(win=win, name='thank_you',
                                         text=ty_str,
                                         font='Arial',
                                         pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)
        self.pause_txt = visual.TextStim(win=win, name='pause',
                                         text=pause_str,
                                         font='Arial',
                                         pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)
        self.vas_txt = visual.TextStim(win=win, name='vas',
                                         text=langue.get_string('VAS_REQUEST'),
                                         font='Arial',
                                         pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)
        self.end_txt = visual.TextStim(win=win, name='end',
                                         text=langue.get_string('END_OF_PHASE'),
                                         font='Arial',
                                         pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)
        self.hdg_devt = visual.TextStim(win=win, name='hdg_devt',
                                     text=langue.get_string('HDG_DEV'),
                                     font='Arial',
                                     pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                     color=Colors.white, colorSpace='rgb255', bold=True,
                                     languageStyle='LTR',
                                     depth=0.0)  # CHANGE THE LOCATION!
        self.hdg_devv = visual.TextStim(win=win, name='hdg_devv',
                                     text='0°',
                                     font='Arial',
                                     pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                     color=Colors.white, colorSpace='rgb255', bold=False,
                                     languageStyle='LTR',
                                     depth=0.0)  # CHANGE THE LOCATION!
        self.com_eval = visual.TextStim(win=win, name='com_eval',
                                     text=langue.get_string('N/A'),
                                     font='Arial',
                                     pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                     color=Colors.white, colorSpace='rgb255', bold=True,
                                     languageStyle='LTR',
                                     depth=0.0)  # CHANGE THE LOCATION!
        self.RT_txt = visual.TextStim(win=win, name='RTt',
                                     text='RT',
                                     font='Arial',
                                     pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                     color=Colors.white, colorSpace='rgb255', bold=True,
                                     languageStyle='LTR',
                                     depth=0.0)  # CHANGE THE LOCATION!
        self.RT_val = visual.TextStim(win=win, name='RTv',
                                      text='0.000 ms',
                                      font='Arial',
                                      pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                      color=Colors.white, colorSpace='rgb255', bold=False,
                                      languageStyle='LTR',
                                      depth=0.0)  # CHANGE THE LOCATION!
        self.TGT_txt = visual.TextStim(win=win, name='TGTt',
                                       text=langue.get_string('TARGETS'),
                                       font='Arial',
                                       pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0,
                                       color=Colors.white, colorSpace='rgb255', bold=True,
                                       languageStyle='LTR',
                                       depth=0.0)  # CHANGE THE LOCATION!
        self.Good_tgtt = visual.TextStim(win=win, name='GTgtt',
                                         text=langue.get_string('DETECTED'),
                                         font='Arial',
                                         pos=(0, 0), height=0.09, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=True,
                                         languageStyle='LTR',
                                         depth=0.0)  # CHANGE THE LOCATION!
        self.Good_tgtv = visual.TextStim(win=win, name='GTgtv',
                                         text='0',
                                         font='Arial',
                                         pos=(0, 0), height=0.09, wrapWidth=None, ori=0.0,
                                         color=Colors.white, colorSpace='rgb255', bold=False,
                                         languageStyle='LTR',
                                         depth=0.0)  # CHANGE THE LOCATION!
        self.Total_tgtt = visual.TextStim(win=win, name='MTgtt',
                                          text=langue.get_string('MISSED'),
                                          font='Arial',
                                          pos=(0, 0), height=0.09, wrapWidth=None, ori=0.0,
                                          color=Colors.white, colorSpace='rgb255', bold=True,
                                          languageStyle='LTR',
                                          depth=0.0)  # CHANGE THE LOCATION!
        self.Total_tgtv = visual.TextStim(win=win, name='MTgtv',
                                          text='0',
                                          font='Arial',
                                          pos=(0, 0), height=0.09, wrapWidth=None, ori=0.0,
                                          color=Colors.white, colorSpace='rgb255', bold=False,
                                          languageStyle='LTR',
                                          depth=0.0)  # CHANGE THE LOCATION!
        self.Suggest_txt = visual.TextStim(win=win, name='suggest',
                                       text=langue.get_string('S_TO_PAUSE'),
                                       font='Arial',
                                       pos=(0, 0), height=0.06, wrapWidth=None, ori=0.0,
                                       color=Colors.white, colorSpace='rgb255', bold=True,
                                       languageStyle='LTR',
                                       depth=0.0)  # CHANGE THE LOCATION!

        self.slide_hlr = visual.ImageStim(win, image=self.slide_loc,
                                    pos=(0, 0), size=(set.wsize[1][0], set.wsize[1][1]), units='pix',  interpolate=False, opacity=1.0)
        self.monitor = None
        if self.type == 'SRC':
            if set.n_mon != 1:
                self.monitor = set.SRCwin
            else:
                self.monitor = set.SRCwin
            self.generate(self.monitor)
        elif self.type == 'NAV':
            self.monitor = set.NAVwin
            self.generate(self.monitor)

    def generate(self, n_monitor):
        # generate on the screen the flight director interface
        from settings import set
        h_space = (1 / 30)
        w_space = h_space / set.ratio[n_monitor]
        h_rect = 1 * ((1 - 4 * h_space) / n_num)
        r_border = 0.05  # 5% of the size is the border
        w_rect = 1 / set.ratio[n_monitor]

        # Set up the Face of the Flight Director
        self.face.size = (w_rect, h_rect)
        # Set up the border
        self.border.size = (w_rect*(1+r_border), h_rect*(1+r_border*3.5))
        # Set up the screen
        self.screen.size = (w_rect, h_rect/3)
        # Set up the LED
        self.led.size = (1.5*h_space, 1.5*h_space*set.ratio[n_monitor])

        if self.type == 'SRC':
            self.face.pos = ((1 - w_rect / 2), (1 - 3 * h_space - h_rect / 2))
            self.border.pos = ((1 - w_rect / 2), (1 - 3 * h_space - h_rect / 2))
            self.screen.pos = (1 - (2 * w_rect / 3 - 8 * w_space), (1 - 9 * h_space))
            self.led.pos = (1 - (w_rect - 3 * w_space), (1 - 5.5 * h_space))
            # Set up the Text SEARCH
            self.text_src.pos = (1 - (w_rect - 16 * w_space), (1 - 5.5 * h_space))
            # Set up the Text ITEM
            self.text_item.pos = (1 - (w_rect - 16 * w_space), (1 - 9 * h_space))
        if self.type == 'NAV':
            # These are just specular values around vertical axis
            self.face.pos = (-(1 - w_rect / 2), (1 - 3 * h_space - h_rect / 2))
            self.border.pos = (-(1 - w_rect / 2), (1 - 3 * h_space - h_rect / 2))
            self.screen.pos = (-(1 - (2 * w_rect / 3 - 8 * w_space)), (1 - 9 * h_space))
            self.led.pos = (-(1 - (w_rect - 3 * w_space)), (1 - 5.5 * h_space))
            self.text_src.pos = (-(1 - (w_rect - 16 * w_space)), (1 - 5.5 * h_space))
            self.text_item.pos = (-(1 - (w_rect - 16 * w_space)), (1 - 9 * h_space))

    def draw(self, case=0, nexts=-1):
        # I will pass also monitor, so I can eventually handle the 2 separated monitors
        from local import langue

        if set.n_mon != 1:
            screenSRC = 1
            screenNAV = 0
        else:
            screenSRC = 0
            screenNAV = 0

        if case == 1:  # CASE MAIN PHASE
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            if self.pause_txt.opacity != 0.0:
                self.pause_txt.opacity = 0.0
            if self.hold_text.opacity != 0.0:
                self.hold_text.opacity = 0.0
            self.border.draw()
            self.face.draw()
            self.screen.draw()
            self.led.draw()
            self.text_src.draw()
            self.text_item.draw()
        elif case == -5:  # Fill the forms please <string>
            self.update_graphics(type_m=self.type)
            self.form_txt.draw()
        elif case == -4:  # Welcome UASOS & SEARCH TUTORIAL SLIDES <graphics>
            # remember to hide all the previous things
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            if self.type == 'SRC':
                if nexts == 99:
                    nexts = 6  # Dims of the slides
                tot = 6

                if nexts == 0:  # No more slides to present
                    return -1
                if self.form_txt.opacity != 0.0:
                    self.form_txt.opacity = 0.0
                if nexts != -1:
                    self.s_final_pth = os.path.join(self.slide_path, langue.lang, f"m4_{(tot-nexts)%tot}.png")  # I pass sequentially the slides
                self.slide_hlr.image = self.s_final_pth
                self.slide_hlr.size = (set.wsize[screenSRC][0], set.wsize[screenSRC][1])
                self.slide_hlr.draw()
                return nexts
            else:
                self.noscreen_txt.draw()
        elif case == -3:  # NAV TUTORIALS <graphics>
            # remember to hide all the previous things
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            tot = 11
            if self.type == 'SRC':
                if nexts == 99:
                    nexts = 5  # Dims of the slides

                if nexts == 0:  # No more slides to present
                    return -1
                if self.form_txt.opacity != 1.0:
                    self.form_txt.opacity = 1.0
                if nexts != -1:
                    self.s_final_pth = os.path.join(self.slide_path, langue.lang,
                                                    f"m4_{(tot - nexts)% tot}.png")  # I pass sequentially the slides
                self.slide_hlr.image = self.s_final_pth
                self.noscreen_txt.draw()
            if self.type == 'NAV':
                if nexts != -1:
                    self.s_final_pth = os.path.join(self.slide_path, langue.lang,
                                                    f"m4_{(tot - nexts)% tot}.png")  # I pass sequentially the slides
                self.slide_hlr.image = self.s_final_pth
                self.slide_hlr.size = (set.wsize[screenNAV][0], set.wsize[screenNAV][1])
                if self.form_txt.opacity != 0.0:
                    self.form_txt.opacity = 0.0
                self.slide_hlr.draw()
            else:
                self.noscreen_txt.draw()
            return nexts
        elif case == -2:  # OVERALL TRAINING TUTORIAL <graphics>
            # remember to hide all the previous things
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            tot = 12
            if self.type == 'SRC':
                if nexts == 99:
                    nexts = 1  # Dims of the slides

                if nexts == 0:  # No more slides to present
                    return -1
                if self.form_txt.opacity != 0.0:
                    self.form_txt.opacity = 0.0
                if nexts != -1:
                    self.s_final_pth = os.path.join(self.slide_path, langue.lang,
                                                    f"m4_{(tot - nexts) % tot}.png")  # I pass sequentially the slides
                self.slide_hlr.image = self.s_final_pth
                self.slide_hlr.size = (set.wsize[screenSRC][0], set.wsize[screenSRC][1])
                self.slide_hlr.draw()
            if self.type == 'NAV':
                if nexts != -1:
                    self.s_final_pth = os.path.join(self.slide_path, langue.lang,
                                                    f"m4_{(tot - nexts) % tot}.png")  # I pass sequentially the slides
                self.slide_hlr.image = self.s_final_pth
                self.slide_hlr.size = (set.wsize[screenNAV][0], set.wsize[screenNAV][1])
                self.slide_hlr.draw()
            else:
                pass
            return nexts
        elif case == -1:  # MAIN PHASE INTRO <graphics>
            # remember to hide all the previous things
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            tot = 14
            if self.type == 'SRC':
                if nexts == 99:
                    nexts = 2  # Dims of the slides

                if nexts == 0:  # No more slides to present
                    return -1
                if self.form_txt.opacity != 0.0:
                    self.form_txt.opacity = 0.0
                if nexts != -1:
                    self.s_final_pth = os.path.join(self.slide_path, langue.lang,
                                                    f"m4_{(tot - nexts) % tot}.png")  # I pass sequentially the slides
                self.slide_hlr.image = self.s_final_pth
                self.slide_hlr.size = (set.wsize[screenSRC][0], set.wsize[screenSRC][1])
                self.slide_hlr.draw()
            if self.type == 'NAV':
                if nexts != -1:
                    self.s_final_pth = os.path.join(self.slide_path, langue.lang,
                                                    f"m4_{(tot - nexts) % tot}.png")  # I pass sequentially the slides
                self.slide_hlr.image = self.s_final_pth
                self.slide_hlr.size = (set.wsize[screenNAV][0], set.wsize[screenNAV][1])
                self.slide_hlr.draw()
            else:
                pass
            return nexts
        elif case == 0:  # Hold Text
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            self.hold_text.draw()  # Hold text for pressing start
        elif case == 2:  # SRC Training Operative <graphics> RT and ACC showing
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            if self.type == 'SRC':
                if self.pause_txt.opacity != 0.0:
                    self.pause_txt.opacity = 0.0
                if self.hold_text.opacity != 0.0:
                    self.hold_text.opacity = 0.0
                self.border.draw()
                self.face.draw()
                self.screen.draw()
                self.led.draw()
                self.text_src.draw()
                self.text_item.draw()
                # RT and ACC
                self.RT_txt.draw()
                self.RT_val.draw()
                self.TGT_txt.draw()
                self.Good_tgtt.draw()
                self.Good_tgtv.draw()
                self.Total_tgtt.draw()
                self.Total_tgtv.draw()
                self.Suggest_txt.draw()
            else:
                self.noscreen_txt.draw()
        elif case == 3:  # NAVI Training Operative <graphics> RT and ACC showing
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            if self.type == 'NAV':
                if self.pause_txt.opacity != 0.0:
                    self.pause_txt.opacity = 0.0
                if self.hold_text.opacity != 0.0:
                    self.hold_text.opacity = 0.0
                self.border.draw()
                self.face.draw()
                self.screen.draw()
                self.led.draw()
                self.text_src.draw()
                self.text_item.draw()
                # RT and ACC
                self.com_eval.draw()
                self.hdg_devt.draw()
                self.hdg_devv.draw()
                self.RT_txt.draw()
                self.RT_val.draw()
                self.TGT_txt.draw()
                self.Good_tgtt.draw()
                self.Good_tgtv.draw()
                self.Total_tgtt.draw()
                self.Total_tgtv.draw()
                self.Suggest_txt.draw()
            else:
                self.noscreen_txt.draw()
        elif case == 4:  # OVERALL Training Operative <graphics> RT and ACC showing
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            if self.pause_txt.opacity != 0.0:
                self.pause_txt.opacity = 0.0
            if self.hold_text.opacity != 0.0:
                self.hold_text.opacity = 0.0
            self.border.draw()
            self.face.draw()
            self.screen.draw()
            self.led.draw()
            self.text_src.draw()
            self.text_item.draw()
            if self.type == 'SRC':
                # RT and ACC
                self.RT_txt.draw()
                self.RT_val.draw()
                self.TGT_txt.draw()
                self.Good_tgtt.draw()
                self.Good_tgtv.draw()
                self.Total_tgtt.draw()
                self.Total_tgtv.draw()
                self.Suggest_txt.draw()
            if self.type == 'NAV':
                # RT and ACC
                self.com_eval.draw()
                self.hdg_devt.draw()
                self.hdg_devv.draw()
                self.RT_txt.draw()
                self.RT_val.draw()
                self.TGT_txt.draw()
                self.Good_tgtt.draw()
                self.Good_tgtv.draw()
                self.Total_tgtt.draw()
                self.Total_tgtv.draw()
                self.Suggest_txt.draw()
        elif case == 5:  # Thank you <string>
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            self.thank_you.draw()
        elif case == 6:  # Pause <string>
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            self.pause_txt.draw()
        elif case == 7:  # VAS <graphics>
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            self.vas_txt.draw()
        elif case == 8:  # Phase end
            if not self.correct_lang and langue.lang != 'fr':
                self.correct_lang = self.update_graphics(type_m=self.type)
            self.end_txt.draw()

    def update_graphics(self, type_m=None):
        from local import langue

        if type_m == 'SRC':
            self.RT_txt.setPos((0.7, 0.0))
            self.RT_val.setPos((0.7, -0.1))
            self.TGT_txt.setPos((0.7, -0.3))
            if langue.lang == 'en':
                self.Good_tgtt.setPos((0.60, -0.40))
                self.Good_tgtv.setPos((0.83, -0.40))
                self.Total_tgtt.setPos((0.56, -0.50))
                self.Total_tgtv.setPos((0.83, -0.50))
                self.Suggest_txt.setPos((0.7, -0.7))
            elif langue.lang == 'fr':
                self.Good_tgtt.setPos((0.60, -0.40))
                self.Good_tgtv.setPos((0.83, -0.40))
                self.Total_tgtt.setPos((0.595, -0.50))
                self.Total_tgtv.setPos((0.83, -0.50))
                self.Suggest_txt.setPos((0.7, -0.7))
            elif langue.lang == 'it':
                self.Good_tgtt.setPos((0.60, -0.40))
                self.Good_tgtv.setPos((0.83, -0.40))
                self.Total_tgtt.setPos((0.60, -0.50))
                self.Total_tgtv.setPos((0.83, -0.50))
                self.Suggest_txt.setPos((0.7, -0.7))
        elif type_m == 'NAV':
            self.com_eval.setPos((-0.7, 0.35))
            self.hdg_devt.setPos((-0.78, 0.2))
            self.hdg_devv.setPos((-0.58, 0.2))
            self.RT_txt.setPos((-0.7, 0.0))
            self.RT_val.setPos((-0.7, -0.1))
            self.TGT_txt.setPos((-0.7, -0.3))
            if langue.lang == 'en':
                self.Good_tgtt.setPos((-0.80, -0.40))
                self.Good_tgtv.setPos((-0.56, -0.40))
                self.Total_tgtt.setPos((-0.80, -0.50))
                self.Total_tgtv.setPos((-0.56, -0.50))
                self.Suggest_txt.setPos((-0.7, -0.7))
            elif langue.lang == 'fr':
                self.Good_tgtt.setPos((-0.75, -0.40))
                self.Good_tgtv.setPos((-0.55, -0.40))
                self.Total_tgtt.setPos((-0.75, -0.50))
                self.Total_tgtv.setPos((-0.55, -0.50))
                self.Suggest_txt.setPos((-0.7, -0.7))
            elif langue.lang == 'it':
                self.Good_tgtt.setPos((-0.80, -0.40))
                self.Good_tgtv.setPos((-0.60, -0.40))
                self.Total_tgtt.setPos((-0.80, -0.50))
                self.Total_tgtv.setPos((-0.60, -0.50))
                self.Suggest_txt.setPos((-0.7, -0.7))

        self.pause_txt.text = langue.get_string('PAUSE')
        self.form_txt.text = langue.get_string('FORM')
        self.noscreen_txt.text = langue.get_string('NOT_ACTIVE')
        self.hold_text.text = langue.get_string('HOLD')
        self.vas_txt.text = langue.get_string('VAS_REQUEST')
        self.Suggest_txt.text = langue.get_string('S_TO_PAUSE')
        self.thank_you.text = langue.get_string('THANK_YOU')
        self.end_txt.text = langue.get_string('END_OF_PHASE')
        if type_m == 'SRC':
            self.text_src.text = langue.get_string('SEARCH')
            self.TGT_txt.text = langue.get_string('TARGETS')
        elif type_m == 'NAV':
            self.text_src.text = langue.get_string('NAVIGATE')
            self.TGT_txt.text = langue.get_string('WAYPOINT')
        self.Good_tgtt.text = langue.get_string('DETECTED')
        self.Total_tgtt.text = langue.get_string('TOTAL')
        self.hdg_devt.text = langue.get_string('HDG_DEV')

        return True

    def item_change(self, id_item):
        from local import langue
        if id_item == 1:
            self.text_item.text = langue.get_string('PEOPLE')
        elif id_item == 4:
            self.text_item.text = langue.get_string('VEHICLES')
        elif id_item == 5:
            self.text_item.text = langue.get_string('HEADING')
        elif id_item == 6:
            self.text_item.text = langue.get_string('WAYPOINT')
        else:
            self.text_item.text = langue.get_string('NONE')
        return

    def make_na(self):
        from local import langue
        self.com_eval.text = langue.get_string('N/A')
        self.com_eval.color = Colors.white
        self.com_eval.draw()

    def make_correct(self):
        from local import langue
        self.com_eval.text = langue.get_string('CORRECT')
        self.com_eval.color = Colors.green
        self.com_eval.draw()

    def make_wrong(self):
        from local import langue
        self.com_eval.text = langue.get_string('WRONG')
        self.com_eval.color = Colors.red
        self.com_eval.draw()

    def led_on(self):
        self.led.color = Colors.green

    def led_off(self):
        self.led.color = Colors.dgreen
