#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dnf_keepcache.py
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
import os

if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False,False]
if_all_true_skip     = [True,False]
                
arch                 = ["all"]
distro_name          = ["fedora"]
distro_version       = ["all"]
category             = "<b>Utils</b>"
category_icon_theme  = "preferences-other"


true  = ["True", "true", "1"]
false = ["False", "false", "0"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="rpm.svg",
                            button_install_label="Dnf Enable keepcache",
                            button_remove_label="Dnf Disable keepcache",
                            buttontooltip="Enable Disable keepcache",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            expand=False)


    def check(self):
        check = subprocess.check_output("dnf config-manager --dump | grep keepcache |cut -f2- -d \"=\"",shell=True).strip().decode("utf-8")
        if check in true:
            return False
        return True

        
    def install(self):
        if subprocess.call("pkexec dnf config-manager --setopt=keepcache=True --save",shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec dnf config-manager --setopt=keepcache=False --save",shell=True)==0:
            return True
        return False

