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
import time
from math import sqrt

from umit.clann import som, matrix
from umit.zion.core import options, host
from umit.zion.scan import sniff, portscan, forge

FORGE_FILTER = 'src host %s and src port %s and dst host %s and dst port %s'
AMOUNT_OS_DETECTION = 2000
AMOUNT_HONEYD_DETECTION = 25
SEND_INTERVAL = 0.1
SYNPROXY_INTERVAL = 1

class Zion(object):
    """
    """
    def __init__(self, option, target=[]):
        """
        """
        self.__option = option
        self.__target = target
        self.__capture_result = []
        self.__attractors = []

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

        try:
            if not dev:
                dev = self.__option.get(options.OPTION_CAPTURE)

            if self.__option.has(options.OPTION_CAPTURE_AMOUNT):
                amount = self.__option.get(options.OPTION_CAPTURE_AMOUNT)
                s.amount = int(amount)

            if self.__option.has(options.OPTION_CAPTURE_FILTER):
                s.filter = self.__option.get(options.OPTION_CAPTURE_FILTER)

            if self.__option.has(options.OPTION_CAPTURE_FIELDS):
                fields = self.__option.get(options.OPTION_CAPTURE_FIELDS)
                s.fields = fields.split(',')

            self.__capture_result = s.start(dev)
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
                    self.do_forge_mode_syn(s, t, ports[0], addr, port)

        else:
            print 'Unimplemented forge mode %s.' % mode

            
    def do_forge_mode_syn(self, s, target, target_port, addr, port):
        """
        """
        
        amount = self.__option.get(options.OPTION_CAPTURE_AMOUNT)

        if amount:
            s.amount = int(amount)

        s.fields = ['tcp.seq']
        s.filter = FORGE_FILTER % (target.get_addr().addr, target_port,
                addr, port)
        packet = forge.Packet(options.FORGE_MODE_SYN,
                addr,
                target.get_addr(),
                (port, target_port))

        interval = self.__option.get(options.OPTION_SEND_INTERVAL)

        if interval:
            packet.interval = float(interval)

        print
        print s.filter
        print

        try:
            packet.start()
            self.__capture_result = s.start(self.__option.get(options.OPTION_CAPTURE))
            packet.stop()
        except Exception, e:
            print 'Error:', e
        except KeyboardInterrupt:
            packet.stop()
                        

    def run(self):
        """
        """
        self.synproxy_detection(self.__target[0])
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
                        
        elif self.__option.has(options.OPTION_DETECT):
            
            print
            print 'OS Detection'
            print '------------'
            
            # configure parameters for OS detection
            if not self.__option.has(options.OPTION_CAPTURE_AMOUNT):
                self.__option.add('--capture-amount',AMOUNT_OS_DETECTION)
            if not self.__option.has(options.OPTION_SEND_INTERVAL):
                self.__option.add('-i',SEND_INTERVAL)                
            self.__option.add('-f','syn')
            
            print 'Capturing packets'
            self.do_forge()

            print 'Calculating PRNG'
            Rt = self.calculate_PRNG()
            
            print 'Creating attractors'
            self.__classification(Rt)
                
        elif self.__option.has(options.OPTION_CAPTURE):

            print
            print 'Capturing packets'
            print '-----------------'

            self.do_capture()                

        else:
            print options.HELP_TEXT
            
            
    def honeyd_detection(self,target):
        """ Detect if target are an honeyd. """
        
        print 'start honeyd detection'
        self.__target = []
        self.append_target(target)
        
        # configure parameters for honeyd detection
        if not self.__option.has(options.OPTION_CAPTURE_AMOUNT):
            self.__option.add('--capture-amount',AMOUNT_HONEYD_DETECTION)
        self.__option.add('-f','syn')
                
        self.do_forge()
        Rt = self.calculate_PRNG()
        
        if len(Rt) > 0:

            # verify cycles
            for i in range(0,5):
                values = set(Rt[i::5])
                if not len(values)==1:
                    return False
                    
            # verify constant increments
            cycle = Rt[:5]
            increments = []
            for i in range(0,5):
                increments.append(cycle[(i+1)%5]-cycle[i%5])
            incs = set(increments)
            for k in incs:
                if increments.count(k)==4:
                    return True

            return False                
        else:
            return False

        
    def synproxy_detection(self, target):
        """ Detect if target is an syn proxy. """
        
        print 'start syn proxy detection'
        self.__target = []
        self.append_target(target)
        
        # configure parameters for honeyd detection
        if not self.__option.has(options.OPTION_CAPTURE_AMOUNT):
            self.__option.add('--capture-amount',1)
        self.__option.add('-f','syn')
        
        # search for open ports in target
        self.do_scan()
        ports = target.get_open_ports()
        
        origin_port1 = random.randint(1024, 65535)
        while True:
            origin_port2 = random.randint(1024, 65535)
            if origin_port2!=origin_port1:
                break

        s = sniff.Sniff()
        addr = self.__option.get(options.OPTION_FORGE_ADDR)
        
        self.do_forge_mode_syn(s, target, ports[0], addr, origin_port1)
        isn1 = self.__capture_result[0][1]
        time.sleep(SYNPROXY_INTERVAL)
        self.do_forge_mode_syn(s, target, ports[0], addr, origin_port2)
        isn2 = self.__capture_result[0][1]
        time.sleep(SYNPROXY_INTERVAL)
        self.do_forge_mode_syn(s, target, ports[0], addr, origin_port1)
        isn3 = self.__capture_result[0][1]
        
        print 'isns:'
        print isn1
        print isn2
        print isn3
        
        if isn1!=isn2 and isn1==isn3:
            return True
        else:
            return False

            
    def calculate_PRNG(self):
        """ Calculate Pseudo Random Number Generator from ISN captured. """
        
        if len(self.__capture_result) == 0:
            print 'Error: no results available'
        else:
            isn = []
            for i in range(len(self.__capture_result)):
                if self.__capture_result[i][1][0] <> 'None':
                    isn.append(int(self.__capture_result[i][1][0]))
        
        ordered = True
        
        # verify if isn numbers are ordered ascendly
        for i in range(1,len(isn)):
            if isn[i] < isn[i-1]:
                ordered = False
                break
            
        Rt = []
        
        if ordered==False:
            Rt = isn
        else:
            for i in range(len(isn)-1):
                Rt.append(isn[i+1] - isn[i])
                    
        return Rt
    
        
    def __classification(self,Rt):
        """ Get attractors and put them in SOM. """
                
        self.__attractors = []
                
        # normalize results
        max_val = max(Rt)
        min_val = min(Rt)
        ratio = 2/(max_val-min_val)
        
        self.__som = som.new(10,(30,30))
        self.__matrix = matrix.new(len(Rt)-1,2)
        
        for i in range(len(Rt)-1):
            x = (Rt[i+1]-min_val)*ratio-1
            y = (Rt[i]-min_val)*ratio-1
            self.__attractors.append((x, y))
            matrix.set(self.__matrix, i, 0, x)
            matrix.set(self.__matrix, i, 1, y)

        # TODO: confirm how train works
        som.train(self.__som, self.__matrix, 1800)        

        
    def get_attractors(self):
        """
        """
        return self.__attractors