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
Address recognition and management module.
"""

import re

def is_name(addr):
	"""
	"""
	valid_domains = [ line.upper().replace('.', '\.').strip() 
		                              for line in open('deps/zion/umit/zion/core/domains.txt') 
		                              if line[0] != '#' ]
	r = re.compile(r'^[A-Z0-9\-]{2,63}\.(%s)$' % ('|'.join(valid_domains),))
	return True if r.match(addr.upper()) else False
		
def recognize(addr):
    """
    """
    addr_types = [IPv4, IPv6, Ethernet]

    for addr_type in addr_types:
        if addr_type(addr).is_valid():
            return addr_type
    return Unknown

class Address(object):
    """
    """
    regexp = None
    bdcast = None

    def __init__(self, addr=None):
        """
        """
        self.addr = addr

    def is_valid(self):
        """
        """
        if re.match(self.regexp, self.addr,re.IGNORECASE):
            return True
        return False

class Ethernet(Address):
    """
    """
    regexp = ':'.join(["([0-9a-fA-F]{2})"] * 6) + '$'
    bdcast = (0xff, 0xff, 0xff, 0xff, 0xff, 0xff)

    def __init__(self, addr=None):
        """
        """
        super(Ethernet, self).__init__(addr)

class IPv4(Address):
    """
    """
    regexp = "((25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)"
    bdcast = (255, 255, 255, 255)

    def __init__(self, addr=None):
        """
        """
        super(IPv4, self).__init__(addr)

class IPv6(Address):
    """
    This regex is complete for all format of Ipv6 address. But only it doesnot deal with case senstive part. It is only
    for upper case word like FE80::FAC but does not match with fe80::fac. To do so re.IGNORECASE is added while matching. 
    """
    
    regexp = "^(?:(?:(?:[A-F0-9]{1,4}:){6}|(?=(?:[A-F0-9]{0,4}:){0,6}(?:[0-9]{1,3}\.){3}[0-9]{1,3}$)(([0-9A-F]{1,4}:){0,5}|:)((:[0-9A-F]{1,4}){1,5}:|:))(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}|(?=(?:[A-F0-9]{0,4}:){0,7}[A-F0-9]{0,4}$)(([0-9A-F]{1,4}:){1,7}|:)((:[0-9A-F]{1,4}){1,7}|:))$"
    bdcast = (0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff)

    def __init__(self, addr=None):
        """
        """
        super(IPv6, self).__init__(addr)

class Unknown(object):
    """
    """

if __name__ == '__main__':

    import sys
    print recognize(sys.argv[1])
