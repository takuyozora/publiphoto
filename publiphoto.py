#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GObject, Gdk, GLib
from src.gui.mainwindow import MainWindow

import os

######
# PubliPhoto version alpha 1.0
# Créé par Olivier Radisson
# Licence : GNU GPL v3 ou suppérieure
# Contact : contacter [dot] oradisson [dot] fr
######


os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    window = MainWindow()
    window.show_all()
    
    GLib.threads_init()
    GObject.threads_init()
    Gdk.threads_init()
    
    Gtk.main()