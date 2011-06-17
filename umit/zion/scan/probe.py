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

import os
import socket
import umit.zion.core.address

from threading import Thread

PROBES_LIMIT = 32
PROBE_TIMEOUT = 7 # in seconds
PROBE_MODE_RANDOM = 0
PROBE_MODE_LINEAR = 1

PROBE_TYPE_ICMP = 0
PROBE_TYPE_TCP_SYN  = 1
PROBE_TYPE_UDP = 2

def get_addr_from_name(name):
    """
    """
    addr = set()
    try:
        answer = socket.getaddrinfo(name, None)

        for a in answer:
            family, socktype, proto, canonname, sockaddr = a
            address = sockaddr[0]
            addr.add(address)
    except:
        pass

    return addr

def get_inet_type(host):
    """
    """
    inet_type = None

    if type(host.get_addr()) == umit.zion.core.address.IPv4:
        inet_type = socket.AF_INET
    elif type(host.get_addr()) == umit.zion.core.address.IPv6:
        inet_type = socket.AF_INET6

    return inet_type

class ConnectThread(Thread):
    """
    """
    def __init__(self, sock, addr):
        """
        """
        self.ans = None
        self.sock = sock
        self.addr = addr
        Thread.__init__(self)

    def run(self):
        """
        """
        self.ans = self.sock.connect_ex(self.addr)

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

    def set_timeout(self, timeout):
        """
        """
        self.__timeout = timeout

    def create_probe(self, target, probe_type, block=False):
        """
        """
        conn = None
        
        if probe_type == PROBE_TYPE_TCP_SYN:
            host, args = target
            print "++++++++"
            print(host)
            print "+++++++++"
            sock = socket.socket(get_inet_type(host), socket.SOCK_STREAM)
            sock.setblocking(block)
            sock.settimeout(self.__timeout)
            conn = ConnectThread(sock, (host.get_addr().addr, args))
            print "value of conn",
            print(conn)

        return conn

    def probe(self, targets, probe_type):
        """
        """
        result = []
        print "Value of target in probe",
        print(targets)
        print "value of self.__socks",
        print(self.__socks)

        while len(targets) + len(self.__socks) != 0:
            while len(self.__socks) < self.__limit and len(targets):
                target = targets.pop()
                print "Target value for create probe ",
                print(target)
                conn = self.create_probe(target, probe_type)
                print "======="
                #print(conn)
                #print(self.__socks)
                print "======="
                if conn:
                    self.__socks.append([target, conn])
                    print "----conn start----"
                    conn.start()


            for t, s in self.__socks:
                if s.ans != None:
                    self.__socks.remove([t, s])
                    print "---------"
                    print(t)
                    print(s.ans)
                    print "---------"
                    result.append([t, s.ans])

        return result
