#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pluginsgtk.py
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
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
import os
import sys
import gettext
import imp
from site import addsitedir

MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""

authors_                 = ["Youssef Sourani <youssef.m.sourani@gmail.com>"]
version_                 = "0.1"
copyright_               ="Copyright © 2018 Youssef Sourani"
comments_                = "LUniversal Installer"
website_                 = "https://arfedora.blogspot.com"
translators_             = ("translator-credit")
appname                  = "luniversalinstaller"
appwindowtitle           = "LUniversal Installer"
appid                    = "com.github.yucefsourani.LUniversalInstaller"
maxwidgetinrow           = 5

locale                   = [l for l in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"locale"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../usr/share/locale")] if os.path.isdir(l)]
if locale:
    gettext.install(appname,locale[0])

icon_                    = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"{}.png".format(appid)),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../usr/share/pixmaps/{}.png".format(appid))] if os.path.isfile(i)]
if icon_:
    icon_ = icon_[0]

plugins_l                = [os.path.join(os.path.realpath(os.path.dirname(__file__)),"plugins"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../usr/share/{}/plugins".format(appname))]
#if len(sys.argv)>1:
#    plugins_l.append(os.path.expanduser(sys.argv[-1]))
plugins_location         = [l for l in  plugins_l if os.path.isdir(l)]




arch = os.uname().machine
distro_desktop = os.getenv("XDG_CURRENT_DESKTOP",False)

def get_distro_name():
    result=""
    if not os.path.isfile("/etc/os-release"):
        return None
    with open("/etc/os-release","r") as myfile:
        for l in myfile.readlines():
            if l.startswith("ID"):
                result=l.split("=")[1].strip()
    if result.startswith("\"") and result.endswith("\""):
        return result[1:-1]
    elif result.startswith("\'") and result.endswith("\'"):
        return result[1:-1]
    return result

def get_distro_version():
    result=""
    if not os.path.isfile("/etc/os-release"):
        return None
    with open("/etc/os-release","r") as myfile:
        for l in myfile.readlines():
            if l.startswith("VERSION_ID"):
                result=l.split("=")[1].strip()
    if result.startswith("\"") and result.endswith("\""):
        return result[1:-1]
    elif result.startswith("\'") and result.endswith("\'"):
        return result[1:-1]
    return result

def get_plugins():
    """Searches the plugins folders"""
    depl = []
    result = []
    for plugin_folder in plugins_location:
        addsitedir(plugin_folder)
        for  module_file in os.listdir(plugin_folder):
            if module_file.endswith(".py") and os.path.isfile(os.path.join(plugin_folder,module_file)):
                if module_file not in depl:
                    module_name, module_extension = os.path.splitext(module_file)
                    result.append(os.path.join(plugin_folder,module_name))
                    depl.append(module_file)
    return result
    
def load_plugin(module_name):
    """import valid plugin"""
    try:
        module_hdl, plugin_path_name, description = imp.find_module(module_name)
        plugin = imp.load_module(module_name, module_hdl, plugin_path_name,description)
    except Exception as e :
        print(e)
        print("Load {} Fail.".format(os.path.join(module_name+".py")))
        return False
    finally:
        if module_hdl:
            module_hdl.close()
    
    return plugin





class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(975, 645)
        sw=Gtk.ScrolledWindow()
        self.mainbox  = Gtk.VBox(spacing=10)
    
        self.revealer = Gtk.Revealer()
        hboxrevealer  = Gtk.HBox()
        hboxrevealer.pack_start(self.revealer,True,False,0)
        self.entry    = Gtk.SearchEntry(placeholder_text="Search Repo")
        self.entry.props.margin_left = 15
        self.entry.props.margin_right = 15
        self.entry.props.margin_top = 5
        self.entry.props.margin_bottom = 5
        self.entry.connect("search-changed", self._on_search)
        self.revealer.add(self.entry)
        self.mainbox.pack_start(hboxrevealer,False,False,0)

        
        self.flowbox = Gtk.FlowBox(homogeneous=True)
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(maxwidgetinrow)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_filter_func(self._flowbox_filter_func)
        
        self.loading_all_plugins()
            
        self.mainbox.pack_start(self.flowbox,False,False,0)
        sw.add(self.mainbox)
        self.add(sw)
        self.connect("key-press-event", self._on_key_press)
        self.show_all()
        
    def _flowbox_filter_func(self, flowbox):
        text = self.entry.get_text()
        if not text:
            return flowbox
        lbl = flowbox.get_child().get_children()[0].get_children()[1]
        if text.lower() in lbl.get_text().lower():
            return flowbox 

    def _on_search(self, entry):
        self.flowbox.invalidate_filter()


    def _on_transition(self,reveal_child=True):
        if  reveal_child:
            if not self.revealer.get_reveal_child():
                pass
            else:
                self.revealer.set_reveal_child(False) 
                self.entry.set_text("") 
        else:
            if self.revealer.get_reveal_child():
                pass
            else:
                self.revealer.set_reveal_child(True)
                self.entry.grab_focus()

    def _on_key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == 'Escape':
            self._on_transition(True)
        else:
            self._on_transition(False)
            
    def loading_all_plugins(self):
        distro_name    = get_distro_name()
        distro_version = get_distro_version()
        all_plugins    = get_plugins()
        for module_name in all_plugins:
            plugin = load_plugin(module_name)
            if not plugin:
                continue
            try:
                if_true_skip         = plugin.if_true_skip
                if_false_skip        = plugin.if_false_skip
                if_one_true_skip     = plugin.if_one_true_skip
                if_all_true_skip     = plugin.if_all_true_skip
                if if_true_skip:
                    continue
                if not if_false_skip:
                    continue
                if any(if_one_true_skip):
                    continue
                if all(if_all_true_skip):
                    continue

                arch_                = plugin.arch
                distro_name_         = plugin.distro_name
                distro_version_      = plugin.distro_version
                if "all" not in arch_:
                    if arch not in arch_:
                        continue
                if "all" not in distro_name_:
                    if distro_name not in distro_name_:
                        continue                 
                if "all" not in distro_version_:
                    if distro_version not in distro_version_:
                        continue

                plugin_class = plugin.Plugin(parent=self)
                self.flowbox.add(plugin_class)
                
            except Exception as e:
                print(e)
                print("Ignored >> Load {} Fail.".format(plugin))
                continue
        
        self.show_all()

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=appid,
                         flags=Gio.ApplicationFlags(0),
                         **kwargs)
        self.window = None
        
    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))
        
    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title=appwindowtitle)
            
        self.window.present()

    def on_quit(self, action, param):
        self.quit()

    def on_about(self,a,p):
        about = Gtk.AboutDialog(parent=self.window,transient_for=self.window, modal=True)
        about.set_program_name(appwindowtitle)
        about.set_version(version_)
        about.set_copyright(copyright_)
        about.set_comments(comments_)
        about.set_website(website_)
        if icon_:
            logo_=GdkPixbuf.Pixbuf.new_from_file(icon_)
            about.set_logo(logo_)
        about.set_authors(authors_)
        about.set_license_type(Gtk.License.GPL_3_0)
        if translators_ != "translator-credits":
            about.set_translator_credits(translators_)
        about.run()
        about.destroy()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)









