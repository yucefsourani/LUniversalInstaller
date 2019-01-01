#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  4kdownload.py
#  
#  Copyright 2019 youcef sourani <youssef.m.sourani@gmail.com>
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
                
arch                 = ["x86_64"]
distro_name          = ["all"]
distro_version       = ["all"]
category             = "<b>Internet</b>"
category_icon_theme  = "applications-internet"





class Plugin(BasePlugin):
    __gtype_name__ = get_uniq_name(__file__) #uniq name and no space
    def __init__(self,parent):
        BasePlugin.__init__(self,parent=parent,
                            spacing=2,
                            margin=10,
                            button_image="videodownloader.b9996289c0e2.svg",
                            button_install_label="Install 4kvideodownloader",
                            button_remove_label="Remove 4kvideodownloader",
                            buttontooltip="Install Remove 4kvideodownloader",
                            buttonsizewidth=100,
                            buttonsizeheight=100,
                            button_relief=2,
                            blockparent=False,
                            waitmsg="Wait...",
                            runningmsg="Running...",
                            loadingmsg="Loading...",
                            ifremovefailmsg="Remove 4kvideodownloader Failed",
                            ifinstallfailmsg="Install 4kvideodownloader Failed",
                            ifinstallsucessmsg="Install 4kvideodownloader Done",
                            ifremovesucessmsg="Remove 4kvideodownloader Done",
                            beforeinstallyesorno="Start Install 4kvideodownloader ?",
                            beforeremoveyesorno="Start Remove 4kvideodownloader ?",
                            expand=False,
                            daemon=True)

        self.parent = parent
        
    def check(self):
        return not os.path.isdir("/opt/4kvideodownloader")
        
    def install(self):
        temp = tempfile.gettempdir()
        link_pro  = "https://dl.4kdownload.com/app/4kvideodownloader_4.4.11_amd64.tar.bz2"
        link_icon = "https://static.4kdownload.com/main/img/redesign/videodownloader.b9996289c0e2.svg"


        pro_saveas = self.__download(link_pro,temp)
        if not pro_saveas:
            print("Download Failed.")
            return False
        icon_saveas = self.__download(link_icon,temp)
        if not icon_saveas:
            print("Download Failed.")
            return False
        old_dir = os.getcwd()
        os.chdir(temp)
        if subprocess.call("tar jxf {}".format(pro_saveas),shell=True)!=0:
            print("Extract {} Failed.".format(pro_saveas))
            os.chdir(old_dir)
            return False
        os.chdir(old_dir)
        folder_files = os.path.join(temp,"4kvideodownloader")
        desktop_file = os.path.join(temp,"4kvideodownloader.desktop")
        desktop_to_write = """[Desktop Entry]
Encoding=UTF-8
Name=4kvideodownloader
GenericName=youtube
Comment=Start 4kvideodownloader
Exec=/opt/4kvideodownloader/4kvideodownloader.sh
Icon={}
Terminal=false
Type=Application
Categories=AudioVideo;Player;
StartupNotify=false
""".format(os.path.basename(link_icon))
        with open(desktop_file,"w") as mf:
            mf.write(desktop_to_write)
        commands = ["cp -r {} /opt".format(folder_files),
        "cp {} /usr/share/applications".format(desktop_file),
        "cp {} /usr/share/pixmaps".format(icon_saveas),
        "chmod 755 /opt/4kvideodownloader/4kvideodownloader-bin",
        "chmod 755 /opt/4kvideodownloader/4kvideodownloader.sh"]
        to_run = write_to_tmp(commands)

        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)!=0:
            return False

        return True
        
    def remove(self):
        link_icon = "https://static.4kdownload.com/main/img/redesign/videodownloader.b9996289c0e2.svg"
        commands = ["rm -rf /opt/4kvideodownloader"]
        for f in ["/usr/share/applications/4kvideodownloader.desktop","/usr/share/pixmaps/{}".format(os.path.basename(link_icon))]:
            if os.path.isfile(f):
                commands.append("rm {}".format(f))

        to_run = write_to_tmp(commands)
        if subprocess.call("pkexec bash  {}".format(to_run),shell=True)!=0:
            return False
        return True



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
                GLib.idle_add(self.__progressbar__.set_text,"{} Already Exists".format(saveas)[:20])
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
