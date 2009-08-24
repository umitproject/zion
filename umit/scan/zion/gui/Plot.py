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

PLOT_MODE_POINT = 0
PLOT_MODE_LINE = 1

class Plot(gtk.DrawingArea):
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
        self.connect('motion_notify_event', self.motion)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.ENTER_NOTIFY |
                        gtk.gdk.LEAVE_NOTIFY |
                        gtk.gdk.MOTION_NOTIFY |
                        gtk.gdk.NOTHING |
                        gtk.gdk.KEY_PRESS_MASK |
                        gtk.gdk.KEY_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.SCROLL_MASK)

        self.set_flags(gtk.CAN_FOCUS)
        self.grab_focus()

    def motion(self, widget, event):
        """
        """
        self.queue_draw()
        return False

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

        self.area = self.get_allocation()
        self.center = (self.area.width / 2, self.area.height / 2)

        self.context.translate(self.center[0], self.center[1])

        self.scale = max(self.area) * 0.8
        self.context.scale(self.scale, -self.scale)

        self.__draw_content()

        return True

    def __draw_content(self):
        """
        """
