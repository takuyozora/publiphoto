# -*- coding: utf-8 -*-

import sys
import os
import pickle

######
# This module help to manage profiles
# It saves and load profiles from a fixed repertory, due to the current system
######
######
# Ce module permet de gérer les profils
# Il enregistre et charge les profiles depuis un répertoire fixé, s'adaptant à la plateforme
######

if sys.platform.startswith('linux'):
    PROFILE_PATH=os.path.join(os.environ["HOME"],".publiphoto","profiles")
else:
    PROFILE_PATH=os.path.join(os.path.expanduser('~user'),"Publiphoto","profiles")
    
    
if os.path.exists(PROFILE_PATH) is not True:
    os.makedirs(PROFILE_PATH)

class Profile:
    """
        Main class 
    """
    
    def __init__(self):
        self.licence = False
        self.author = False
        self.size = False
        self.font = False
        self.rename = False
        self.dir = False
        self._version = 1.0
        self._compatibility = [1.0]
        
    def __repr__(self):
        return (str)(self.__dict__)
    
    def __str__(self):
        return (str)(self.__dict__)
        
    def save(self,name):
        with open(os.path.join(PROFILE_PATH,name+".profile"),'wb+') as file:
            pickle.dump(self,file)
            
def load_compatibility(p):
    actual_p = Profile()
    if p._version == actual_p._version:
        return p
    elif p._version in actual_p._compatible:
        ## Try to return a compatible profile object
        return sett ## Actualy only one version is compatible
    else:
        ## Can't load this profile
        return False

def load_profile(name):
    with open(os.path.join(PROFILE_PATH,name+".profile"),'rb') as f:
        return load_compatibility(pickle.load(f))
    
def get_profiles():
    profiles = []
    for elem in os.listdir(PROFILE_PATH):
        p = elem.replace(".profile","")
        if p is not False:
            profiles.append(p)
    return profiles

def del_profile(name):
    return os.remove(os.path.join(PROFILE_PATH,name+".profile"))

