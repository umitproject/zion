# Copyright (C) 2010 Adriano Monteiro Marques
#
# Author: Diogo Ricardo Marques Pinheiro <diogormpinheiro@gmail.com>
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

import gobject

class Connector(gobject.GObject):
    __gsignals__ = {
        # emited by zion when host scan finish.
        'scan_finished': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (object,)),

        # signal emited when all tcp isn samples obtained.
        # TODO: should be refreshed periodically ?
        'isn_samples_finished': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),

        # emited when time series created.
        'timeseries_created': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),

        # emited when attractors are built.
        'attractors_built': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (object,)),

        # signal emited when fingerprint finished.
        'fingerprint_finished': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        
        # signal emited when fingerprint matching done.
        'matching_finished': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (object,)),
        
        # signal emited when synproxy detection finish
        'synproxy_finished': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (bool,)),
        
        # signal emited when honeyd detection finish
        'honeyd_finished': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (bool,)),
        
        # signal emited to update operation status
        'update_status': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (str,))
    }

    def __init__(self):
        self.__gobject_init__()


gobject.type_register(Connector)
