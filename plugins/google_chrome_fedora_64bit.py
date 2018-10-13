#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  google_chrome_fedora_64bit.py
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
from universalplugin.uplugin import BasePlugin, write_to_tmp, get_uniq_name
import subprocess
import time
import os

if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False,False]
if_all_true_skip     = [True,False]
                
arch                 = ["x86_64"]
distro_name          = ["fedora"]
distro_version       = ["all"]
category             = "<b>Internet</b>"
category_icon_theme  = "applications-internet"

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="Chrome.png",
                            button_install_label="Install Google Chrome",
                            button_remove_label="Remove Google Chrome",
                            buttontooltip="Install Remove Google Chrome",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Google Chrome Failed",
                            ifremovefailmsg="Remove Google Chrome Failed",
                            expand=False)


    def check(self):
        return not os.path.isfile("/usr/bin/google-chrome")
        
    def install(self):
        if os.path.isfile("/etc/yum.repos.d/google-chrome.repo"):
            commands = ["dnf config-manager --set-enabled google-chrome","dnf install google-chrome-stable -y --best"]
        else:
            commands = ["echo -e '[google-chrome]\nname=google-chrome\nbaseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64\nenabled=1\ngpgcheck=1\ngpgkey=https://dl.google.com/linux/linux_signing_key.pub' > /etc/yum.repos.d/google-chrome.repo",
            "dnf config-manager --set-enabled google-chrome",
            "dnf install google-chrome-stable -y --best"]
        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e google-chrome-stable",shell=True)==0:
            return True
        return False

