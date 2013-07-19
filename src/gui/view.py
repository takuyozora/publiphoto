# -*- coding: utf-8 -*-

from gi.repository import Gtk
from src.tools import root_path

######
# Classe de base pour une view
######

class View(Gtk.Alignment):
    """
        This class define a view and a constructor
         which load a glade view and connect theses signals
    """
    
    def __init__(self,gladeFile,viewName):
        Gtk.Alignment.__init__(self)
        
        ## Load from Glade
        self.builder = Gtk.Builder()
        self.builder.add_from_file(gladeFile)
        self.builder.connect_signals(self)
        self.viewBox = self.builder.get_object(viewName)
        
        try:
            self.viewBox.unparent()
        except AttributeError as e:
            print(e)
        self.add(self.viewBox)
        
    def load_objects(self,object_liste):
        """
            Return a dictionary contains objects loaded
        """
        result = dict()
        for object in object_liste:
            result[object] = self.builder.get_object(object)
        return result
        
        