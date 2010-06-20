#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Adriano Monteiro Marques
#
# Author: Joao Paulo de Souza Medeiros <ignotus@umitproject.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import gtk
import gobject

from higwidgets.higframe import HIGFrameRNet
from higwidgets.higboxes import HIGVBox, HIGHBox
from higwidgets.higdialogs import HIGAlertDialog
from higwidgets.higscrollers import HIGScrolledWindow

from umit.core.UmitConf import ProfileNotFound, Profile
from umit.core.Paths import Path
from umit.core.UmitLogging import log
from umit.core.I18N import _

from umit.gui.ScanOpenPortsPage import ScanOpenPortsPage

from umit.scan.zion.gui.AttractorWidget import AttractorWidget
from umit.zion.scan import probe
from umit.zion.core import address, options, zion, host
from umit.zion.core.host import PORT_STATE_OPEN

ICON_DIR = 'share/pixmaps/zion/'

PIXBUF_FIREWALL = gtk.gdk.pixbuf_new_from_file(ICON_DIR + 'firewall.png')
PIXBUF_SYNPROXY = gtk.gdk.pixbuf_new_from_file(ICON_DIR + 'shield.png')
PIXBUF_HONEYD = gtk.gdk.pixbuf_new_from_file(ICON_DIR + 'honey.png')

class ZionHostsView(gtk.Notebook):
    """
    """
    def __init__(self):
        """
        """
        gtk.Notebook.__init__(self)
        self.set_border_width(6)
        self.set_tab_pos(gtk.POS_TOP)

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__scans_page = ZionScansPage()
        #self.__ports_page = ZionPortsPage()
        self.__ports_page = HIGVBox()
        self.__ident_page = ZionIdentificationPage()
        
        self.open_ports = ScanOpenPortsPage()

        self.append_page(self.__scans_page, gtk.Label(_('Scans')))
        self.append_page(self.__ports_page, gtk.Label(_('Ports')))
        self.append_page(self.__ident_page, gtk.Label(_('Identification')))
        
        self.__ports_page.add(self.open_ports)
        
    def port_mode(self):
        self.open_ports.host.port_mode()        

class ZionScansPage(HIGVBox):
    """
    """
    def __init__(self):
        """
        """
        HIGVBox.__init__(self)

class ZionPortsPage(HIGVBox):
    """
    """
    def __init__(self):
        """
        """
        HIGVBox.__init__(self)

class ZionIdentificationPage(HIGVBox):
    """
    """
    def __init__(self):
        """
        """
        HIGVBox.__init__(self)

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__hbox = HIGHBox()
        self.__info = gtk.Label(_('Information'))
        self.__attractor = AttractorWidget()
        self.__frame_attractor = HIGFrameRNet(_('Attractor'))
        self.__frame_attractor._add(self.__attractor)

        self.__hbox._pack_expand_fill(self.__info)
        self.__hbox._pack_noexpand_nofill(self.__frame_attractor)

        self._pack_noexpand_nofill(self.__hbox)

class ZionHostsList(gtk.ScrolledWindow):
    """
    """
    def __init__(self):
        """
        """
        gtk.ScrolledWindow.__init__(self)
        self.set_border_width(6)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_NONE)

        self.__create_widgets()

    def __create_widgets(self):
        """
        """
        self.__cell_text = gtk.CellRendererText()
        self.__cell_pixbuf = gtk.CellRendererPixbuf()

        self.__hosts_store = gtk.ListStore(gtk.gdk.Pixbuf,
                                           gobject.TYPE_STRING)

        self.__hosts_treeview = gtk.TreeView(self.__hosts_store)
        self.__hosts_treeview.connect('cursor-changed', self.__cursor_callback)

        self.__hosts_column = list()

        self.__column_type = gtk.TreeViewColumn(_('Type'),
                                                self.__cell_pixbuf,
                                                pixbuf=0)
        self.__column_host = gtk.TreeViewColumn(_('Host'),
                                                self.__cell_text,
                                                text=1)

        self.__hosts_store.append([PIXBUF_FIREWALL,
            'firewall.example.com\n192.0.2.1'])
        self.__hosts_store.append([PIXBUF_SYNPROXY,
            'synproxy.example.com\n192.0.2.2'])
        self.__hosts_store.append([PIXBUF_HONEYD,
            'honeyd.example.com\n192.0.2.3'])

        self.__column_type.set_reorderable(True)
        self.__column_type.set_resizable(False)
        self.__column_host.set_reorderable(True)
        self.__column_host.set_resizable(False)

        self.__hosts_treeview.append_column(self.__column_type)
        self.__hosts_treeview.append_column(self.__column_host)

        self.__hosts_store.set_sort_func(0, self.__sort_type)
        self.__hosts_store.set_sort_func(1, self.__sort_host)

        self.add(self.__hosts_treeview)

        self.__hosts_treeview.set_cursor((0,))
        self.__cursor_callback(self.__hosts_treeview)

    def __cursor_callback(self, widget):
        """
        """
        path = widget.get_cursor()[0]
        iter = self.__hosts_store.get_iter(path)
        self.__hosts_store.get_value(iter, 0)

    def __sort_type(self, treemodel, iter1, iter2):
        """
        """
        return 0

    def __sort_host(self, treemodel, iter1, iter2):
        """
        """
        return 0

class ZionResultsPage(gtk.HPaned):
    """
    """
    def __init__(self):
        """
        """
        gtk.HPaned.__init__(self)

        self.__create_widgets()
        self.set_position(200)

    def __create_widgets(self):
        """
        """
        self.__list = ZionHostsList()
        self.__view = ZionHostsView()

        self.add1(self.__list)
        self.add2(self.__view)
        
    def clear_port_list(self):
        """Clear Umit's scan result ports list."""
        self.__view.open_ports.host.clear_port_list()
        
    def set_host_port(self, host):
        """Set host to dipslay in Ports tab."""
        host_page = self.__view.open_ports.host
        host_page.switch_port_to_list_store()
        
        host_page.clear_port_list()
        
        ports = host.get_ports()
        port_ids = ports.keys()
        port_ids.sort()
        
        for port in port_ids:
            host_page.add_port(
                    (self.findout_service_icon(ports[port]), ) +
                    get_port_info(ports[port]))
            
    def update_host_info(self, host):
        """Update host info to show host ports."""
        self.__view.port_mode()
        self.set_host_port(host)        
            
    def findout_service_icon(self, port_info):
        return gtk.STOCK_YES            

class ZionProfile(HIGVBox):
    """
    """
    def __init__(self, target=None):
        """
        """
        HIGVBox.__init__(self)

        self.target = target
        self.result = ZionResultsPage()

        self.pack_end(self.result)

    def update_target(self, target):
        """
        """
        self.target = target

    def check_scan(self):
        """
        """
        if self.target:
            return True

        return False

class ZionProfileHoneyd(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)

class ZionProfileOS(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)
        
    def start(self):
        """
        """
        z = zion.Zion(options.Options(), [])
        
        self.result.clear_port_list()
        
        # what options are needed ?
        z.get_option_object().add("-s")
        
        if address.recognize(self.target) == address.Unknown:
            l = probe.get_addr_from_name(self.target)
            for i in l:
                try:
                    z.append_target(host.Host(i, self.target))
                except:
                    print "Unimplemented support to address: %s." % i
        else:
            z.append_target(host.Host(self.target))
              
        z.run()
        
        # update host information
        self.result.update_host_info(z.get_target_list()[0])

class ZionProfilePrompt(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)

        self.__command_hbox = HIGHBox()
        self.__command_label = gtk.Label(_('Command:'))
        self.__command_entry = gtk.Entry()

        self.__command_hbox._pack_noexpand_nofill(self.__command_label)
        self.__command_hbox._pack_expand_fill(self.__command_entry)

        self._pack_noexpand_nofill(self.__command_hbox)

    def check_scan(self):
        """
        """
        if self.__command_entry.get_text().strip():
            return True

        return False

class ZionProfileSYNProxy(ZionProfile):
    """
    """
    def __init__(self, target=None):
        """
        """
        ZionProfile.__init__(self, target)

PROFILE_CLASS = {'1': ZionProfileHoneyd,
                 '2': ZionProfileOS,
                 '3': ZionProfilePrompt,
                 '4': ZionProfileSYNProxy}

class ZionScanNotebookPage(gtk.Alignment):
    """
    """
    def __init__(self, page):
        """
        """
        gtk.Alignment.__init__(self, 0, 0, 1, 1)

        self.page = page
        self.profile = None

    def profile_changed(self, widget, event=None):
        """
        """
        profile = self.page.toolbar.selected_profile
        target = self.page.toolbar.selected_target.strip()

        if self.profile != profile:
            id = Profile()._get_it(profile, 'zion_id')
            if self.get_child():
                self.remove(self.get_child())

            self.add(PROFILE_CLASS[id](target))

            if type(self.get_child()) == ZionProfilePrompt:
                self.page.toolbar.target_entry.set_sensitive(False)
            else:
                self.page.toolbar.target_entry.set_sensitive(True)

            self.show_all()
            self.profile = profile

    def target_changed(self, widget, event=None):
        """
        """
        target = self.page.toolbar.selected_target.strip()
        self.get_child().update_target(target)

        if self.get_child().check_scan():
            self.page.toolbar.scan_button.set_sensitive(True)
        else:
            self.page.toolbar.scan_button.set_sensitive(False)

    def start_scan_cb(self, widget):
        """
        """
        self.get_child().start()

    def kill_scan(self):
        """
        """
        pass

    def close_tab(self):
        """
        """
        pass

    def create_references(self):
        """
        """
        self.target_handle = self.page.toolbar.target_entry.connect('changed',
                self.target_changed)
        self.page.toolbar.target_entry.changed_handler = self.target_handle

    def delete_references(self):
        """
        """
        id = self.target_handle
        if (self.page.toolbar.target_entry.handler_is_connected(id)):
            self.page.toolbar.target_entry.disconnect(id)
            self.page.toolbar.target_entry.changed_handler = None

def get_port_info(port):
    """Return port info."""
    if (port.status == host.PORT_STATE_OPEN):
        status = 'open'
    elif (port.status == host.PORT_STATE_FILTERED):
        status = 'filtered'
    else:
        status = 'closed'
        
    if (port.protocol == host.PROTOCOL_TCP):
        protocol = 'tcp'
    elif (port.protocol == PROTOCOL_UDP):
        protocol = 'udp'
    elif (port.protocol == PROTOCOL_ICMP):
        procotol = 'icmp'
    else:
        protocol = ''

    return (
            int(port.number),
            protocol,
            status,
            port.service,
            '')