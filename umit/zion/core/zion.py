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

from umit.zion.core import options, host
from umit.zion.scan import portscan

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
        if hasattr(self.__option, options.OPTIONS["-s"]):
            ports = portscan.PORTS_DEFAULT
            if hasattr(self.__option, options.OPTIONS["-p"]):
                ports = options.create_posts_list(self.__option.PORTS)

            scan = portscan.TCPConnectPortScan(self.__target)
            result = scan.scan(ports)

            for (target, port), status in result:
                target.add_port(host.Port(port, host.PROTOCOL_TCP, status))
