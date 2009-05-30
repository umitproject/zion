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
Host management module.
"""

import umit.zion.core.address as Address

PROTOCOL_TCP = 0
PROTOCOL_UDP = 1
PROTOCOL_ICMP = 2

class Port(object):
    """
    """
    def __init__(self, number, protocol, status, service=None):
        """
        """
        self.number = number
        self.protocol = protocol
        self.status = status
        self.service = service

class Host(object):
    """
    Class that represent an network entity that has a least one address.
    """
    def __init__(self, addr=None):
        """
        """
        self.set_addr(addr)
        self.__ports = {}

    def add_port(self, port):
        """
        """
        self.__ports[port.number] = port

    def set_addr(self, addr):
        """
        """
        if addr:
            addr_type = Address.recognize(addr)
            if addr_type:
                self.__addr = addr_type(addr)
        else:
            self.__addr = None

    def get_addr(self):
        """
        """
        return self.__addr

    def __str__(self):
        """
        """
        #

if __name__ == "__main__":

    print Host(addr=(127,0,0,1)).get_addr()
