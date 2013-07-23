# -*- coding: utf-8 -*-

import sys
import os
import pickle

######
# Ce module permet de gérer les profiles
# Il enregistre et charge les profiles depuis un répertoire fixé, s'adaptant à la plateforme
######

if sys.platform.startswith('linux'):
    SETTINGS_PATH=os.path.join(os.environ["HOME"],".publiphoto")
else:
    SETTINGS_PATH=os.path.join(os.path.expanduser('~user'),"Publiphoto")
    
if os.path.exists(SETTINGS_PATH) is not True:
    os.makedirs(SETTINGS_PATH)

class Settings:
    """
        Main class 
    """
    
    def __init__(self):
        self.font = {"scale":1,"haloScale":1,"path":"src/media/DejaVuSansCondensed.ttf","color":(255,255,255),"haloColor":(0,0,0)}
        self.dirName = "publiphoto"
        
    def __repr__(self):
        return (str)(self.__dict__)
        
    def save(self):
        with open(os.path.join(SETTINGS_PATH,"publiphoto.settings"),'wb+') as file:
            pickle.dump(self,file)

def load_settings():
    try:
        with open(os.path.join(SETTINGS_PATH,"publiphoto.settings"),'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        ## If here, settings doesn't exist
        sett = Settings()
        sett.save()
        return sett
