# vim: set encoding=utf-8 :

# Copyright (C) 2009 Adriano Monteiro Marques.
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
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
"""

import socket
import select
import umit.umpa

SCAN_MODE_RANDOM = 0
SCAN_MODE_LINEAR = 1

PORTS_ALL = range(1, 2**16)
PORTS_DEFAULT = [21, 22, 23, 25, 53, 80, 110, 443]

class TCPConnectScan(object):
    """
    """
    def __init__(self, host):
        """
        """
        self.__host = host

    def scan(self, ports=PORTS_DEFAULT, mode=SCAN_MODE_RANDOM)
        """
        """
