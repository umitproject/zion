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

import random

from umit.clann import som
from umit.zion.core import options, host
from umit.zion.scan import sniff, portscan, forge

FORGE_FILTER = 'src host %s and src port %s and dst host %s and dst port %s'

class Zion(object):
    """
    """
    def __init__(self, option, target=[]):
        """
        """
        self.__option = option
        self.__target = target
        self.__attractors = []
        self.__isn = []

    def get_option_object(self):
        """
        """
        return self.__option
    
    def reset_options(self):
        """
        """
        self.__option = options.Options()

    def append_target(self, target):
        """
        """
        self.__target.append(target)

    def get_target_list(self):
        """
        """
        return self.__target

    def do_scan(self):
        """
        """
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
            
    def do_capture(self, dev=None):
        """
        """
        s = sniff.Sniff()
        s.som = self.__som

        try:
            if not dev:
                dev = self.__option.get(options.OPTION_CAPTURE)

            if self.__option.has(options.OPTION_CAPTURE_AMOUNT):
                amount = self.__option.get(options.OPTION_CAPTURE_AMOUNT)
                s.amount = int(amount)
            else:
                # TODO: what should be default value ?
                s.amount = 10

            if self.__option.has(options.OPTION_CAPTURE_FILTER):
                s.filter = self.__option.get(options.OPTION_CAPTURE_FILTER)

            if self.__option.has(options.OPTION_CAPTURE_FIELDS):
                fields = self.__option.get(options.OPTION_CAPTURE_FIELDS)
                s.fields = fields.split(',')

            self.__isn = s.start(dev)
        except Exception, e:
            print 'Error:', e
        except KeyboardInterrupt:
            pass

    def do_forge(self):
        """
        """
        mode = self.__option.get(options.OPTION_FORGE)
        addr = self.__option.get(options.OPTION_FORGE_ADDR)
        port = random.randint(1024, 65535)

        s = sniff.Sniff()

        if mode == options.FORGE_MODE_SYN:
            self.do_scan()

            for t in self.__target:

                ports = t.get_open_ports()

                if len(ports):
                    amount = self.__option.get(options.OPTION_CAPTURE_AMOUNT)

                    if amount:
                        s.amount = int(amount)

                    s.fields = ['tcp.seq']
                    s.filter = FORGE_FILTER % (t.get_addr().addr, ports[0],
                            addr, port)
                    packet = forge.Packet(options.FORGE_MODE_SYN,
                            addr,
                            t.get_addr(),
                            (port, ports[0]))

                    interval = self.__option.get(options.OPTION_SEND_INTERVAL)

                    if interval:
                        packet.interval = float(interval)

                    print
                    print s.filter
                    print

                    try:
                        packet.start()
                        s.start(self.__option.get(options.OPTION_CAPTURE))
                        packet.stop()
                    except Exception, e:
                        print 'Error:', e
                    except KeyboardInterrupt:
                        packet.stop()

        else:
            print 'Unimplemented forge mode %s.' % mode

    def run(self):
        """
        """
        self.__som = som.new(10,(30,30))
        
        if self.__option.has(options.OPTION_HELP):

            print options.HELP_TEXT

        if self.__option.has(options.OPTION_FORGE):

            print
            print 'Getting packets'
            print '---------------'

            self.do_forge()

        elif self.__option.has(options.OPTION_SCAN):

            print
            print 'TCP SYN port scan results'
            print '-------------------------'

            self.do_scan()

        elif self.__option.has(options.OPTION_CAPTURE):

            print
            print 'Capturing packets'
            print '-----------------'

            self.do_capture()
            
            self.__classification()

        else:
            print options.HELP_TEXT 
                    
        
    def __classification(self):
        """ Get attractors and put them in SOM. """
        
        ordered = True
        
        # verify if isn numbers are ordered ascendly
        for i in range(1,len(self.__isn)):
            if self.__isn[i] < self.__isn[i-1]:
                ordered = False
                break
            
        Rt = []
        self.__attractors = []

        if ordered==False:
            Rt = self.__isn
        else:
            for i in range(0, len(self.__isn)-1):
                Rt.append(self.__isn[i+1] - self.__isn[i])
                
        for i in range(0, len(Rt)-1):
            self.__attractors.append((Rt[i+1],Rt[i]))
         
        # TODO: confirm how train works
        #som.train(self.__som, matrix, 1800)

        
    def get_attractors(self):
        """
        """
        return self.__attractors