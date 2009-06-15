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
import umpa.protocols

import umit.zion.scan.probe
import umit.zion.core.address

from umit.zion.core import options

class Packet(object):
    """
    """
    def __init__(self, ptype, addr, args=[]):
        """
        """
        self._addr = addr

        if type(self._addr) == umit.zion.core.address.IPv4:
            self._sock = socket.socket(socket.AF_INET,
                    socket.SOCK_RAW,
                    socket.IPPROTO_RAW)
        elif type(self._addr) == umit.zion.core.address.IPv6:
            self._sock = socket.socket(socket.AF_INET6,
                    socket.SOCK_RAW,
                    socket.IPPROTO_RAW)
        else:
            raise 'Unimplemented protocol.'

        if ptype == options.GET_MODE_SYN:
            tcp = TCPSYN(args[0], args[1])
            p = umpa.Packet(tcp)
            self._raw = p.get_raw()
        else:
            self._raw = []

    def send(self):
        """
        """
        print self._addr.addr
        self._sock.sendto(self._raw, (self._addr.addr, 10000))

class IPv4(umpa.protocols.IP):
    """
    """
    def __init__(self, saddr, daddr):
        """
        """
        super(IP, self).__init__()

        self.source_address = saddr
        self.destination_address = daddr

class TCP(umpa.protocols.TCP):
    """
    """
    def __init__(self, sport, dport):
        """
        """
        super(TCP, self).__init__()

        self.source_port = sport
        self.destination_port = dport

class TCPSYN(TCP):
    """
    """
    def __init__(self, sport, dport):
        """
        """
        super(TCPSYN, self).__init__(sport, dport)

        self.set_flags('control_bits', syn=True)
