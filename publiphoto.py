#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GObject, Gdk, GLib
from src.gui.mainwindow import MainWindow

import os
import locale
import os
import sys
import gettext

######
# PubliPhoto version alpha 1.0
# Créé par Olivier Radisson
# Licence : GNU GPL v3 ou suppérieure
# Contact : contacter [dot] oradisson [dot] fr
######

# setup translation support
(lang_code, encoding) = locale.getlocale()
LOCALE_DOMAIN = 'publiphoto'
LOCALE_DIR = os.path.join(sys.prefix, 'share', 'locale')
 
gettext.bindtextdomain(LOCALE_DOMAIN, LOCALE_DIR)   # (1)
gettext.textdomain(LOCALE_DOMAIN)                   # (2)
gettext.install(LOCALE_DOMAIN)                      # (3)
# Gtk.bindtextdomain(LOCALE_DOMAIN, LOCALE_DIR) # (4)
# Gtk.textdomain(LOCALE_DOMAIN)                 # (5)

# Set the current directory to match files
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    window = MainWindow()
    window.show_all()
    
    GLib.threads_init()
    GObject.threads_init()
    Gdk.threads_init()
    
    Gtk.main()