# -*- coding: utf-8 -*-

from gi.repository import Gtk,GdkPixbuf,Gdk

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
        
    def on_about_clicked(self,widget):
        b = Gtk.Builder()
        b.add_from_file("src/gui/glade/aboutDialog.glade")
        d = b.get_object("about")
        d.set_comments(_("""Publi' Photo was develop in order to help the publishing of professional or semi-professional photographies.
The main idea is that in majority, country's law say that a photography will automaticly be protected by the intellectual property. So the public domain suffer of this, cause lots of pictures could free as in freedom.
Publi' Photo is here to help people to distribute their photographies with a free licence."""))
        d.set_logo(GdkPixbuf.Pixbuf.new_from_file("src/publiphoto.svg"))
        d.run()
        d.destroy()