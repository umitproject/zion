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
from umit.zion.scan import sniff, portscan

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
        if self.__option.has(options.OPTION_SCAN):

            print
            print 'TCP SYN port scan results'
            print '-------------------------'

            if self.__option.has(options.OPTION_PORTS):
                ports = self.__option.get(options.OPTION_PORTS)
                ports = options.parse_posts_list(ports)
            else:
                ports = portscan.PORTS_DEFAULT

            scan = portscan.TCPConnectPortScan(self.__target)
            result = scan.scan(ports)

            for (target, port), status in result:
                target.add_port(host.Port(port, host.PROTOCOL_TCP, status))

            for target in self.__target:
                print target

        if self.__option.has(options.OPTION_CAPTURE):

            print
            print 'Capturing packets'
            print '-----------------'

            s = sniff.Sniff()

            try:
                dev = self.__option.get(options.OPTION_CAPTURE)

                if dev not in s.devices.keys():
                    print 'Cannot access device: %s.' % dev

                if self.__option.has(options.OPTION_CAPTURE_AMOUNT):
                    amount = self.__option.get(options.OPTION_CAPTURE_AMOUNT)
                    s.amount = int(amount)

                if self.__option.has(options.OPTION_CAPTURE_FILTER):
                    s.filter = self.__option.get(options.OPTION_CAPTURE_FILTER)

                if self.__option.has(options.OPTION_CAPTURE_FIELDS):
                    fields = self.__option.get(options.OPTION_CAPTURE_FIELDS)
                    s.fields = fields.split(',')

                s.start(dev)
            except Exception, e:
                print 'Error', e
            except KeyboardInterrupt:
                pass

            print '\nTotal of %d packets captured.' % len(s.packets)

        print
