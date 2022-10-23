#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  codecs_fedora.py
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

all_package_to_remove = ['amrnb', 'gstreamer1-plugin-libav', 
                         'faad2', 
                         'gstreamer1-plugins-ugly', 'amrwb', 'xine-lib', 
                         'ffmpeg', 'gstreamer1-plugins-bad-freeworld', 
                         'xine-lib-devel', 'xine-lib-extras']

all_package_to_install = ['lame', 'gstreamer1-plugins-ugly', 
                          'gstreamer1-plugins-bad-free', 'xine-lib', 
                          'xine-lib-extras', 'x264', 'faad2', 'amrwb', 
                          'libdvdnav', 'gstreamer-plugin-crystalhd', 
                          'ffmpeg', 'gstreamer1-plugins-good', 'flac', 
                          'gstreamer-plugins-espeak', 'lame-libs', 
                          'libdvdread', 'gstreamer1-plugins-good-extras', 
                          'lsdvd', 'xine-lib-devel',
                          'amrnb', 'gstreamer1-plugin-libav', 'gstreamer1-plugins-bad-freeworld', 
                          'gstreamer1-vaapi', 'ffmpeg-libs', 'gstreamer1-plugins-bad-free-extras']

               
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False,False]
if_all_true_skip     = [True,False]
                
arch                 = ["all"]
distro_name          = ["fedora"]
distro_version       = ["31","32","33","34","35","36","37"]
category             = "<b>Multimedia</b>"
category_icon_theme  = "applications-multimedia"


class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="codecs.png",
                            button_install_label="Install Codecs",
                            button_remove_label="Remove Codecs",
                            buttontooltip="Install Remove Codecs",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            daemon=True,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifinstallfailmsg="Install Codecs Failed",
                            ifremovefailmsg="Remove Codecs Failed",
                            expand=False)


        
        
    def check(self):
        check_package = all([self.check_package(pack) for pack in all_package_to_install])
        return not check_package
        
    def install(self):
        rpmfusion  = all([ self.check_package(pack) for pack in ["rpmfusion-nonfree-release", "rpmfusion-free-release"]])
        to_install = [pack for pack in all_package_to_install if not self.check_package(pack)]
        to_install = " ".join(to_install)
        commands = ["dnf install {} -y --best".format(to_install)]
        if not rpmfusion:
            d_version = self.get_distro_version()
            command_to_install_rpmfusion = "dnf install  --best -y --nogpgcheck  \
    http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-{}.noarch.rpm \
    http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{}.noarch.rpm".format(d_version,d_version)
            commands.insert(0,command_to_install_rpmfusion)
        to_run = write_to_tmp(commands)

        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)==0:
            return True
        return False
        
    def remove(self):
        to_remove = " ".join([pack for pack in all_package_to_remove if self.check_package(pack)])
        if subprocess.call("pkexec rpm -v --nodeps -e {}".format(to_remove),shell=True)==0:
            return True
        return False

    def check_package(self,package_name):
        if subprocess.call("rpm -q {} &>/dev/null".format(package_name),shell=True) == 0:
            return True
        return False
        
    def get_distro_version(self):
        result=""
        if not os.path.isfile("/etc/os-release"):
            return None
        with open("/etc/os-release") as myfile:
            for l in myfile:
                if l.startswith("VERSION_ID"):
                    result=l.split("=",1)[1].strip()
        return result.replace("\"","").replace("'","")
