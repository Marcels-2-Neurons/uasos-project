# local.py>
# Library used for Experiment Localization
# Imported in flight director as library
# Author: Vincenzo Maria VITALE - DCAS - MS TAS AERO - FTE
###################################################################

import json

global langue


class local:
    def __init__(self, lang='fr'):
        self.lang = lang
        self.file_path = "./localization/lang.json"
        self.translations = {}

        self.load_translations()

    def load_translations(self):
        with open(self.file_path, 'rb') as file:
            self.translations = json.load(file, encoding='utf-8')

    def set_language(self, lang):
        langs = {'fr':'Change la langue en Français',
                 'en':'Changing Language to English',
                 'it':'Cambio la lingua in Italiano'}
        self.lang = lang
        print(langs[lang])
        self.load_translations()

    def get_string(self, key):
        if key in self.translations and self.lang in self.translations[key]:
            return self.translations[key][self.lang]
        else:
            return key


langue = local()
