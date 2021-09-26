#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  luniversalinstaller.py
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
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio,Pango
import os
import sys
import gettext
from site import addsitedir
import threading
import urllib.request
import random

__minor__ = sys.version_info.minor
if __minor__>4:
    import importlib
else:
    import imp



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
version_                 = "0.2"
copyright_               ="Copyright © 2018 Youssef Sourani"
comments_                = "LUniversal Installer"
website_                 = "https://github.com/yucefsourani/LUniversalInstaller"
translators_             = ("translator-credit")
appname                  = "luniversalinstaller"
appwindowtitle           = "LUniversal Installer"
appid                    = "com.github.yucefsourani.LUniversalInstaller"
maxwidgetinrow           = 6

locale                   = [l for l in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"locale"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/locale")] if os.path.isdir(l)]
if locale:
    gettext.install(appname,locale[0])

icon_                    = [i for i in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"{}.png".format(appid)),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/pixmaps/{}.png".format(appid))] if os.path.isfile(i)]
if icon_:
    icon_ = icon_[0]


plugins_location         = [l for l in  [os.path.join(os.path.realpath(os.path.dirname(__file__)),"plugins"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../share/{}/plugins".format(appname))] if os.path.isdir(l)]

class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,parent=None):
        Gtk.MessageDialog.__init__(self,buttons = Gtk.ButtonsType.OK_CANCEL)
        self.props.message_type = Gtk.MessageType.QUESTION
        self.props.text         = msg
        self.p=parent
        if self.p != None:
            self.parent=self.p
            self.set_transient_for(self.p)
            self.set_modal(True)
            self.p.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
            
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            self.destroy()
            if self.p != None:
                self.p.set_sensitive(True)
            return True
        else:
            if self.p != None:
                self.p.set_sensitive(True)
            self.destroy()
            return False

image_loction  = [l for l in [os.path.join(os.path.realpath(os.path.dirname(__file__)),"images"),os.path.join(os.path.realpath(os.path.dirname(__file__)),"../../images".format(appname))] if os.path.isdir(l)]
def get_image_location(image_name):
    if image_loction:
        for i in image_loction:
            location = os.path.join(i,image_name)
            if os.path.isfile(location):
                return location
    return False
    
arch = os.uname().machine
distro_desktop = os.getenv("XDG_CURRENT_DESKTOP",False)


def get_distro_name(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("ID") and not l.startswith("ID_"):
                result=l.split("=",1)[1].strip()
    return result.replace("\"","").replace("'","")

def get_distro_name_like(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("ID_LIKE") :
                result=l.split("=",1)[1].strip()
    if not result:
        result = get_distro_name(location)
    return result.replace("\"","").replace("'","")
    
def get_distro_version(location="/etc/os-release"):
    result=""
    if not os.path.isfile(location):
        return None
    with open(location) as myfile:
        for l in myfile:
            if l.startswith("VERSION_ID"):
                result=l.split("=",1)[1].strip()
    return result.replace("\"","").replace("'","")

def old_get_plugins():
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


def new_get_plugins():
    """Searches the plugins folders"""
    depl = []
    result = []
    for plugin_folder in plugins_location:
        addsitedir(plugin_folder)
        for  module_file in os.listdir(plugin_folder):
            if module_file.endswith(".py") and os.path.isfile(os.path.join(plugin_folder,module_file)):
                if module_file not in depl:
                    module_name, module_extension = os.path.splitext(module_file)
                    result.append((plugin_folder,module_name,module_file))
                    depl.append(module_file)
    return result



"""def new_load_plugin(info):
    module_ = importlib.machinery.SourceFileLoader(info[1],os.path.join(info[0],info[2])).exec_module(os.path.join(info[0],info[1]))
    return module_"""

def new_load_plugin(info):
    spec   = importlib.util.spec_from_file_location(info[1],os.path.join(info[0],info[2]))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def old_load_plugin(module_name):
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

if __minor__>4:
    get_plugins = new_get_plugins
    load_plugin = new_load_plugin
else:
    get_plugins = old_get_plugins
    load_plugin = old_load_plugin

class Splash(threading.Thread):
    def __init__(self):
        super(Splash, self).__init__()
        self.window = Gtk.Window()
        self.window.set_decorated(False)
        self.window.props.window_position = Gtk.WindowPosition.CENTER
        self.window.connect('delete-event', self.destroy)
        self.window.set_default_size(600, 400)
        
        urls = ["https://i.imgur.com/CA1il3p.gif",
                "http://bestanimations.com/Animals/Birds/Penguins/Penguin-04-june.gif",
                "http://bestanimations.com/Animals/Birds/Penguins/penguinanimation-10.gif",
                "http://bestanimations.com/Animals/Birds/Penguins/animatedpenguin-11.gif",
                "http://bestanimations.com/Animals/Birds/Penguins/penguin-animation.gif",
                "http://bestanimations.com/Animals/Birds/Penguins/Penguin-03-june.gif",]
        gio_file = Gio.File.new_for_uri(random.choice(urls))
        gio_file.load_contents_async(None,self.on_async_ready)

        mainbox        = Gtk.VBox()
        self.image_box = Gtk.Box()
        label_box      = Gtk.Box()
        mainbox.pack_start(self.image_box, True, True, 10)
        mainbox.pack_start(label_box, True, True, 10)
        
        self.label     = Gtk.Label()
        self.label.set_line_wrap(True)
        self.label.set_line_wrap(True)
        self.label.props.use_markup = True
        self.label.set_line_wrap_mode(Pango.WrapMode(0))
        label_box.pack_start(self.label, True, True, 10)
        
        self.window.add(mainbox)

    def run(self):
        self.window.set_auto_startup_notification(False)
        self.window.show_all()
        self.window.set_auto_startup_notification(True)


    def destroy(self):
        self.window.destroy()
        
    def on_async_ready(self,source_object, result, user_data=None):
        try:
            succes, content, etag = source_object.load_contents_finish(result)#result=Gio.Task()
            stream       = Gio.MemoryInputStream.new_from_data(content)
            image_pixbuf = GdkPixbuf.PixbufAnimation.new_from_stream(stream,None)
            #image_pixbuf = GdkPixbuf.PixbufAnimation.new_from_stream_finish(result)
            image        = Gtk.Image.new_from_animation(image_pixbuf)
            self.image_box.pack_start(image,True,True,0)
        except Exception as e:
            print(e)
            image = Gtk.Spinner()
            image.start()
            self.image_box.pack_start(image,True,True,0)


        self.window.show_all()
        
class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(850, 645)

        self.init()
        
    def init(self):
        self.all_category   = {}
        self.switchcategory = {}

        self.sw=Gtk.ScrolledWindow()
        self.maincontainer = Gtk.VBox()
        self.grid          = Gtk.Grid()
        self.stack    = Gtk.Stack()
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        self.listbox_ = Gtk.ListBox()
        
        self.grid.attach(self.listbox_, 0, 0, 1, 1)
        self.grid.attach(self.stack, 1, 0, 1, 1)
        self.sw.add(self.grid)
        self.maincontainer.pack_start(self.sw,True,True,0)
        self.add(self.maincontainer)

        self.loading_all_plugins()
        

        self.listbox_.connect("row-activated",self.on_activated_row)
        try:
            gi.require_version('Vte', '2.91')
            from gi.repository import Vte
            tscrolledwindow = Gtk.ScrolledWindow()
            tscrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC ,Gtk.PolicyType.AUTOMATIC)
            self.terminal = Vte.Terminal()
            
            #self.terminal.set_color_background(Gdk.RGBA(red=0.180392, green=0.203922, blue=0.211765, alpha=1.000000))
            self.terminal.set_color_foreground(Gdk.RGBA(red=0.988235, green=0.913725, blue=0.309804, alpha=1.000000))
            vadjustment = self.terminal.get_vadjustment()
            tscrolledwindow.set_vadjustment(vadjustment)
            _pty = Vte.Pty.new_sync(Vte.PtyFlags(0),None)
            _pty.child_setup()
            self.terminal.set_pty(_pty)
            
            self.terminal.connect("button-release-event",self.on_button_event)
            
            self.menu = Gtk.Menu()
            self.menu.set_screen(Gdk.Screen().get_default())
            
            self.copytextmenuitem = Gtk.MenuItem.new_with_label("Copy")
            cursorcolormenuitem = Gtk.MenuItem.new_with_label("Cursor Color")
            backgroundmenuitem = Gtk.MenuItem.new_with_label("Backgound Color")
            foregroundmenuitem = Gtk.MenuItem.new_with_label("Foreground Color")
            
            self.copytextmenuitem.connect("activate", self.copy_text)
            cursorcolormenuitem.connect("activate", self.on_cursor_menuitem_activated)
            backgroundmenuitem.connect("activate", self.on_background_menuitem_activated)
            foregroundmenuitem.connect("activate", self.on_foreground_menuitem_activated)
            
            self.menu.append(self.copytextmenuitem)
            self.menu.append(cursorcolormenuitem)
            self.menu.append(backgroundmenuitem)
            self.menu.append(foregroundmenuitem)
            
            self.vte_format = Vte.Format(1)
            tscrolledwindow.add(self.terminal)
            self.maincontainer.pack_end(tscrolledwindow,False,True,0)
        except Exception as e:
            print(e)
        self.show_all()

        
    def _flowbox_filter_func(self, flowbox,entry):
        text = entry.get_text()
        if not text:
            return flowbox
        lbl  = flowbox.get_child().get_children()[0].get_children()[1]
        if text.lower() in lbl.get_text().lower():
            return flowbox 

    def _on_search(self, entry,flowbox):
        flowbox.invalidate_filter()


    def _on_transition(self,revealer,entry,reveal_child=True):
        if  reveal_child:
            if not revealer.get_reveal_child():
                pass
            else:
                revealer.set_reveal_child(False) 
                entry.set_text("") 
        else:
            if revealer.get_reveal_child():
                pass
            else:
                revealer.set_reveal_child(True)
                entry.grab_focus()

    def _on_key_press(self, widget, event):
        mainvbox   = self.stack.get_visible_child()
        revealer   = mainvbox.get_children()[0].get_children()[0]
        entry      = mainvbox.get_children()[0].get_children()[0].get_children()[0]
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == 'Escape':
            self._on_transition(revealer,entry,True)
        else:
            self._on_transition(revealer,entry,False)

            
    def loading_all_plugins(self):
        splash = Splash()
        splash.start()
        distro_name    = get_distro_name()
        distro_version = get_distro_version()
        all_plugins    = get_plugins()
        for module_name in all_plugins:
            splash.label.set_label("<span font_weight=\"bold\">Loading {} Plugin.</span>".format(module_name[1]))
            while Gtk.events_pending():
                Gtk.main_iteration()
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
                
                category             = plugin.category
                category_icon_theme  = plugin.category_icon_theme
                if category not in self.all_category.keys():
                    cb=Gtk.HBox(spacing=10)
                    try:
                        category_icon=GdkPixbuf.Pixbuf.new_from_file_at_size(get_image_location(category_icon_theme),32,32)
                    except :
                        try:
                            category_icon = Gtk.IconTheme.get_default().load_icon(category_icon_theme,32, Gtk.IconLookupFlags.FORCE_SIZE)
                        except:
                            #failback
                            category_icon = Gtk.IconTheme.get_default().load_icon("applications-accessories",32, Gtk.IconLookupFlags.FORCE_SIZE)
                            
                    category_icon  = Gtk.Image.new_from_pixbuf(category_icon)
                    category_label = Gtk.Label()
                    category_label.props.use_markup=True
                    category_label.set_markup(category)
                    cb.pack_start(category_icon,False,False,0)
                    cb.pack_start(category_label,False,False,0)
                    
                    cb.set_margin_start(10)
                    cb.set_margin_end(70)
                    grid__=Gtk.Grid()
                    grid__.add(cb)
                    row_ = Gtk.ListBoxRow(activatable=True)
                    row_.add(grid__)
                    self.listbox_.add(row_)
                    
                    
                    mainbox       = Gtk.VBox(spacing=5)
                    
                    revealer      = Gtk.Revealer()
                    hboxrevealer  = Gtk.HBox()
                    hboxrevealer.pack_start(revealer,True,False,0)
                    entry         = Gtk.SearchEntry(placeholder_text="Search...")
                    entry.props.margin_start = 15
                    entry.props.margin_end = 15
                    entry.props.margin_top = 5
                    entry.props.margin_bottom = 5
                    revealer.add(entry)
                    mainbox.pack_start(hboxrevealer,False,False,0)

        
                    flowbox = Gtk.FlowBox(homogeneous=True)
                    entry.connect("search-changed", self._on_search,flowbox)
                    flowbox.set_valign(Gtk.Align.START)
                    flowbox.set_max_children_per_line(maxwidgetinrow)
                    flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
                    flowbox.set_filter_func(self._flowbox_filter_func,entry)
                    mainbox.pack_start(flowbox,False,False,0)

                    
                        
                    self.stack.add_named(mainbox, category)
                    self.all_category.setdefault(category,mainbox)
                    self.switchcategory.setdefault(row_,category) 


                plugin_class = plugin.Plugin(parent=self)
                self.all_category[category].get_children()[1].add(plugin_class) #right flowbox.add(plugin_class)
                del plugin
            except Exception as e:
                print(e)
                print("Ignored >> Load {} Fail.".format(plugin))
                continue
        if len(self.switchcategory)>0:
            self.connect("key-press-event", self._on_key_press)
        
        splash.destroy()
        del splash

    def on_activated_row(self, listbox,listboxrow):
        self.stack.set_visible_child_name(self.switchcategory[listboxrow]) # ==category name == mainbox for this category name
        
        
    def copy_text(self,w):
        self.terminal.copy_clipboard_format(self.vte_format)

        
    def on_button_event(self,terminal,event):
        if not  self.terminal.get_has_selection():
            self.copytextmenuitem.set_sensitive(False)
        else:
            self.copytextmenuitem.set_sensitive(True)
            
        if  event.button==3:
            self.menu.popup_at_pointer()
            self.menu.show_all()

    def on_cursor_menuitem_activated(self,menuitem):
        colorchooserdialog = Gtk.ColorChooserDialog(parent=self)
        if colorchooserdialog.run() == Gtk.ResponseType.OK:
            color = colorchooserdialog.get_rgba()
            self.terminal.set_color_cursor(color)
        colorchooserdialog.destroy()
        
        
    def on_background_menuitem_activated(self,menuitem):
        colorchooserdialog = Gtk.ColorChooserDialog(parent=self)
        if colorchooserdialog.run() == Gtk.ResponseType.OK:
            color = colorchooserdialog.get_rgba()
            self.terminal.set_color_background(color)
        colorchooserdialog.destroy()

    def on_foreground_menuitem_activated(self,menuitem):
        colorchooserdialog = Gtk.ColorChooserDialog(parent=self)
        if colorchooserdialog.run() == Gtk.ResponseType.OK:
            color = colorchooserdialog.get_rgba()
            self.terminal.set_color_foreground(color)
        colorchooserdialog.destroy()
        

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
            self.window.connect("delete-event",self.on_quit)
            
        self.window.present()

    def on_quit(self, action, param=None):
        if threading.active_count()>1:
            dt = [t for t in threading.enumerate()[1:] if not t.daemon]
            if dt:
                print("Threads Not Daemon Running Wait To Finish.")
                for t in dt:
                    print(t)
                return True
            else:
                check = Yes_Or_No("Tasks Running In Background,Are You Sure You Want To Exit?")
                check = check.check()
                if  check:
                    self.quit()
                else:
                    return True
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









