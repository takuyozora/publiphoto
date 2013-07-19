# -*- coding: utf-8 -*-

import sys 

from gi.repository import Gtk

from ..gui.welcome import WelcomeView
from src.gui.labelize import SelectPhotoView
from src.tools import root_path 


import os
######
# Classe de base du programme, gère le changement de view
######

class MainWindow(Gtk.Window):
    """
        MainWindow of Help me IF You Can
    """
    
    def __init__(self):
        Gtk.Window.__init__(self, title="Publi' Photo")
        self.set_default_size(600,400)
        self.set_icon_from_file("src/publiphoto.svg")
        self.connect("destroy",self.on_destroy)
        
        self.mainBox = Gtk.VBox() # Main container of the window
        self.current_view = None
        
        self.init_default_window()
        if len(sys.argv) < 2:
            self.init_welcome_view()
        else:
            self.switch_view(SelectPhotoView(self,sys.argv))
        
    def init_default_window(self):
        builder = Gtk.Builder()
        builder.add_from_file("src/gui/glade/mainWindow.glade")
        self.mainBox = builder.get_object("mainBox")
        self.viewContainer = builder.get_object("viewContainer")
        self.mainBox.reparent(self) # Reparent mainBox (cause it's already parent in glade)
        
    def switch_view(self,view):
        self.clean_viewContainer()
        self.current_view = view
        self.viewContainer.pack_start(self.current_view,True,True,0)
        self.current_view.show()
        
    def init_welcome_view(self):
        self.switch_view(WelcomeView(self))
        
        
    def clean_viewContainer(self):
        if self.current_view is not None:
            self.viewContainer.remove(self.current_view)
            
    def on_destroy(self,widget):
        Gtk.main_quit()
        
        