#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  intellij_idea.py
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
import hashlib
import json

if_true_skip         = False
try:
    from bs4 import BeautifulSoup
    if_false_skip   = True
except Exception as e:
    print(e)
    if_false_skip    = False
if_one_true_skip     = [False,False]
if_all_true_skip     = [True,False]
                
arch                 = ["all"]
distro_name          = ["fedora"]
distro_version       = ["all"]
category             = "<b>Developer Tools</b>"
category_icon_theme  = "applications-development"


location             = os.path.join(GLib.get_user_data_dir(),"IntelliJIDEA")
location_bin         = os.path.join(GLib.get_home_dir(),".local","bin")
exec_filename        = "idea.sh"
code_name            = "IIC"
edesktop_file_name   = "intellijidea.desktop"
icon_filename        = "idea.png"


all_package_to_install = ["java-1.8.0-openjdk","java-openjdk","java-1.8.0-openjdk-devel","java-openjdk-devel"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="idea.png",
                            button_install_label="Install IntelliJ IDEA Community",
                            button_remove_label="Remove IntelliJ IDEA Community",
                            buttontooltip="Install Remove IntelliJ IDEA Community",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove IntelliJ IDEA Community Failed",
                            ifinstallfailmsg="Install IntelliJ IDEA Community Failed",
                            ifinstallsucessmsg="Install IntelliJ IDEA Community Done",
                            ifremovesucessmsg="Remove IntelliJ IDEA Community Done",
                            beforeinstallyesorno="Start Install IntelliJ IDEA Community ?",
                            beforeremoveyesorno="Start Remove IntelliJ IDEA Community ?",
                            expand=False,
                            daemon=False)

        self.parent = parent
        
    def check(self):
        return not (os.path.isfile(os.path.join(location,"bin",exec_filename)) and os.path.isfile(os.path.join(location_bin,exec_filename)))
        
    def install(self):
        temp = tempfile.gettempdir()
        link_pro,checksumlink = self.__get_downlaod_link(code=code_name)
        if not link_pro:
            print("Get Download Link Failed.")
            return False
            
        try:
            os.makedirs(location,exist_ok=True)
        except:
            print("Makedir {} Failed.".format(location))
            return False
            
        pro_saveas = self.__download(link_pro,temp)
        if not pro_saveas:
            print("Download Failed.")
            return False
            
        if not self.check_sum(pro_saveas,checksumlink):
            print("Check sha256 Failed Redownload .")
            return False
        
            
        if subprocess.call("tar --strip=1 -xvzf {} -C {}".format(pro_saveas,location),shell=True) != 0:
            print("'tar -xvzf {} -C {}' Failed.".format(pro_saveas,location))
            return False

        try:
            os.makedirs(location_bin,exist_ok=True)
        except Exception as e:
            print(e)
            return False
        
        subprocess.call("chmod 755 {}".format(os.path.join(location,"bin",exec_filename)),shell=True)
        if subprocess.call("ln -sf {} {}".format(os.path.join(location,"bin",exec_filename),os.path.join(location_bin,exec_filename)),shell=True)!=0:
            print("'ln -sf {} {}' Failed.".format(os.path.join(location,"bin",exec_filename),os.path.join(location_bin,exec_filename)))
            return False
        
        
        application_location = os.path.join(GLib.get_user_data_dir(),"applications",edesktop_file_name)
        to_write_desktop = """[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Terminal=false
Exec={}
Icon={}
Name=IntelliJ IDEA Community
Comment=IntelliJ IDEA Community
Categories=ActiveState;Application;Development;Editor;Utility;TextEditor;
""".format(os.path.join(location_bin,exec_filename),os.path.join(location,"bin",icon_filename))

        try:
            with open(application_location,"w") as mf:
                mf.write(to_write_desktop)
        except:
            return False
        return True

    def check_sum(self,pro_saveas,checksumlink):
        try:
            url    = request.Request(checksumlink,headers={"User-Agent":"Mozilla/5.0"})
            opurl  = request.urlopen(url,timeout=10)
            sha256 =  opurl.read().decode("utf-8").strip().split()[0]
        except Exception as e:
            print(e)
            return False
            
        sha = hashlib.sha256()
        with open(pro_saveas, 'rb') as f:
            while True:
                data = f.read(1024 * 1024 * 32)
                if not data:
                    break
                sha.update(data)

        if sha.hexdigest().lower()!=sha256.lower():
            return False
        return True
        
    def remove(self):
        if subprocess.call("rm -rf {}".format(location),shell=True)!=0:
            print("'rm -rf {}' Failed.".format(location))
            return False
        
        application_location = os.path.join(GLib.get_user_data_dir(),"applications",edesktop_file_name)
        subprocess.call("rm -f {}".format(application_location),shell=True)
        subprocess.call("rm -rf {}".format(os.path.join(location_bin,exec_filename)),shell=True)
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
            if  os.path.isfile("/etc/fedora-release"):
                packs = [pack for pack in all_package_to_install if not self.check_package(pack)]
                if packs:
                    packs = " ".join([pack for pack in packs])
                    commands = ["dnf install {} --best -y".format(packs)]
                    to_run = write_to_tmp(commands)
                    if subprocess.call("pkexec bash  {}".format(to_run),shell=True)!=0:
                        GLib.idle_add(self.__progressbar__.set_fraction,0.0)
                        GLib.idle_add(self.__progressbar__.set_text,"Fail")
                        GLib.idle_add(self.__mainbox__.remove,self.__progressbar__)
                        return False
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

        
    def __get_downlaod_link(self,code):
        url = request.Request("https://data.services.jetbrains.com/products",headers={"User-Agent":"Mozilla/5.0"})
        try:
            with request.urlopen(url) as response:
                body = json.loads(response.read().decode('utf-8'))
                for info in body:
                    if code in info["code"]:
                        for i in info["releases"]:
                            if isinstance(i,dict):
                                if "version" in i.keys() and "downloads" in i.keys():
                                    if i["type"]=="release":
                                        try:
                                            info__ = [i["downloads"]["linux"]["link"], i["downloads"]["linux"]["checksumLink"]]
                                            return info__
                                        except:
                                            continue
                    
        except Exception as e:
            print(e)
            return False

        return False

