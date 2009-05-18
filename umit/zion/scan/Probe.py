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

PROBES_LIMIT = 21
PROBE_TIMEOUT = 1 # in seconds
PROBE_MODE_RANDOM = 0
PROBE_MODE_LINEAR = 1

PROBE_TYPE_ICMP = 0
PROBE_TYPE_TCP_SYN  = 1
PROBE_TYPE_UDP = 2

class Probe(object):
    """
    """
    def __init__(self, limit=PROBES_LIMIT, timeout=PROBE_TIMEOUT):
        """
        """
        self.__socks = []
        self.__limit = limit
        self.__timeout = timeout

    def set_limit(self, limit):
        """
        """
        self.__limit = limit

    def set_limit(self, timeout):
        """
        """
        self.__timeout = timeout

    def fire_probe(self, host, probe_type, args, block=False):
        """
        """
        inet_type = None
        sock = None

        if type(host.get_addr()) == umit.zion.core.Address.IPv4:
            inet_type = socket.AF_INET
        elif type(host.get_addr()) == umit.zion.core.Address.IPv6:
            inet_type = socket.AF_INET6

        if probe_type = PROBE_TYPE_TCP_SYN:
            sock = socket.socket(inet_type, socket.SOCK_STREAM)
            sock.setblocking(block)
            sock.connect_ex((host.get_addr(), args))

        return sock

    def probe(self, targets):
        """
        """
        while True:
            while len(self.__socks) < self.__limit and len(targets):
                target = targets.pop()
                host, probe_type, args = target[0], target[1], target[1:]
                sock = self.fire_probe(host, probe_type, args)

                if sock:
                    self.__socks.append(sock)

            #rlist, wlist, xlist = select.select(self.__socks, [], [])

class TCPConnectProbe(object):
    """
    """
    DEFAULT_PORT = 80

    def __init__(self, hosts):
        """
        """
        self.__hosts = hosts

    def probe(self, mode=PROBE_MODE_RANDOM):
        """
        """
        pass
