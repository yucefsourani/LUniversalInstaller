#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  teamviewer_fedora.py
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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  xdm.py
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
from universalplugin.uplugin import BasePlugin, get_uniq_name,write_to_tmp
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





class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="Team_Viewer.png",
                            button_install_label="Install TeamViewer",
                            button_remove_label="Remove TeamViewer",
                            buttontooltip="Install Remove TeamViewer",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove TeamViewer Failed",
                            ifinstallfailmsg="Install TeamViewer Failed",
                            ifinstallsucessmsg="Install TeamViewer Done",
                            ifremovesucessmsg="Remove TeamViewer Done",
                            beforeinstallyesorno="Start Install TeamViewer ?",
                            beforeremoveyesorno="Start Remove TeamViewer ?",
                            expand=False,
                            daemon=False)


        
    def check(self):
        return not self.check_package("teamviewer")
        
    def install(self):
        arch = os.uname().machine
        if arch=="x86_64":
            link_pro = "https://download.teamviewer.com/download/linux/teamviewer.x86_64.rpm"
        else:
            link_pro = "https://download.teamviewer.com/download/linux/teamviewer.i686.rpm"

        if subprocess.call("pkexec dnf install {} -y --best -v".format(link_pro),shell=True)!=0:
            return False

        return True
        
    def remove(self):
        if subprocess.call("pkexec rpm -v --nodeps -e teamviewer",shell=True)!=0:
            return False
        return True

    def check_package(self,package_name):
        if subprocess.call("rpm -q {} &>/dev/null".format(package_name),shell=True) == 0:
            return True
        return False
