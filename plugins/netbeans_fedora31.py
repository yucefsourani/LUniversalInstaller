#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  netbeans.py
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
from universalplugin.uplugin import BasePlugin, get_uniq_name,Yes_Or_No,write_to_tmp
import subprocess
import time
import os
from urllib import request
from gi.repository import GLib
import subprocess
import tempfile
import queue

if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False,False]
if_all_true_skip     = [True,False]
                
arch                 = ["all"]
distro_name          = ["fedora"]
distro_version       = ["31","32"]
category             = "<b>Developer Tools</b>"
category_icon_theme  = "applications-development"


location     = os.path.join(GLib.get_user_data_dir(),"netbeans")
all_package_to_install = ["java-1.8.0-openjdk", "java-latest-openjdk-devel", "java-latest-openjdk",  "java-1.8.0-openjdk-devel"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="NetBeans.png",
                            button_install_label="Install NetBeans 8.2",
                            button_remove_label="Remove NetBeans 8.2",
                            buttontooltip="Install Remove NetBeans 8.2",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove NetBeans 8.2 Failed",
                            ifinstallfailmsg="Install NetBeans 8.2 Failed",
                            ifinstallsucessmsg="Install NetBeans 8.2 Done",
                            ifremovesucessmsg="Remove NetBeans 8.2 Done",
                            beforeinstallyesorno="Start Install NetBeans 8.2 ?",
                            beforeremoveyesorno="Start Remove NetBeans 8.2 ?",
                            expand=False,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        check_package = all([self.check_package(pack) for pack in all_package_to_install])
        if not check_package:
            return True
        return not os.path.isfile("{}/bin/netbeans".format(location))
        
    def install(self):
        packs = [pack for pack in all_package_to_install if not self.check_package(pack)]
        if packs:
            packs = " ".join([pack for pack in packs])
            commands = ["dnf install {} --best -y".format(packs)]
            to_run = write_to_tmp(commands)
            if subprocess.call("pkexec bash  {}".format(to_run),shell=True)!=0:
                return False
            if os.path.isfile("{}/bin/netbeans".format(location)):
                return True

        link_pro     = "http://download.netbeans.org/netbeans/8.2/final/bundles/netbeans-8.2-linux.sh"
        try:
            os.makedirs(location,exist_ok=True)
        except:
            print("Makedir {} Failed.".format(location))
            return False
        pro_saveas = self.__download(link_pro,tempfile.gettempdir())
        if not pro_saveas:
            print("Download Failed.")
            return False
        
        if subprocess.call("chmod 755 {}".format(pro_saveas),shell=True)!=0:
            print("'chmod 755 {}' Failed.".format(pro_saveas))
            return False
        if subprocess.call("{} --silent \"-J-Dnb-base.installation.location={}\" \"-J-Dnb-base.jdk.location=/usr/lib/jvm/java-1.8.0-openjdk\"  ".format(pro_saveas,location),shell=True)!=0:
            print("Install To {} Failed.".format(location))
            return False

            
        return True
        
    def remove(self):
        if subprocess.call("chmod 755 {}/uninstall.sh".format(location),shell=True)!=0:
            print("'chmod 755 {}/uninstall.sh' Failed.".format(location))
            return False
            
        if subprocess.call("{}/uninstall.sh --silent".format(location),shell=True)!=0:
            print("'{}/uninstall.sh --silent' Failed.".format(location))
            return False

        return True


    def check_package(self,package_name):
        if subprocess.call("rpm -q {} &>/dev/null".format(package_name),shell=True) == 0:
            return True
        return False

    def __download(self,link,location):
        GLib.idle_add(self.__mainbox__.pack_start,self.__progressbar__,True,True,0)
        GLib.idle_add(self.__progressbar__.set_show_text,True)
        GLib.idle_add(self.__progressbar__.show)
        try:
            url   = request.Request(link,headers={"User-Agent":"Mozilla/5.0"})
            opurl = request.urlopen(url,timeout=10)
            try:
                saveas = opurl.headers["Content-Disposition"].split("=",1)[-1]
            except Exception as e:
                #print(e)
                saveas = os.path.basename(opurl.url)
            saveas = os.path.join(location,saveas)
            if os.path.isfile(saveas):
                q = queue.Queue()
                GLib.idle_add(self.yesorno__,"An older file with same location '{}' already exists, Remove it?".format(saveas),q)
                while q.empty():
                    pass
                if  q.get():
                    subprocess.call("rm -rf {}".format(saveas),shell=True)
            if  os.path.isfile(saveas):
                GLib.idle_add(self.__progressbar__.set_fraction,1.0)
                GLib.idle_add(self.__progressbar__.set_text,"{} Already Exists".format(saveas))
                GLib.idle_add(self.__mainbox__.remove,self.__progressbar__)
                return saveas
            else:
                size = int(opurl.headers["Content-Length"])
                psize = 0
                with open(saveas, 'wb') as op:
                    while True:
                        chunk = opurl.read(600)
                        if not chunk:
                            break
                        count = int((psize*100)//size)
                        fraction = count/100
                        op.write(chunk)
                        psize += 600
                        GLib.idle_add(self.__progressbar__.set_fraction,fraction)
                        GLib.idle_add(self.__progressbar__.set_text,"Downloading "+str(count)+"%")
            
                GLib.idle_add(self.__progressbar__.set_fraction,1.0)
                GLib.idle_add(self.__progressbar__.set_text,"Done")
        except Exception as e:
            print(e)
            GLib.idle_add(self.__progressbar__.set_fraction,0.0)
            GLib.idle_add(self.__progressbar__.set_text,"Fail")
            GLib.idle_add(self.__mainbox__.remove,self.__progressbar__)


            return False
        GLib.idle_add(self.__mainbox__.remove,self.__progressbar__)


        return saveas

    def yesorno__(self,msg,q):
        yesorno = Yes_Or_No(msg,q)
        yesorno.check()


        
        
