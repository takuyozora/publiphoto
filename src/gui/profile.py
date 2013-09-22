# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gettext import gettext as _

import os
import sys

from src.gui import view
from src.gui.process import ProcessView


from src.profile import load_profile
from src.tools import numbify
from src.config import LICENCES
from src.profile import load_profile, get_profiles, Profile

# ##
# Todo : comprendre pourquoi l'import de manage (on save clicked) plante si il est placé au début
# (Peut-être à cause d'une boucle d'import ou d'un problème de nommage parès l'unification des profile gui)
# ##


class ProfileView(view.View):
    
    def __init__(self,parent,previous):
        view.View.__init__(self,"src/gui/glade/genericProfileView.glade")
        
        self.previous = previous
        
        self.elems = self.load_objects(["toggleSize","toggleAuthor","toggleLicence","toggleFont","toggleRename","toggleDir",
                                        "sizeView","authorView","licenceView","fontView","renameView","dirView","profileView","buttonView","nameView",
                                        "mainLabel","processButtonBox","editButtonBox","profileNameBox","dirLabel",
                                               "selectDirBox","dirBoxSmall","renameBoxAll","renameBoxSmall","customisedFontBox","profileBox","fontBox",
                                               "h","w","ratio","author","font","name","prefixe","suffixe","newname","dir"])
        ## Transform into only number entry
        numbify(self.elems['w'])
        numbify(self.elems['h'])
        
        ## Create the licence chooser widget
        licences = LICENCES
        self.licenceChooser = Gtk.ComboBoxText()
        for elem in licences:
            self.licenceChooser.append_text(elem)
        self.licenceChooser.set_entry_text_column(0)
        self.licenceChooser.set_id_column(0)
        self.licenceChooser.set_active_id(licences[0])
        self.elems["licenceView"].pack_start(self.licenceChooser,False,False,0)
        self.elems["licenceView"].show_all()
        
        self.parent = parent
        
    def create_profile_from_entry(self):
        p = Profile()
        
        if self.elems["toggleSize"].get_active():
            w = self.elems["w"].get_text()
            h = self.elems["h"].get_text()
            ratio = self.elems["ratio"].get_active()
            p.size = (w,h,ratio)
        else:
            p.size = False
            
        if self.elems["toggleAuthor"].get_active():
            p.author = self.elems["author"].get_text()
        else:
            p.author == False    
                
        if self.elems["toggleLicence"].get_active():
            p.licence = self.licenceChooser.get_active_text()
        else:
            p.licence == False
        
        if self.elems["toggleRename"].get_active():
            p.rename = (self.elems["prefixe"].get_text(),self.elems["suffixe"].get_text())
        else:
            p.rename == False
            
        return p

        
    def fill_with_profile(self,p):
        if p.author is not False:
            self.elems["toggleAuthor"].set_active(True)
            self.elems["author"].set_text(p.author)
        else:
            self.elems["toggleAuthor"].set_active(False)
            self.elems["author"].set_text("")
            
        if p.size is not False:
            self.elems["toggleSize"].set_active(True)
            self.elems["w"].set_text(p.size[0])
            self.elems["h"].set_text(p.size[1])
            self.elems["ratio"].set_active(p.size[2])
        else:
            self.elems["toggleSize"].set_active(False)
            self.elems["w"].set_text("")
            self.elems["h"].set_text("")
            self.elems["ratio"].set_active(True)
            
        if p.licence is not False:
            self.elems["toggleLicence"].set_active(True)
            self.licenceChooser.set_active_id(p.licence)
        else:
            self.elems["toggleLicence"].set_active(False)
            self.licenceChooser.set_active_id(LICENCES[0])
            
        if p.rename is not False:
            self.elems["toggleRename"].set_active(True)
            self.elems["prefixe"].set_text(p.rename[0])
            self.elems["suffixe"].set_text(p.rename[1])
        else:
            self.elems["toggleRename"].set_active(False)
            self.elems["prefixe"].set_text("")
            self.elems["suffixe"].set_text("")
            
        self.elems["toggleDir"].set_active(p.dir in (True,None))
        self.elems["dirView"].set_sensitive(p.dir in (True,None))   
        
    def on_file_selected(self,widget):
        pass
    
    def on_dir_selected(self,widget):
        pass
        
    def on_size_toggled(self,widget,n):
        self.elems["sizeView"].set_sensitive(widget.get_active())
    
    def on_author_toggled(self,widget,n):
        self.elems["authorView"].set_sensitive(widget.get_active())
    
    def on_licence_toggled(self,widget,n):
        self.elems["licenceView"].set_sensitive(widget.get_active())
        
    def on_rename_toggled(self,widget,n):
        self.elems["renameView"].set_sensitive(widget.get_active())
        
    def on_font_toggled(self,widget,n):
        pass
    
    def on_dir_toggled(self,widget,n):
        self.elems["dirView"].set_sensitive(widget.get_active())
        
    def on_autodir_clicked(self,widget,uri):
        pass
        
    def on_return_clicked(self,widget):
        self.parent.switch_view(self.previous)
    
    def on_continue_clicked(self,widget):
        pass
    
    def on_save_clicked(self,widget):
        pass
        
class ProcessProfileView(ProfileView):
    def __init__(self,parent,previous,files):
        ProfileView.__init__(self, parent, previous)
        
        self.files = files
        
        self.elems["profileBox"].reparent(self.elems["profileView"])
        self.elems["selectDirBox"].reparent(self.elems["dirView"])
        self.elems["renameBoxAll"].reparent(self.elems["renameView"])
        self.elems["processButtonBox"].reparent(self.elems["buttonView"])
        
        ## Create the profile chooser
        profiles = get_profiles()
        self.profileChooser = Gtk.ComboBoxText()
        self.profileChooser.set_entry_text_column(0)
        self.profileChooser.connect("changed",self.on_profile_changed)
        for elem in profiles:
            self.profileChooser.append_text(elem)
        self.elems["profileBox"].pack_start(self.profileChooser,False,False,0)
        self.elems["profileBox"].show_all()
        
        self.elems["mainLabel"].set_text(_("Operations to apply"))
        
        self.on_dir_selected(self.elems["dir"])
        self.on_autodir_clicked(self.elems["dir"], "auto")
        
    def create_profile_from_entry(self):
        p = ProfileView.create_profile_from_entry(self)
        
        if self.elems["toggleRename"].get_active():
            p.rename = (p.rename[0],p.rename[1],self.elems["newname"].get_text())
            
        if self.elems["toggleDir"].get_active():
            p.dir = self.elems["dir"].get_filename()
        else:
            p.dir = False
            
        currentProfile = self.profileChooser.get_active_text()
        if currentProfile is not None:
            p.font = load_profile(currentProfile).font
            
        return p
    
    def on_continue_clicked(self,widget):
        self.parent.switch_view(ProcessView(self.parent,self.files,self.create_profile_from_entry().__dict__))
        
    def on_autodir_clicked(self,widget,uri):
        if uri == "auto":
            self.elems["dir"].unselect_all()
            self.elems["dir"].set_sensitive(False)
        else:
            self.elems["dir"].set_sensitive(True)
            if sys.platform.startswith('linux'):
                self.elems["dir"].set_filename(os.environ["HOME"])
            else:
                self.elems["dir"].set_filename(os.path.expanduser('~user'))
        return True # Do not show the link
        
    def on_dir_selected(self, widget):
        if widget.get_filename() is not None:
            self.elems["dirLabel"].set_markup(_("<i><span size='small'>If you want to automaticly create a new directory click <a href='auto'>here</a></span></i>"))
        else:
            self.elems["dirLabel"].set_markup(_("<i><span size='small'>Currently a new directory will be create, if you don't want, click <a href='unauto'>here</a></span></i>"))
            
        
    def on_profile_changed(self,widget):
        self.fill_with_profile(load_profile(widget.get_active_text()))
        
class EditProfileView(ProfileView):
    
    def __init__(self,parent,previous,profile=None):
        ProfileView.__init__(self, parent, previous)
        
        self.elems["profileNameBox"].reparent(self.elems["nameView"])
        self.elems["dirBoxSmall"].reparent(self.elems["dirView"])
        self.elems["renameBoxSmall"].reparent(self.elems["renameView"])
        self.elems["customisedFontBox"].reparent(self.elems["fontView"])
        self.elems["editButtonBox"].reparent(self.elems["buttonView"])
        
        self.elems["prefixe"] = self.builder.get_object("prefixe1")
        self.elems["suffixe"] = self.builder.get_object("suffixe1")
        
        self.profile = profile
        if self.profile is not None:
            self.elems["mainLabel"].set_text(_("Edit profile"))
            self.elems["name"].set_text(previous.currentSelected)
            self.fill_with_profile(load_profile(self.profile))
        
    def create_profile_from_entry(self):
        p = ProfileView.create_profile_from_entry(self)
        
        if self.elems["toggleDir"].get_active():
            p.dir = True
        else:
            p.dir = False
        if self.elems["toggleFont"].get_active():
            p.font = self.elems["font"].get_filename()
        else:
            p.font = False
            
        return p
    
    def on_save_clicked(self,widget):
        if self.elems["name"].get_text() in get_profiles():
            dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL, _("A profile already has this name"))
            dialog.format_secondary_text(
                _("Are you sure to save this profile and lose the older one ?"))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                dialog.destroy()
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                return
        try:
            self.create_profile_from_entry().save(self.elems["name"].get_text())
            dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, _("Succed to create the profile"))
            dialog.run()
            dialog.destroy()
        except:
            dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, _("An error occured"))
            dialog.format_secondary_text(
                _("Unable to save the profile"))
            dialog.run()
            dialog.destroy()
            return
        finally:
            from src.gui import manage
            self.parent.switch_view(manage.ManageProfileView(self.parent))
        
    def on_font_toggled(self,widget,n):
        self.elems["fontBox"].set_sensitive(widget.get_active())