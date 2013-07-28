# -*- coding: utf-8 -*-

import sys
import os
import pickle

######
# This module help to manage settings
# It saves and load settings from a fixed repertory, due to the current system
######
######
# Ce module permet de gérer les préférences
# Il enregistre et charge les préférences depuis un répertoire fixé, s'adaptant à la plateforme
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
        self._version = 1.0
        self._compatible = [1.0]
        
    def __repr__(self):
        return (str)(self.__dict__)
    
    def __str__(self):
        return (str)(self.__dict__)
        
    def save(self):
        with open(os.path.join(SETTINGS_PATH,"publiphoto.settings"),'wb+') as file:
            pickle.dump(self,file)
            
def load_compatibility(sett):
    actual_sett = Settings()
    if sett._version == actual_sett._version:
        return sett
    elif sett._version in actual_sett._compatible:
        ## Try to return a compatible setting object
        return sett ## Actualy only one version is compatible
    else:
        ## Return new default settings
        actual_sett.save()
        return actual_sett
        

def load_settings():
    try:
        with open(os.path.join(SETTINGS_PATH,"publiphoto.settings"),'rb') as f:
            return load_compatibility(pickle.load(f))
    except FileNotFoundError:
        ## If here, settings doesn't exist
        sett = Settings()
        sett.save()
        return sett
