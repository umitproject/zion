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

from umit.zion.scan import portscan

OPTION_SCAN = 0
OPTION_CAPTURE = 1
OPTION_CAPTURE_AMOUNT = 2
OPTION_CAPTURE_FILTER = 3
OPTION_CAPTURE_FIELDS = 4
OPTION_CAPTURE_SAVE = 5
OPTION_VERBOSE = 6
OPTION_PORTS = 7
OPTION_DETECT = 8
OPTION_FORGE = 9
OPTION_FORGE_ADDR = 10
OPTION_SEND_INTERVAL = 11

FORGE_MODE_SYN = 'syn'

OPTIONS = {'-v':                OPTION_VERBOSE,
           '-c':                OPTION_CAPTURE,
           '--capture':         OPTION_CAPTURE,
           '--capture-amount':  OPTION_CAPTURE_AMOUNT,
           '--capture-filter':  OPTION_CAPTURE_FILTER,
           '--capture-fields':  OPTION_CAPTURE_FIELDS,
           '--capture-save':    OPTION_CAPTURE_SAVE,
           '-s':                OPTION_SCAN,
           '--scan':            OPTION_SCAN,
           '-p':                OPTION_PORTS,
           '--ports':           OPTION_PORTS,
           '-f':                OPTION_FORGE,
           '--forge':           OPTION_FORGE,
           '--forge-addr':      OPTION_FORGE_ADDR,
           '-i':                OPTION_SEND_INTERVAL,
           '-d':                OPTION_DETECT,
           '--detect':          OPTION_DETECT}

OPTIONS_SHORT = 'c:d:i:p:f:sv'
OPTIONS_LONG = ['capture=',
                'capture-amount=',
                'capture-filter=',
                'capture-fields=',
                'capture-save=',
                'scan',
                'forge=',
                'forge-addr=',
                'ports=',
                'detect=']

def parse_posts_list(ports):
    """
    """
    if ports == "all":
        return portscan.PORTS_ALL

    ports = ports.split(",")
    rval = []

    for p in ports:
        if p.find("-") != -1:
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
        self.__options = {}

    def get_options(self):
        """
        """
        return self.__options

    def has(self, option):
        """
        """
        if option in self.__options.keys():
            return True
        return False

    def get(self, option):
        """
        """
        if option in self.__options.keys():
            return self.__options[option]
        return None

    def add(self, option, value=None):
        """
        """
        if option in OPTIONS.keys():
            self.__options[OPTIONS[option]] = value
