# -*- coding: utf-8 -*-

import os
import sys
from os import path
import mimetypes
from src import config 
from gi.repository import Gdk

from urllib.parse import unquote

######
# This module contains some function which help to manage data
######
######
# Ce module comporte un lot de fonctions utiles qui permettent de traiter des donnees
######

def convert_to_rgba(color):
    return Gdk.RGBA(color[0]/255,color[1]/255,color[2]/255,0)

def convert_to_rgb(rgba):
    return ((int)(255*rgba.red),(int)(255*rgba.green),(int)(255*rgba.blue))

def from_uri_to_path(files):
    new_list = []
    for elem in files:
        elem = unquote(elem) # Transform URL format to normal encoding (%20 => " ")
        elem = elem.replace("file://","")  # Remove file://
        if not sys.platform.startswith('linux'):
            elem = elem[1:] # WINDOWS compatibility (remove the first /)
        new_list.append(elem)
    return new_list
        

def root_path(path):
    return path

def numbify(widget): # Only accept numbers for an entry
    def filter_numbers(entry, *args):
        text = entry.get_text().strip()
        entry.set_text(''.join([i for i in text if i in '0123456789']))

    widget.connect('changed', filter_numbers)

def get_all_files(files,recursive=True): 
    file_list= []
    for elem in files:
        if path.isfile(elem):
            select_file(elem,file_list)
        elif path.isdir(elem):
            if recursive:
                file_list.extend(cross_recursive(elem))
                
    return file_list

def cross_recursive(dir):
    file_list = []
    for elem in os.listdir(dir):
        elem = path.join(dir,elem)
        if path.isfile(elem):
            select_file(elem,file_list)
        elif path.isdir(elem):
            file_list.extend(cross_recursive(elem))
    return file_list

def select_file(path,file_list): # Select or not a file from is mimetype
    mime =  mimetypes.guess_type(path)[0]
    if type(mime) is not str:
        return
    if "image" in mime:
        file_list.append(path) 