# -*- coding: utf-8 -*-

import sys
import os
import pickle

######
# Ce module permet de gérer les profiles
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
        
    def save(self,name):
        with open(os.path.join(PROFILE_PATH,name+".profile"),'wb+') as file:
            pickle.dump(self,file)

def load_profile(name):
    with open(os.path.join(PROFILE_PATH,name+".profile"),'rb') as f:
        return pickle.load(f)
    
def get_profiles():
    profiles = []
    for elem in os.listdir(PROFILE_PATH):
        profiles.append(elem.replace(".profile",""))
    return profiles

def del_profile(name):
    return os.remove(os.path.join(PROFILE_PATH,name+".profile"))

