# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk

from src.gui import view
from src.settings import load_settings, Settings
from src.tools import convert_to_rgb, convert_to_rgba

######
# Ce module permet de gérer les préférences :
#  * Police 
#    -- Taille
#    -- Couleur
#    -- Halo
#    -- Font
#  * Nom du répertoire par défaut
######

class SettingView(view.View):
    
    def __init__(self,parent):
        view.View.__init__(self,"src/gui/glade/settingView.glade","settingBox")
        
        self.entires = self.load_objects([
                                          "fontScale","fontPath","fontColor","haloColor",
                                          "dirName"])
        
        self.fill_with_settings()
        self.parent = parent
        
    def fill_with_settings(self):
        sett = load_settings()
        self.entires["fontScale"].set_value(sett.font["scale"])
        self.entires["fontPath"].set_filename(sett.font["path"])
        print(convert_to_rgba(sett.font["color"]))
        print(convert_to_rgba(sett.font["haloColor"]))
        self.entires["fontColor"].set_rgba(convert_to_rgba(sett.font["color"]))
        self.entires["haloColor"].set_rgba(convert_to_rgba(sett.font["haloColor"]))
        self.entires["dirName"].set_text(sett.dirName)
     
    def fill_settings(self):
        sett = Settings()
        sett.font["scale"] = (float)(self.entires["fontScale"].get_value())
        sett.font["path"] = (str)(self.entires["fontPath"].get_filename())
        sett.font["color"] = convert_to_rgb(self.entires["fontColor"].get_rgba())
        sett.font["haloColor"] = convert_to_rgb(self.entires["haloColor"].get_rgba())
        sett.dirName = (str)(self.entires["dirName"].get_text())
        return sett
        
    def on_save_clicked(self,widget):
        dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.QUESTION,
        Gtk.ButtonsType.OK_CANCEL, "Confirmer l'enregistrement")
        dialog.format_secondary_text(
            "Êtes vous sur de vouloir remplacer les préférences par celles-ci ?")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            return
        
        self.fill_settings().save()
        
    def on_return_clicked(self,widget):
        self.parent.init_welcome_view()
        