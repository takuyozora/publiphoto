# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk

from gettext import gettext as _

from src.gui import view
from src.settings import load_settings, Settings
from src.tools import convert_to_rgb, convert_to_rgba

######
# This module can set settings :
# * Font
#    -- Size
#    -- Color
#    -- HaloSize
#    -- HaloColor
#    -- Font path
# * Default directory name
######
######
# Ce module permet de gérer les préférences :
#  * Police 
#    -- Taille
#    -- Couleur
#    -- Halo
#    -- Couleur du Halo
#    -- Font
#  * Nom du répertoire par défaut
######

class SettingView(view.View):
    
    def __init__(self,parent):
        view.View.__init__(self,"src/gui/glade/settingView.glade","settingBox")
        
        self.entires = self.load_objects([
                                          "fontScale","haloScale","fontPath","fontColor","haloColor",
                                          "bottom-left","bottom-right","center","top-left","top-right","angle",
                                          "dirName"])
        
        self.fill_with_settings()
        self.on_corner_changed(self.entires["center"])
        self.parent = parent
        
    def fill_with_settings(self):
        sett = load_settings()
        self.entires["fontScale"].set_value(sett.font["scale"])
        self.entires["haloScale"].set_value(sett.font["haloScale"])
        self.entires["fontPath"].set_filename(sett.font["path"])
        self.entires["fontColor"].set_rgba(convert_to_rgba(sett.font["color"]))
        self.entires["haloColor"].set_rgba(convert_to_rgba(sett.font["haloColor"]))
        self.entires["angle"].set_value(sett.position["angle"])
        self.entires[sett.position["corner"]].set_active(True)
        self.entires["dirName"].set_text(sett.dirName)
        self.show_all()
     
    def fill_settings(self):
        sett = Settings()
        sett.font["scale"] = (float)(self.entires["fontScale"].get_value())
        sett.font["haloScale"] = (float)(self.entires["haloScale"].get_value())
        sett.font["path"] = (str)(self.entires["fontPath"].get_filename())
        sett.font["color"] = convert_to_rgb(self.entires["fontColor"].get_rgba())
        sett.font["haloColor"] = convert_to_rgb(self.entires["haloColor"].get_rgba())
        sett.position["angle"] = (float)(self.entires["angle"].get_value())*(int)(self.entires["center"].get_active())
        sett.position["corner"] = self.find_corner()
        sett.dirName = (str)(self.entires["dirName"].get_text())
        return sett
    
    def find_corner(self):
        for radio in self.entires["bottom-left"].get_group():
            if radio.get_active():
                for name, widget in self.entires.items():
                    if widget == radio:
                        return name
                    
    def on_corner_changed(self,widget):
        self.entires["angle"].set_sensitive(self.entires["center"].get_active())
        
    def on_save_clicked(self,widget):
        dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.QUESTION,
        Gtk.ButtonsType.OK_CANCEL, _("Confirm saving"))
        dialog.format_secondary_text(
            _("Are you sure to replace settings ?"))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return
        
        self.fill_settings().save()
        
    def on_return_clicked(self,widget):
        self.parent.init_welcome_view()
        