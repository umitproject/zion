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

from higwidgets.higboxes import HIGVBox, HIGHBox
from higwidgets.higdialogs import HIGAlertDialog
from higwidgets.higscrollers import HIGScrolledWindow

from umit.core.UmitConf import ProfileNotFound, Profile
from umit.core.Paths import Path
from umit.core.UmitLogging import log
from umit.core.I18N import _

class ZionProfileSYNProxy(HIGVBox):
    """
    """
    def __init__(self):
        """
        """
        HIGVBox.__init__(self)

class ZionProfilePromptPage(HIGVBox):
    """
    """
    def __init__(self):
        """
        """
        HIGVBox.__init__(self)

        self.__command_hbox = HIGHBox()
        self.__command_label = gtk.Label(_('Command:'))
        self.__command_entry = gtk.Entry()

        self.__command_hbox._pack_noexpand_nofill(self.__command_label)
        self.__command_hbox._pack_expand_fill(self.__command_entry)

        self._pack_noexpand_nofill(self.__command_hbox)

PROFILE_CLASS = {'1': ZionProfileSYNProxy,
                 '2': ZionProfilePromptPage}

class ZionScanNotebookPage(HIGVBox):
    """
    """
    def __init__(self, page):
        """
        """
        HIGVBox.__init__(self)

        self.container = gtk.Alignment(0, 0, 1, 1)
        self.container.set_padding(0, 0, 0, 0)

        self.page = page
        self.profile = None
        self.content = None

        self._pack_expand_fill(self.container)

    def profile_changed_local(self, widget, event=None):
        """
        """
        profile = self.page.toolbar.selected_profile
        target = self.page.toolbar.selected_target.strip()

        if self.profile != profile:
            id = Profile()._get_it(profile, 'zion_id')
            if self.content:
                self.container.remove(self.content)
            self.content = PROFILE_CLASS[id]()
            self.container.add(self.content)
            self.container.show_all()

            self.profile = profile

    def kill_scan(self):
        """
        """
        pass

    def close_tab(self):
        """
        """
        pass

    def erase_references(self):
        """
        """
        pass
