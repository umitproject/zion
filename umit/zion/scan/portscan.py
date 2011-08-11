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

import copy
import random
import socket
import select

from umit.zion.scan import probe

SCAN_MODE_RANDOM = 0
SCAN_MODE_LINEAR = 1

PORTS_ALL = range(1, 2**16)
PORTS_DEFAULT = [21, 22, 23, 25, 53, 80, 110, 113, 135, 443]

class PortScan(object):
    """
    """
    def __init__(self, target=[]):
        """
        """
        self.target = target

    def append_target(self, target):
        """
        """
        self.target.append(target)

    def scan(self, ports, mode):
        """
        Abstract scan method
        """
        pass

class TCPConnectPortScan(PortScan):
    """
    """
    def __init__(self, target=[]):
        """
        """
        super(TCPConnectPortScan, self).__init__(target)

    def scan(self, ports=PORTS_DEFAULT, mode=SCAN_MODE_RANDOM):
        """
        """
        targets = []

        if mode == SCAN_MODE_RANDOM:
            random.seed()

        for t in self.target:

            if mode == SCAN_MODE_RANDOM:
                ports = copy.copy(ports)
                random.shuffle(ports)

            for p in ports:
                targets.append([t, p])

        p = probe.Probe()
        return p.probe(targets, probe.PROBE_TYPE_TCP_SYN)
