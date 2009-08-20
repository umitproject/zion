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

class AttractorWidget(gtk.DrawingArea):
    """
    """
    def __init__(self, input=None):
        """
        """
        gtk.DrawingArea.__init__(self)

        if input:
            self.__input = input
        else:
            self.__input = []

        self.connect('expose_event', self.expose)

    def expose(self, widget, event):
        """
        Drawing callback
        @type  widget: GtkWidget
        @param widget: Gtk widget superclass
        @type  event: GtkEvent
        @param event: Gtk event of widget
        @rtype: boolean
        @return: Indicator of the event propagation
        """
        self.set_size_request(200, 200)
        self.context = widget.window.cairo_create()
        self.context.rectangle(*event.area)
        self.context.set_source_rgb(1.0, 1.0, 1.0)
        self.context.fill_preserve()
        self.context.set_line_width(1)
        self.context.set_source_rgb(0.0, 0.0, 0.0)
        self.context.stroke()

        self.__draw()

        return False

    def __draw(self):
        """
        """
        pass
