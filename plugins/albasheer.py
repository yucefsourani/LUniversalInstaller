#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  albasheer.py
#  
#  Copyright 2021 youcef sourani <youssef.m.sourani@gmail.com>
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
from universalplugin.uplugin import BasePlugin, get_uniq_name,write_to_tmp
import subprocess
import os
from gi.repository import GLib



if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False,False]
if_all_true_skip     = [True,False]
                
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
category             = "<b>Other</b>"
category_icon_theme  = "applications-other"



class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="albasheer-128.png",
                            button_install_label="Install albasheer  (Flatpak User wide)",
                            button_remove_label="Remove albasheer (Flatpak User wide)",
                            buttontooltip="Install Remove albasheer (Flatpak User wide)",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove albasheer Failed",
                            ifinstallfailmsg="Install albasheer Failed",
                            ifinstallsucessmsg="Install albasheer Done",
                            ifremovesucessmsg="Remove albasheer Done",
                            beforeinstallyesorno="Start Install albasheer ?",
                            beforeremoveyesorno="Start Remove albasheer ?",
                            expand=False,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        self.package_name = "com.github.yucefsourani.albasheer-electronic-quran-browser"
        return not self.check_package(self.package_name)
        
    def install(self):
        if not self.check_repo("flathub"):
            if subprocess.call("flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo --user",shell=True) !=0:
                print("Add Flathub repo Failed.")
                return False
        
        if subprocess.call("flatpak --user install flathub {} -y".format(self.package_name),shell=True)==0:
            return True
        return False
        
    def remove(self):
        try:
            if subprocess.call("flatpak --user remove {} -y".format(self.package_name),stderr=subprocess.DEVNULL,shell=True)==0:
                return True
        except:
            if subprocess.call("pkexec flatpak  remove {} -y".format(self.package_name),stderr=subprocess.DEVNULL,shell=True)==0:
                return True
        return False
        
    def check_package(self,package_name):
        if subprocess.call("flatpak list  --app |grep {}".format(package_name),stderr=subprocess.DEVNULL,shell=True) == 0:
            return True
        return False

    def check_repo(self,repo_name):
        if subprocess.call("flatpak --user remote-list  |grep {}".format(repo_name),stderr=subprocess.DEVNULL,shell=True) == 0:
            return True
        return False
