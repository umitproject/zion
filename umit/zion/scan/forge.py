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

import time
import socket

import umit.umpa.protocols
import umit.zion.core.address

from umit.zion.core import options
from threading import Thread

class Packet(Thread):
    """
    """
    def __init__(self, ptype, saddr, daddr, args=[]):
        """
        """
        Thread.__init__(self)
        self.flag = False
        self.interval = 0.01
        self._addr = daddr

        if type(self._addr) == umit.zion.core.address.IPv4:
            self._sock = socket.socket(socket.AF_INET,
                    socket.SOCK_RAW,
                    socket.IPPROTO_RAW)
        elif type(self._addr) == umit.zion.core.address.IPv6:
            self._sock = socket.socket(socket.AF_INET6,
                    socket.SOCK_RAW,
                    socket.IPPROTO_TCP)
        else:
            raise 'Unimplemented protocol.'

        self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if ptype == options.FORGE_MODE_SYN:
            if type(self._addr) == umit.zion.core.address.IPv4:
                ip = IPv4(saddr, self._addr.addr)
                tcp = TCPSYN(args[0], args[1])
                self._packet = umit.umpa.Packet(ip, tcp)
            else:
                raise 'UMPA unimplemented protocol.'
        else:
            self._packet = None

    def send(self):
        """
        """
        self._sock.sendto(self._packet.get_raw(), (self._addr.addr, 0))

    def stop(self):
        """
        """
        self.flag = False

    def run(self):
        """
        """
        self.flag = True
        while self.flag:
            if self.interval:
                time.sleep(self.interval)
            self.send()

class IPv4(umit.umpa.protocols.IP):
    """
    """
    def __init__(self, saddr, daddr):
        """
        """
        super(IPv4, self).__init__()

        self.src = saddr
        self.dst = daddr

class TCP(umit.umpa.protocols.TCP):
    """
    """
    def __init__(self, sport, dport):
        """
        """
        super(TCP, self).__init__()

        self.srcport = sport
        self.dstport = dport

class TCPSYN(TCP):
    """
    """
    def __init__(self, sport, dport):
        """
        """
        super(TCPSYN, self).__init__(sport, dport)

        self.set_flags('flags', syn=True)
