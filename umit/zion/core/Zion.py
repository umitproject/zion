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
from umit.zion.scan.PortScan import PORTS_ALL, TCPConnectPortScan

OPTIONS = {"-v": "VERBOSE",
           "-s": "SCAN",
           "-i": "INTERVAL",
           "-a": "AMOUNT",
           "-l": "LIST",
           "-p": "PORTS",
           "-d": "DETECT"}


def create_posts_list(ports):
    """
    """
    ports = ports.split(",")
    rval = []

    for p in ports:
        if p.index("-"):
            a, b = p.split("-")
            try:
                c = range(int(a), int(b) + 1)
                for i in c:
                    if i not in rval:
                        rval.append(i)
            except:
                pass
        try:
            i = int(p)
            if i not in rval:
                rval.append(i)
        except:
            pass

    return rval

class Options(object):
    """
    """
    def __init__(self):
        """
        """
        pass

    def add_option(self, option, value):
        """
        """
        if option in OPTIONS.keys():
            setattr(self, OPTIONS[option], value)

class Zion(object):
    """
    """
    def __init__(self, option, target=[]):
        """
        """
        self.__option = option
        self.__target = target

    def get_option_object(self):
        """
        """
        return self.__option

    def append_target(self, target):
        """
        """
        self.__target.append(target)

    def get_target_list(self):
        """
        """
        return self.__target

    def run(self):
        """
        """
        if hasattr(self.__option, OPTIONS["-s"]):
            ports = PORTS_ALL
            if hasattr(self.__option, OPTIONS["-p"]):
                ports = create_posts_list(self.__option.PORTS)
            scan = TCPConnectPortScan(self.__target)
            scan.scan(ports)
