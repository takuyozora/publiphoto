# -*- coding: utf-8 -*-

from gi.repository import Gtk,Gdk

from gettext import gettext as _

from src.tools import numbify
from src import tools
from src.config import LICENCES
from src.gui import view
from src.gui.process import ProcessView
from src import profile
import os

######
# Ce module est celui qui permet de sélectionner les images et les paramètres du traitement
# Il dispose de deux classes : 
#  * OpperationView se charge de récupérer les paramètres voules par l'utilisateur
#  * SelectPhotoView qui permet de choisir les photos à traiter
######

class OpperationView(view.View):
    """
        Profile view
         This is the main view of the programme
          Allow you to :
           * Connect to a profile host
           * See log
           * Switch to edit profile view
    """
    
    def __init__(self,parent,files):
        view.View.__init__(self,"src/gui/glade/oppView.glade","oppBox")
        
        self.profileBox = self.builder.get_object("profileBox")
        self.sizeBox = self.builder.get_object("sizeBox")
        self.authorBox = self.builder.get_object("authorBox")
        self.licenceBox = self.builder.get_object("licenceBox")
        self.renameBox = self.builder.get_object("renameBox")
        self.dirBox = self.builder.get_object("dirBox")
        
        self.elems = self.load_objects(["toggleSize","toggleAuthor","toggleLicence","toggleRename","toggleDir","h","w","ratio","author","prefixe","suffixe","dir","defaultDirLabel","newname"])
        numbify(self.elems['w'])
        numbify(self.elems['h'])

        self.licences = LICENCES
        self.licenceChooser = Gtk.ComboBoxText()
        for elem in self.licences:
            self.licenceChooser.append_text(elem)
        self.licenceChooser.set_entry_text_column(0)
        self.licenceChooser.set_id_column(0)
        self.licenceChooser.set_active_id(self.licences[0])
        self.licenceBox.pack_start(self.licenceChooser,False,False,0)
        self.licenceBox.show_all()
        
        profiles = profile.get_profiles()
        self.profileChooser = Gtk.ComboBoxText()
        self.profileChooser.set_entry_text_column(0)
        self.profileChooser.connect("changed",self.on_profile_changed)
        for elem in profiles:
            self.profileChooser.append_text(elem)
        self.profileBox.pack_start(self.profileChooser,False,False,0)
        self.profileBox.show_all()
        
        self.files = files
        self.parent = parent
        self.font = False
        
    def on_size_toggled(self,widget,n):
        self.sizeBox.set_sensitive(widget.get_active())
    
    def on_author_toggled(self,widget,n):
        self.authorBox.set_sensitive(widget.get_active())
    
    def on_licence_toggled(self,widget,n):
        self.licenceBox.set_sensitive(widget.get_active())
        
    def on_rename_toggled(self,widget,n):
        self.renameBox.set_sensitive(widget.get_active())
        
    def on_dir_toggled(self,widget,n):
        active = widget.get_active()
        self.dirBox.set_sensitive(active)
        active = active is True and self.elems["dir"].get_filename() is None
        self.elems["defaultDirLabel"].set_visible(active)
        
    def on_dir_selected(self,widget):
        self.elems["defaultDirLabel"].set_visible(False)
        
    def on_apply_clicked(self,widget):
        args={"size": None,"author": None,"licence":None,"rename":None,"dir":None,"font":None}
        if self.elems["toggleSize"].get_active() is not True:
            args["size"] = False
        else:
            args["size"] = (self.elems["w"].get_text(),self.elems["h"].get_text(),self.elems["ratio"].get_active())
        if self.elems["toggleAuthor"].get_active() is not True:
            args["author"] = False
        else:
            args["author"] = self.elems["author"].get_text()
        if self.elems["toggleLicence"].get_active() is not True:
            args["licence"] = False
        else:
            args["licence"] = self.licenceChooser.get_active_text()
        if self.elems["toggleRename"].get_active() is not True:
            args["rename"] = False
        else:
            args["rename"] = (self.elems["prefixe"].get_text(),self.elems["suffixe"].get_text(),self.elems["newname"].get_text())
        if self.elems["toggleDir"].get_active() is not True:
            args["dir"] = False
        else:
            args["dir"] = self.elems["dir"].get_filename()
        args["font"] = self.font
        #print(args)
            
        self.parent.switch_view(ProcessView(self.parent,self.files,args))
        
    def on_return_clicked(self,widget):
        self.parent.switch_view(SelectPhotoView(self.parent,self.files))
        
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
    
    def on_profile_changed(self,widget):
        p = profile.load_profile(widget.get_active_text())
        
        self.fill_with_profile(p)
            
        if p.font is not False:
            self.font = p.font

class SelectPhotoView(view.View):
    """
        Profile view
         This is the main view of the programme
          Allow you to :
           * Connect to a profile host
           * See log
           * Switch to edit profile view
    """
    
    def __init__(self,parent,files=[]):
        view.View.__init__(self,"src/gui/glade/selectPhotoView.glade","selectBox")
        
        self.files = tools.get_all_files(files)
        self.model = Gtk.ListStore(str)
        self.view = Gtk.TreeView(self.model)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(_("Files"), renderer, text=0)
        self.view.append_column(column)
        self.box  = self.builder.get_object("box")
        self.box.add(self.view)
        self.recreate_model()
        self.show_all()
        
        self.parent = parent

    def on_stop_clicked(self,widget):
        self.parent.init_welcome_view()
        
    def on_continue_clicked(self,widget):
        if len(self.files) < 1:
            dialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, _("Please, select at least one file to continue"))
            dialog.run()
    
            dialog.destroy()
            return
        self.parent.switch_view(OpperationView(self.parent,self.files))
            
    def recreate_model(self):
        self.model = Gtk.ListStore(str)
        for elem in self.files:
            self.model.append([os.path.basename(elem)])
        self.view.set_model(self.model)
        
    def on_change_clicked(self,widget):
        dialog = Gtk.FileChooserDialog(_("Select pictures to labelize"), self.parent,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_select_multiple(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            files = tools.from_uri_to_path(dialog.get_uris())
            self.files = tools.get_all_files(files)
            self.recreate_model()
        elif response == Gtk.ResponseType.CANCEL:
            pass

        dialog.destroy()
        


    
