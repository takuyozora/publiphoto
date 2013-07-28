# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk

from src.gui import view
from src.gui.labelize import SelectPhotoView
from src.gui.manage import ManageProfileView
from src.gui.settings import SettingView 

######
# This class is the first view which be shown
######

class WelcomeView(view.View):
    
    def __init__(self,parent):
        view.View.__init__(self,"src/gui/glade/welcomeView.glade","welcomeBox")
        
        self.parent = parent        
        
    def on_start_clicked(self,widget):
        self.parent.switch_view(SelectPhotoView(self.parent))
        
    def on_manageprofile_clicked(self,widget):
        self.parent.switch_view(ManageProfileView(self.parent))
        
    def on_setting_clicked(self,widget):
        self.parent.switch_view(SettingView(self.parent))