# -*- coding: utf-8 -*-

import threading
import os
from time import sleep, time
from gettext import gettext as _

from gi.repository import GObject, Gdk, GLib

from src.settings import load_settings
from src.gui import view
from src import tools
from src import image

######
# Ce module est celui qui gère le traitement par lot des images
# Il dispose de deux classes : 
#  * Un thread qui, une fois lancé, fait les oppérations sur les images
#  * Une view qui permet d'afficher des informations à l'utilisateur
######

class RunningProcess(threading.Thread):
    
    def __init__(self,files,args,view):
        threading.Thread.__init__(self)
        
        self.setDaemon(True)
        self.compute = False
        self.files = files
        self.args = args
        self.view = view
        
    def run(self):
        PUBLIPHOTO_DIRNAME = load_settings().dirName
        i = 0
        self.must_stop = False
        self.compute = True
        t_start = time()
        n_finished = 0
        for path in self.files:
            self.view.update_progress(n_finished/len(self.files))
            n_finished += 1
            basename = os.path.basename(path)
            self.view.update_name(basename)
            self.view.update_action(_("Opening"))
            self.view.add_to_log(_("Working on")+" "+path)
            try:
                img = image.open_img(path)
            except Exception as e:
                self.view.add_to_log("  "+_("Unable to open file"))
                self.view.add_to_log((str)(e))
                continue
            if self.must_stop:
                break
            
            try:
                if self.args["size"] not in (False,None):
                    self.view.update_action(_("Resizing"))
                    x=self.args["size"][0]
                    if x == "": x = None
                    y=self.args["size"][1]
                    if y == "": y = None
                    self.view.add_to_log("  -- "+_("Resize in")+" "+(str)(x)+"x"+(str)(y),False)
                    if self.args["size"][2]:
                        self.view.add_to_log(" "+_("keeping ratio"))
                    else:
                        self.view.add_to_log(" "+_("without keeping ratio"))
                    img = image.resize_img(img,x,y,self.args["size"][2])
                    if self.must_stop:
                        break
            except Exception as e:
                self.view.add_to_log("  "+_("Unable to rename the picute"))
                self.view.add_to_log("  "+(str)(e))
                continue
            
            try:
                if self.args["author"] not in (False,None) or self.args["licence"] not in (False,None):
                    self.view.update_action(_("Adding label")+" ...")
                    label = ""
                    if self.args["author"] not in (False,None):
                        label += self.args["author"] + " "
                    if self.args["licence"] not in (False,None):
                        label += "© " + self.args["licence"]
                    self.view.add_to_log("  -- "+_("Adding label")+" : "+label)
                    img = image.draw_label(img,label,self.args["font"])
                    if self.must_stop:
                        break
            except Exception as e:
                self.view.add_to_log("  "+_("Unable to add the label"))
                self.view.add_to_log((str)(e))
                continue
                
            try:
                self.view.update_action(_("Saving")+" ...")
                if self.args["rename"] not in (False,None):
                    split = basename.split('.')
                    if self.args["rename"][2] != "": # Renomme le fichier
                        sans_ext = self.args["rename"][2]
                    else:
                        sans_ext = ".".join(split[:-1])
                    if len(split) < 2: # Ajout de l'extension jpeg si la photo n'en n'a pas
                        split.append("jpeg")
                    basename = self.args["rename"][0] + sans_ext + self.args["rename"][1] + "." + split[-1]
                    basename = basename.replace("%n", "{0:04d}".format(n_finished)) # format number with 4 digit 
                if self.args["dir"] is None:
                    dir = os.path.join(os.path.dirname(path),PUBLIPHOTO_DIRNAME)
                    if not os.path.exists(dir): os.makedirs(dir)
                elif self.args["dir"] is False:
                    dir = os.path.dirname(path)
                else:
                    dir = self.args["dir"]
                    
                new_path = os.path.join(dir,basename)
                self.view.add_to_log("  -- "+_("Saving as")+" : "+new_path)
                image.save_img(img,new_path)
                self.view.add_to_log("  -- "+_("Succes"))
            except Exception as e:
                self.view.add_to_log("  "+_("Unable to save the picture"))
                self.view.add_to_log((str)(e))
                continue
                
        self.view.update_progress(n_finished/len(self.files))    
        delta_t = (int)((time() - t_start)*100)
        delta_t /= 100
        self.view.add_to_log(_("Work done in %s seconde(s)") % (str)(delta_t))
        self.compute = False
        self.view.clear_action()
        self.view.finished()
            
    def ask_to_stop(self):
        self.must_stop = True
        
    def is_computing(self):
        return self.compute is True

            
class ProcessView(view.View):
    """
        ProcessView
    """
    
    def __init__(self,parent,files,args):
        view.View.__init__(self,"src/gui/glade/processView.glade","processBox")
        self.connect("destroy",self.on_destroy)
        
        self.nameLabel = self.builder.get_object("nameLabel")
        self.progressBar = self.builder.get_object("progressBar")
        self.oppBar = self.builder.get_object("oppBar")        
        self.logView = self.builder.get_object("logView")
        self.logBuffer = self.logView.get_buffer()
        self.finishedButton = self.builder.get_object("finishedButton")

        self.parent = parent
        self.thread = RunningProcess(files,args,self)
        GLib.idle_add(self.thread.start)
        
        GObject.timeout_add(80, self.action_pulse)
        
    def action_pulse(self):
        if self.thread.is_computing():
            self.oppBar.pulse()
        return True
    
    def add_to_log(self,text,newline=True):
        if newline:
            more="\n"
        else:
            more=""
        Gdk.threads_enter()
        self.logBuffer.insert_at_cursor(text+more)
        Gdk.threads_leave()
        
    def update_name(self,name):
        Gdk.threads_enter()
        self.nameLabel.set_text((str)(name))
        Gdk.threads_leave()
        
    def update_progress(self,fraction):
        Gdk.threads_enter()
        self.progressBar.set_fraction(fraction)
        Gdk.threads_leave()
        
    def update_action(self,action):
        Gdk.threads_enter()
        self.oppBar.set_text(action)
        Gdk.threads_leave()
        
    def clear_action(self):
        Gdk.threads_enter()
        self.oppBar.set_text(_("Finished"))
        self.oppBar.set_fraction(0)
        Gdk.threads_leave()
        
    def finished(self):
        Gdk.threads_enter()
        self.finishedButton.set_sensitive(True)
        Gdk.threads_leave()
        
    def on_destroy(self,widget):
        self.thread.ask_to_stop()
        self.thread.join(1)
        
    def on_stop_clicked(self,widget):
        self.thread.ask_to_stop()
        self.thread.join(1)
        self.parent.init_welcome_view()
        
    def on_quit_clicked(self,widget):
        self.on_destroy(widget)
        self.parent.on_destroy(self.parent)
        
        
    