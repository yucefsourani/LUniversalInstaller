#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  uplugin.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, GLib, GdkPixbuf, Pango
import threading
import os
from string import punctuation
import queue

appname        = "luniversalinstaller"
image_loction  = [l for l in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"images"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../../images".format(appname))] if os.path.isdir(l)]
def get_image_location(image_name):
    if image_loction:
        for i in image_loction:
            location = os.path.join(i,image_name)
            if os.path.isfile(location):
                return location
    return False

class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,q,parent=None):
        Gtk.MessageDialog.__init__(self,parent,flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL,message_format=msg,use_markup=True)
        self.q  = q
        self.parent=parent
        if self.parent != None:
            self.set_transient_for(self.parent)
            self.set_modal(True)
            self.parent.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)

        
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            if self.parent != None:
                self.parent.set_sensitive(True)
            self.destroy()
            self.q.put(True)
            return True
        else:
            if self.parent != None:
                self.parent.set_sensitive(True)
            self.destroy()
            self.q.put(False)
            return False


class NInfo(Gtk.MessageDialog):
    def __init__(self,message,parent=None):
        Gtk.MessageDialog.__init__(self,parent,1,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,message,use_markup=True)
        self.parent=parent
        if self.parent != None:
            self.set_transient_for(self.parent)
            self.set_modal(True)
            self.parent.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
        self.get_message_area().get_children()[0].set_selectable(True)
    def start(self):
        self.run() 
        if self.parent != None:
            self.parent.set_sensitive(True)
        self.destroy()
        return False



class ThreadCheck(threading.Thread):
    def __init__(self,func_check,label,
               button_remove_label,button_install_label,
               spinner,button,loadingmsg):
        threading.Thread.__init__(self)
        self.func_check           = func_check
        self.label                = label
        self.button_remove_label  = button_remove_label
        self.button_install_label = button_install_label
        self.spinner              = spinner
        self.button               = button
        self.loadingmsg           = loadingmsg

    def run(self):
        GLib.idle_add(self.label.set_markup,self.loadingmsg)
        GLib.idle_add(self.button.set_sensitive,False)
        GLib.idle_add(self.spinner.start)
        if self.func_check():
            GLib.idle_add(self.label.set_markup,self.button_install_label)
        else:
            GLib.idle_add(self.label.set_markup,self.button_remove_label)
        
        GLib.idle_add(self.button.set_sensitive,True)
        GLib.idle_add(self.spinner.stop)


        
class ThreadCheckInstallRemove(threading.Thread):
    def __init__(self,func_check,func_install,func_remove,label,
               button_remove_label,button_install_label,parent,
               spinner,blockparent,waitmsg,runningmsg,
               ifinstallfailmsg,ifremovefailmsg,
               ifinstallsucessmsg,ifremovesucessmsg,
               beforeinstallyesorno,beforeremoveyesorno):
                   
        threading.Thread.__init__(self)
        self.func_check           = func_check
        self.func_install         = func_install
        self.func_remove          = func_remove
        self.label                = label
        self.button_remove_label  = button_remove_label
        self.button_install_label = button_install_label
        self.parent               = parent
        self.spinner              = spinner
        self.blockparent          = blockparent
        self.waitmsg              = waitmsg
        self.runningmsg           = runningmsg
        self.ifinstallfailmsg     = ifinstallfailmsg
        self.ifremovefailmsg      = ifremovefailmsg
        self.ifinstallsucessmsg   = ifinstallsucessmsg
        self.ifremovesucessmsg    = ifremovesucessmsg
        self.beforeinstallyesorno = beforeinstallyesorno
        self.beforeremoveyesorno  = beforeremoveyesorno

    def info__(self,msg):
        msg = NInfo(msg,self.parent)
        msg.start()

    def yesorno__(self,msg,q):
        yesorno = Yes_Or_No(msg,q,self.parent)
        yesorno.check()
        
    def run(self):
        if self.blockparent:
            GLib.idle_add(self.parent.set_sensitive,False)
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self.label.set_markup,self.waitmsg)
        
        if self.func_check():
            if self.beforeinstallyesorno:
                q = queue.Queue()
                GLib.idle_add(self.yesorno__,self.beforeinstallyesorno,q)
                while q.empty():
                    pass
                if not q.get():
                    del q
                    GLib.idle_add(self.label.set_markup,self.button_install_label)
                    if self.blockparent:
                        GLib.idle_add(self.parent.set_sensitive,True)
                        GLib.idle_add(self.spinner.stop)
                    return

            GLib.idle_add(self.label.set_markup,self.runningmsg)
            check_install = self.func_install()
            if check_install:
                GLib.idle_add(self.label.set_markup,self.button_remove_label)
                if self.ifinstallsucessmsg:
                    GLib.idle_add(self.info__,self.ifinstallsucessmsg)
            else:
                GLib.idle_add(self.label.set_markup,self.button_install_label)
                if self.ifinstallfailmsg:
                    GLib.idle_add(self.info__,self.ifinstallfailmsg)
        else:
            if self.beforeremoveyesorno:
                q = queue.Queue()
                GLib.idle_add(self.yesorno__,self.beforeremoveyesorno,q)
                while q.empty():
                    pass

                if not q.get():
                    del q
                    GLib.idle_add(self.label.set_markup,self.button_remove_label)
                    if self.blockparent:
                        GLib.idle_add(self.parent.set_sensitive,True)
                        GLib.idle_add(self.spinner.stop)
                    return

            GLib.idle_add(self.label.set_markup,self.runningmsg)
            check_remove = self.func_remove()
            if check_remove:
                GLib.idle_add(self.label.set_markup,self.button_install_label)
                if self.ifremovesucessmsg:
                    GLib.idle_add(self.info__,self.ifremovesucessmsg)
            else:
                GLib.idle_add(self.label.set_markup,self.button_remove_label)
                if self.ifremovefailmsg:
                    GLib.idle_add(self.info__,self.ifremovefailmsg)
        if self.blockparent:
            GLib.idle_add(self.parent.set_sensitive,True)
        GLib.idle_add(self.spinner.stop)

        


class BasePlugin(Gtk.Grid):
    def __init__(self,parent,spacing=2,margin=10,button_image="",button_install_label="Install",
                button_remove_label="Remove",
                buttontooltip="Test tooltip",
                buttonsizewidth=100,
                buttonsizeheight=100,
                button_relief=2,
                blockparent=True,
                waitmsg="Wait...",
                runningmsg="Running...",
                loadingmsg="Loading...",
                ifinstallfailmsg="",
                ifremovefailmsg="",
                ifinstallsucessmsg="",
                ifremovesucessmsg="",
                beforeinstallyesorno="",
                beforeremoveyesorno="",
                expand=False):
        Gtk.Grid.__init__(self,margin=margin,expand=expand)
        
        self.parent               = parent
        self.spacing              = spacing
        self.button_image         = button_image
        self.button_install_label = button_install_label
        self.button_remove_label  = button_remove_label
        self.buttontooltip        = buttontooltip
        self.buttonsizewidth      = buttonsizewidth
        self.buttonsizeheight     = buttonsizeheight
        self.button_relief        = button_relief
        self.blockparent          = blockparent
        self.waitmsg              = waitmsg
        self.runningmsg           = runningmsg
        self.loadingmsg           = loadingmsg
        self.ifinstallfailmsg     = ifinstallfailmsg
        self.ifremovefailmsg      = ifremovefailmsg
        self.ifinstallsucessmsg   = ifinstallsucessmsg
        self.ifremovesucessmsg    = ifremovesucessmsg
        self.beforeinstallyesorno = beforeinstallyesorno
        self.beforeremoveyesorno  = beforeremoveyesorno


        self.mainbox              = Gtk.VBox(spacing=self.spacing)
        
        self.__button__           = Gtk.Button(always_show_image=True,relief=Gtk.ReliefStyle(self.button_relief))
        self.__button__.connect("clicked",self.clicked)
        try:
            pixbuf=GdkPixbuf.Pixbuf.new_from_file_at_size(get_image_location(self.button_image),self.buttonsizewidth,self.buttonsizeheight)
        except Exception as e:
            print(e)
            try:
                pixbuf = Gtk.IconTheme.get_default().load_icon(self.button_image,self.buttonsizewidth, Gtk.IconLookupFlags.FORCE_SIZE)
            except:
                #failback
                pixbuf = Gtk.IconTheme.get_default().load_icon("applications-accessories",self.buttonsizewidth, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.__button__.add(image)
        if self.buttontooltip:
            self.__button__.set_tooltip_markup(self.buttontooltip)
    

        self.__spinner__          = Gtk.Spinner()
        
        
        self.__label__            = Gtk.Label(use_markup=True)
        self.__label__.set_line_wrap(True)
        self.__label__.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        self.__label__.set_max_width_chars(14)
        self.__label__.set_justify(Gtk.Justification.CENTER)
        ThreadCheck(self.check,self.__label__,
                    self.button_remove_label,
                    self.button_install_label,
                    self.__spinner__,
                    self.__button__,
                    self.loadingmsg).start()
        
    
        self.mainbox.pack_start(self.__button__,True,True,0)
        self.mainbox.pack_start(self.__label__,True,True,0)
        self.mainbox.pack_start(self.__spinner__,True,True,0)
        self.add(self.mainbox)

        
        
    def clicked(self,button):
        ThreadCheckInstallRemove(func_check=self.check,
        func_install=self.install,
        func_remove=self.remove,
        label=self.__label__,
        button_remove_label=self.button_remove_label,
        button_install_label=self.button_install_label,
        parent=self.parent,
        spinner=self.__spinner__,
        blockparent=self.blockparent,
        waitmsg=self.waitmsg,
        runningmsg=self.runningmsg,
        ifinstallfailmsg=self.ifinstallfailmsg,
        ifremovefailmsg=self.ifremovefailmsg,
        ifinstallsucessmsg=self.ifinstallsucessmsg,
        ifremovesucessmsg=self.ifremovesucessmsg,
        beforeinstallyesorno=self.beforeinstallyesorno,
        beforeremoveyesorno=self.beforeremoveyesorno
        ).start()

def get_uniq_name(name):
    name = name.replace(" ","")
    return "".join([char for char in name if char not in punctuation])
