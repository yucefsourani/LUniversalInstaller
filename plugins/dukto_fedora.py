#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  example_plugin.py
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
from universalplugin.uplugin import BasePlugin, write_to_tmp
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
category             = "<b>Utils</b>"
category_icon_theme  = "preferences-other"

class Plugin(BasePlugin):
    __gtype_name__ = "__installremovedukto__" #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="dukto.png",
                            button_install_label="Install Dukto",
                            button_remove_label="Remove Dukto",
                            buttontooltip="Install Remove Dukto",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            daemon=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            expand=False)


    def check(self):
        return not os.path.isfile("/usr/bin/dukto")
        
    def install(self):
        if os.path.isfile("/etc/yum.repos.d/home:colomboem.repo"):
            commands = ["dnf install dukto -y --best"]
        else:
            commands = ["dnf config-manager --add-repo https://download.opensuse.org/repositories/home:colomboem/RHEL_7/home:colomboem.repo",
            "dnf install dukto -y --best"]
        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e dukto",shell=True)==0:
            return True
        return False

