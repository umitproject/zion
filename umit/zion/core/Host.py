# vim: set encoding=utf-8 :

# Copyright (C) 2009 Adriano Monteiro Marques.
#
# Author: João Paulo de Souza Medeiros <ignotus@umitproject.org>
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

import umit.zion.core.Address as Address

class Host(object):
    """
    Class that represent an network entity that has a least one address.
    """
    def __init__(self, addr=None):
        """
        """
        self.set_addr(addr)

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


if __name__ == "__main__":

    print Host(addr=(127,0,0,1)).get_addr()
