#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Pango
from dbase import ICDdb
import logging
import os
import setting

ICO_APP_SVG = os.path.dirname(__file__) + "/resources/icd-ten.svg"
DB_PATH = os.path.dirname(__file__) + "/resources/icd.db"


class MainWnd(Gtk.ApplicationWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(title=setting._APP_NAME, application=app, *args, **kwargs)
        self.app = app
        Gtk.Window.__init__(self, title=setting._APP_NAME, application=app)
        self.lgr = logging.getLogger('mainwnd')
        self.def_ico = self.get_icon()

        if self.def_ico:
            self.set_default_icon(self.def_ico)

        self.set_keep_above(True)
        self.__single_mode = True


        grid = Gtk.Grid()

        self.add(grid)

        self.column_cbox = Gtk.ComboBoxText()
        self.column_cbox.append_text("ICD")
        self.column_cbox.append_text("Description")
        self.column_cbox.set_active(1)
        # print(self.column_cbox.get_active())
        grid.attach(self.column_cbox, 6, 0, 1, 1)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Enter description")

        self.search_entry.connect("search-changed", self.search_changed)
        #self.search_entry.connect("stop-search", self.stop_search)

        self.search_bar = Gtk.SearchBar()
        self.search_bar.connect_entry(self.search_entry)
        self.search_bar.add(self.search_entry)
        self.search_bar.set_search_mode(True)

        # self.search_bar.search_mode_enabled(True)
        self.search_bar.set_show_close_button(False)
        grid.attach(self.search_bar, 0, 0, 5, 1)

        self.store = Gtk.ListStore(str, str)
        self.treev = Gtk.TreeView.new_with_model(self.store)#Gtk.TreeView(self.store)

        icd_renderer = Gtk.CellRendererText()
        desc_renderer = Gtk.CellRendererText()

        column_icd = Gtk.TreeViewColumn("ICD", icd_renderer, text=0)
        column_desc = Gtk.TreeViewColumn("Description", desc_renderer, text=1)

        self.treev.append_column(column_icd)
        self.treev.append_column(column_desc)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_policy(Gtk.PolicyType.EXTERNAL,
                                            Gtk.PolicyType.AUTOMATIC)

        self.scrollable_treelist.add(self.treev)

        grid.attach(self.scrollable_treelist, 0, 1, 7, 7)

        self.db = ICDdb(DB_PATH)
        self.db.connect()
        if not self.db.connected:
            self.lgr.error('Cannot connect to database')
            exit(1)

    def search_changed(self, entry):
        self.store.clear()
        txt = entry.get_text()

        if len(txt) == 1:
            if ord(txt)  < 128:
                self.column_cbox.set_active(0)
            else:
                self.column_cbox.set_active(1)

        if self.column_cbox.get_active() == 1:
            answer = self.db.get_like_description(txt)


            if len(txt) > 1:
                if answer:
                    for s in answer:
                        self.store.append([s[0], s[1]])
        else:
            answer = self.db.get_like_icd(txt)
            if len(txt) > 0:
                if answer:
                    for s in answer:
                        self.store.append([s[0], s[1]])


            #for i in range(40):
            #    self.store.append(["I70.2",  entry.get_text()])

    def stop_search(self, entry):
        print(entry.get_text())


    def get_icon(self):
        #if os.path.exists(os.path.dirname(__file__) + "/resources/"):
        #    return GdkPixbuf.Pixbuf.new_from_file(os.path.dirname(__file__) + "/resources/icd-ten.svg")

        if os.path.exists(os.path.dirname(ICO_APP_SVG)):
            return GdkPixbuf.Pixbuf.new_from_file(ICO_APP_SVG)

        self.lgr.error('no image! ')
        return None



    # view:
    @property
    def single_mode(self):
        return self.__single_mode

    @single_mode.setter
    def single_mode(self, setup_mode):
        """
        setter single_mode:
            :param setup_mode: Boolean enable / disable single mode view
        """
        self.__single_mode = setup_mode

        if setup_mode:
            self.lgr.debug('single on')
        else:
            self.lgr.debug('single off')

    # actions:
    def act_about_execute(self, action, parameter):
        about_wnd = Gtk.AboutDialog(parent=self)
        # about_wnd.set_icon_from_file(os.path.dirname(__file__) + "/resource/ico.png")

        authors = ["Aweal"]
        # about_wnd.set_logo(GdkPixbuf.Pixbuf.new_from_file(os.path.dirname(__file__) + "/resource/logo.png"))
        if self.def_ico:
            about_wnd.set_logo(GdkPixbuf.Pixbuf.new_from_file(ICO_APP_SVG))
            about_wnd.set_default_icon(self.def_ico)

        # about_wnd.set_logo_icon_name('translate')
        about_wnd.set_program_name(setting._APP_NAME)

        about_wnd.set_copyright(
            "Copyright \xa9 2015 Aweal")
        about_wnd.set_authors(authors)

        about_wnd.set_website("http://github.com/aweal/")
        about_wnd.set_website_label("show source on github")

        about_wnd.connect("response", self.on_close)
        about_wnd.show()

    def on_close(self, widget, resp):
        widget.destroy()
