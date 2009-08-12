#!/usr/bin/env python
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

import os
import sys
import getopt

if not hasattr(sys, 'frozen'):
    _source_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.path.pardir))
    if os.path.exists(os.path.join(_source_path, 'bin/zion.py')):
        # Assuming zion is being executed from a svn checkout
        sys.path.insert(0, _source_path)

from umit.zion.scan import probe
from umit.zion.core import address, options, zion, host

if __name__ == '__main__':

    z = zion.Zion(options.Options(), [])

    try:
        opts, addrs = getopt.gnu_getopt(sys.argv[1:],
                options.OPTIONS_SHORT,
                options.OPTIONS_LONG)
    except getopt.GetoptError, e:
        print 'Error: %s.' % e
        sys.exit(0)

    for o in opts:
        opt, value = o
        z.get_option_object().add(opt, value)

    for a in addrs:
        if address.recognize(a) == address.Unknown:
            l = probe.get_addr_from_name(a)
            for i in l:
                try:
                    z.append_target(host.Host(i, a))
                except:
                    print "Unimplemented support to address: %s." % i
        else:
            z.append_target(host.Host(a))

    z.run()
