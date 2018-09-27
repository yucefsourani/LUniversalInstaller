#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  flash_player_fedora.py
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
from universalplugin.uplugin import BasePlugin, get_uniq_name, write_to_tmp
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
category             = "<b>Internet</b>"
category_icon_theme  = "applications-internet"

arch = os.uname().machine

if arch=="x86_64":
    command_install = ["rpm -ivh http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm", "rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux"]
    repo_package    = "adobe-release-x86_64"
else:
    command_install = ["rpm -ivh http://linuxdownload.adobe.com/adobe-release/adobe-release-i386-1.0-1.noarch.rpm", "rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux"]
    repo_package    = "adobe-release-i386"
    
class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="Adobe-Flash-250x250.png",
                            button_install_label="Install Flash Player",
                            button_remove_label="Remove Flash Player",
                            buttontooltip="Install Remove Flash Player",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            daemon=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Flash Player Failed",
                            ifremovefailmsg="Remove Flash Player Failed",
                            expand=False)


    def check(self):
        return not self.check_package("flash-plugin")
        
    def install(self):
        if  self.check_package(repo_package):
            commands = ["dnf install flash-plugin -y --best"]
        else:
            commands = command_install + ["dnf install flash-plugin -y --best"]

        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        if subprocess.call("pkexec rpm --nodeps -e flash-plugin",shell=True)==0:
            return True
        return False

    def check_package(self,package_name):
        if subprocess.call("rpm -q {} &>/dev/null".format(package_name),shell=True) == 0:
            return True
        return False
