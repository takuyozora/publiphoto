# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk

from gettext import gettext as _

from src.config import LICENCES
from src.tools import numbify
from src.gui import view
from src.gui.profile import EditProfileView
from src.profile import get_profiles, del_profile, Profile, load_profile


######
# This module manages profiles, it can add or delete profiles
# It contains two class :
#  * NewProfileView which can create or edit a profile
#  * ManageProfileView which list profiles and allow user to delte a profile
######
######
# Ce module s'occupe de gérer les profils, il permet d'ajouter modifier ou supprimer les profils
# Il comporte deux classes :
#  * NewProfileView qui sert à la création et à l'édition de profil
#  * ManageProfileView qui sert à lister et supprimer les profils
######

class NewProfileView(view.View):
    """
        View to create a profile
    """
    
    def __init__(self,parent,modify=None):
        view.View.__init__(self,"src/gui/glade/newProfileView.glade","newBox")
        
        self.sizeBox = self.builder.get_object("sizeBox")
        self.authorBox = self.builder.get_object("authorBox")
        self.licenceBox = self.builder.get_object("licenceBox")
        self.fontBox = self.builder.get_object("fontBox")
        self.renameBox = self.builder.get_object("renameBox")
        self.dirBox = self.builder.get_object("dirBox")
        
        self.elems = self.load_objects(["toggleSize","toggleAuthor","toggleLicence","toggleFont","toggleRename","toggleDir","h","w","ratio","author","font","name","prefixe","suffixe"])
        numbify(self.elems['w'])
        numbify(self.elems['h'])
        
        self.authorEntry = self.builder.get_object("authorEntry")

        licences = LICENCES
        self.licenceChooser = Gtk.ComboBoxText()
        for elem in licences:
            self.licenceChooser.append_text(elem)
        self.licenceChooser.set_entry_text_column(0)
        self.licenceChooser.set_id_column(0)
        self.licenceChooser.set_active_id(licences[0])
        self.licenceBox.pack_start(self.licenceChooser,False,False,0)
        self.licenceBox.show_all()
        
        self.font = None
        self.parent = parent
        
        if modify is not None:
            p = load_profile(modify)
            self.elems["name"].set_text(modify)
            self.fill_with_profile(p)
            
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
        self.dirBox.set_sensitive(p.dir in (True,None))   
            
            
        
    def on_size_toggled(self,widget,n):
        self.sizeBox.set_sensitive(widget.get_active())
    
    def on_author_toggled(self,widget,n):
        self.authorBox.set_sensitive(widget.get_active())
    
    def on_licence_toggled(self,widget,n):
        self.licenceBox.set_sensitive(widget.get_active())
        
    def on_font_toggled(self,widget,n):
        self.fontBox.set_sensitive(widget.get_active())
        
    def on_rename_toggled(self,widget,n):
        self.renameBox.set_sensitive(widget.get_active())
        
    def on_dir_toggled(self,widget,n):
        self.dirBox.set_sensitive(active)
        
    def on_return_clicked(self,widget):
        self.parent.switch_view(ManageProfileView(self.parent))
        
    def on_file_selected(self,widget):
        font = widget.get_filename()
        self.font = font
        
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
                    
        p = Profile()
        if self.elems["toggleSize"].get_active():
            w = self.elems["w"].get_text()
            h = self.elems["h"].get_text()
            ratio = self.elems["ratio"].get_active()
            p.size = (w,h,ratio)
        else:
            p.size = False
        if self.elems["toggleAuthor"].get_active() is not True:
            p.author == False
        else:
            p.author = self.elems["author"].get_text()
        if self.elems["toggleLicence"].get_active() is not True:
            p.licence == False
        else:
            p.licence = self.licenceChooser.get_active_text()
        if self.elems["toggleRename"].get_active() is not True:
            p.rename == False
        else:
            p.rename = (self.elems["prefixe"].get_text(),self.elems["suffixe"].get_text())
        if self.elems["toggleDir"].get_active() is not True:
            p.dir = False
        else:
            p.dir = True
        if self.elems["toggleFont"].get_active():
            p.font = self.font
        try:
            p.save(self.elems["name"].get_text())
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
        self.parent.switch_view(ManageProfileView(self.parent))
        

class ManageProfileView(view.View):
    """
        View to manage profile
    """
    
    def __init__(self,parent):
        view.View.__init__(self,"src/gui/glade/manageProfileView.glade","manageBox")
        
        self.profiles = self.builder.get_object("profileBox")
        self.model = Gtk.ListStore(str)
        for elem in get_profiles():
            self.model.append([elem])
        self.view = Gtk.TreeView(self.model)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(_("Profile name"), renderer, text=0)
        self.view.append_column(column)
        
        self.profiles.add(self.view)
        self.profiles.show_all()
        select = self.view.get_selection()
        select.connect("changed", self.on_profilesList_changed)
        
        self.butModify = self.builder.get_object("butModify")
        self.butDelete = self.builder.get_object("butDelete")

        self.parent = parent
        self.currentSelected = None
        
    def on_profilesList_changed(self,selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.butModify.set_sensitive(True)
            self.butDelete.set_sensitive(True)
            self.currentSelected = model[treeiter][0]
        else:
            self.butModify.set_sensitive(False)
            self.butDelete.set_sensitive(False)
            self.currentSelected = None
            
    def on_delete_clicked(self,widget):
        if self.currentSelected is None:
            return
        dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO, _("Confirm the action"))
        dialog.format_secondary_text(
            _("Are you sure to delete thie profile %s ?") % self.currentSelected)
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            model, treeiter = self.view.get_selection().get_selected()
            if del_profile(self.currentSelected) is not False:
                del self.model[treeiter]
            else:
                pass
        elif response == Gtk.ResponseType.NO:
            pass

        dialog.destroy()
        
    def on_new_clicked(self,widget):
        self.parent.switch_view(EditProfileView(self.parent,self))
    
    def on_modify_clicked(self,widget):
        self.parent.switch_view(EditProfileView(self.parent,self,self.currentSelected))
        
    def on_return_clicked(self,widget):
        self.parent.init_welcome_view()