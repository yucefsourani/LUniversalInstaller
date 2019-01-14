#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  komodo_fedora.py
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


location     = os.path.join(GLib.get_user_data_dir(),"komodo")
location_bin = os.path.join(GLib.get_home_dir(),".local","bin")
all_package_to_install = ["gtk+", "glib2", "pango", "libstdc++", "gdk-pixbuf2",\
"libgnome", "libgnomeui", "scim", "scim-gtk", "scim-bridge-qt3"]

class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="komodo48.png",
                            button_install_label="Install Komodo",
                            button_remove_label="Remove Komodo",
                            buttontooltip="Install Komodo",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove Komodo Failed",
                            ifinstallfailmsg="Install Komodo Failed",
                            ifinstallsucessmsg="Install Komodo Done",
                            ifremovesucessmsg="Remove Komodo Done",
                            beforeinstallyesorno="Start Install Komodo ?",
                            beforeremoveyesorno="Start Remove Komodo ?",
                            expand=False,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        check_package = all([self.check_package(pack) for pack in all_package_to_install])
        if not check_package:
            return True
        return not (os.path.isfile(os.path.join(location,"bin","komodo")) and os.path.isfile(os.path.join(location_bin,"komodo")))
        
    def install(self):
        temp = tempfile.gettempdir()
        packs = [pack for pack in all_package_to_install if not self.check_package(pack)]
        if packs:
            packs = " ".join([pack for pack in packs])
            commands = ["dnf install {} --best -y".format(packs)]
            to_run = write_to_tmp(commands)
            if subprocess.call("pkexec bash  {}".format(to_run),shell=True)!=0:
                return False
            if os.path.isfile(os.path.join(location,"bin","komodo")) and os.path.isfile(os.path.join(location_bin,"komodo")):
                return True

        link_pro = self.get_komodo_downlaod_link()
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
        if subprocess.call("tar -xvzf {} -C {}".format(pro_saveas,temp),shell=True) != 0:
            print("'tar -xvzf {} -C {}' Failed.".format(pro_saveas,temp))
            return False
        folder_name = os.path.basename(pro_saveas).rsplit(".",2)[0]
        install_file_location = os.path.join(temp,folder_name)
        old_cwd = os.getcwd()
        os.chdir(install_file_location)
        if subprocess.call("chmod 755 install.sh",shell=True)!=0:
            print("'chmod 755 install.sh' Failed.")
            os.chdir(old_cwd)
            return False
        if subprocess.call("./install.sh -I {}".format(location),shell=True) != 0 :
            print("Install To {} Failed.".format(location))
            os.chdir(old_cwd)
            return False
        os.chdir(old_cwd)
        try:
            os.makedirs(location_bin,exist_ok=True)
        except Exception as e:
            print(e)
            return False
        if subprocess.call("ln -sf {} {}".format(os.path.join(location,"bin","komodo"),os.path.join(location_bin,"komodo")),shell=True)!=0:
            print("'ln -sf {} {}' Failed.".format(os.path.join(location,"bin","komodo"),os.path.join(location_bin,"komodo")))
            return False
            
        return True
        
    def remove(self):
        if subprocess.call("rm -rf {}".format(location),shell=True)!=0:
            print("'rm -rf {}' Failed.".format(location))
            return False
        
        application_location = os.path.join(GLib.get_user_data_dir(),"applications")
        if subprocess.call("rm -f {}/komodo-edit*".format(application_location),shell=True)!=0:
            print("Remove Desktop Entry From {} Failed.".format(application_location))
            return False
            
        if subprocess.call("rm -rf {}".format(os.path.join(location_bin,"komodo")),shell=True)!=0:
            print("'rm -rf {}' Failed.".format(os.path.join(location_bin,"komodo")))
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

        
    def get_komodo_downlaod_link(self):
        if os.uname().machine == "x86_64":
            download_arch = "linuxx86_64"
        else:
            download_arch = "linuxx86"
        
        url = request.Request("https://www.activestate.com/komodo-ide/downloads/edit",headers={"User-Agent":"Mozilla/5.0"})
        try:
            htmldoc = request.urlopen(url,timeout=10)
        except Exception as e:
            print(e)
            return False
        soup = BeautifulSoup(htmldoc.read(),"html.parser")
        for tag in soup.findAll("td",{"class":"dl_link"}):
            try:
                l = tag.a.attrs["href"]
                if download_arch=="linuxx86_64":
                    if l.endswith("linux-x86_64.tar.gz"):
                        return l.split("=",1)[-1]
                elif download_arch=="linuxx86":
                    if l.endswith("linux-x86.tar.gz"):
                        return l.split("=",1)[-1]
            except Exception as e:
                print(e)
                continue
        return False
