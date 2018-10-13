#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  geany_fedora.py
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
from universalplugin.uplugin import BasePlugin, get_uniq_name
import subprocess
import time
import os

if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False,False]
if_all_true_skip     = [True,False]
                
arch                 = ["all"]
distro_name          = ["fedora"]
distro_version       = ["all"]
category             = "<b>Developer Tools</b>"
category_icon_theme  = "applications-development"

all_package = ["geany-themes","geany","geany-libgeany","xterm"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="geany.png",
                            button_install_label="Install Geany",
                            button_remove_label="Remove Geany",
                            buttontooltip="A fast and lightweight IDE using GTK3",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Geany Failed",
                            ifremovefailmsg="Remove Geany Failed",
                            expand=False)


    def check(self):
        check_package = all([self.check_package(pack) for pack in ["geany","geany-libgeany"]])
        return not check_package     
         
    def install(self):
        to_install = [pack for pack in all_package if not self.check_package(pack)]
        to_install = " ".join(to_install)
        if subprocess.call("pkexec dnf install {} -y --best".format(to_install),shell=True)==0:
            return True
        return False
        
    def remove(self):
        to_remove = " ".join([pack for pack in ["geany","geany-libgeany"] if self.check_package(pack)])
        if subprocess.call("pkexec rpm -v --nodeps -e {}".format(to_remove),shell=True)==0:
            return True
        return False

    def check_package(self,package_name):
        if subprocess.call("rpm -q {} &>/dev/null".format(package_name),shell=True) == 0:
            return True
        return False
        
