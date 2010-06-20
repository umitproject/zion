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

from umit.zion.core import address

HOST_STATUS_UP = 'up'
HOST_STATUS_DOWN = 'down'
HOST_STATUS_UNREACHABLE = 'unreachable'

PORT_STATE_OPEN = 0
PORT_STATE_CLOSED = 111
PORT_STATE_FILTERED = 11

PORT_STATE_STR = {PORT_STATE_OPEN: 'open',
                  PORT_STATE_FILTERED: 'filtered',
                  PORT_STATE_CLOSED: 'closed'}

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
    def __init__(self, addr=None, name=None):
        """
        """
        self.set_addr(addr)
        self.__name = name
        self.__ports = {}
        self.__status = HOST_STATUS_DOWN

    def set_status(self, status):
        """
        """
        self.__status = status

    def add_port(self, port):
        """
        """
        self.__ports[port.number] = port

        if port.status in [PORT_STATE_OPEN, PORT_STATE_CLOSED]:
            self.set_status(HOST_STATUS_UP)
        elif port.status == HOST_STATUS_UNREACHABLE:
            print port.number, port.status
            self.set_status(HOST_STATUS_UNREACHABLE)

    def set_addr(self, addr):
        """
        """
        if addr:
            addr_type = address.recognize(addr)
            if addr_type:
                self.__addr = addr_type(addr)
        else:
            self.__addr = None

    def get_addr(self):
        """
        """
        return self.__addr

    def get_open_ports(self):
        """
        """
        result = []
        for port in self.__ports.values():
            if port.status == PORT_STATE_OPEN:
                result.append(port.number)

        return result
    
    def get_ports(self):
        """Return ports scanned."""
        return self.__ports

    def __str__(self):
        """
        """
        s = ['']

        if self.__name:
            s.append('%s' % self.__name)

        s.append('%s (%s)' % (self.get_addr().addr, self.__status))

        if self.__status == HOST_STATUS_UP:
            ports = self.__ports.keys()
            ports.sort()
            for p in ports:
                port = self.__ports[p]
                s.append(' %d %s' % (port.number, PORT_STATE_STR[port.status]))

        return '\n'.join(s)

if __name__ == "__main__":

    print Host(addr=("127.0.0.1")).get_addr()
