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
"""

__all__ = ["IPv4"]

def recognize(addr):
    """
    """
    pass

class Address(object):
    """
    """
    regexp = None
    broadcast = None

    def __init__(self, addr=None):
        """
        """
        self.__addr = addr

    @classmethod
    def is_valid(cls):
        """
        """

class IPv4(Address):
    """
    """
    regexp = "\.".join(["(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])"] * 4) + "$"
    broadcast = (255, 255, 255, 255)

    def __init__(self, addr=None):
        """
        """
        super(IPv4, self).__init__(addr)

if __name__ == "__main__":

    import re
    import sys
    print re.match(IPv4.regexp, sys.argv[1])
