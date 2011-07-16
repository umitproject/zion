# vim: set encoding=utf-8 :

# Copyright (C) 2009 Adriano Monteiro Marques.
#
# Author: Joao Paulo de Souza Medeiros <ignotus@umitproject.org>
#         Gaurav Ranjan < g.ranjan143@gmail.com >
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
import sqlite3
import sys
import json
import cPickle
from math import sqrt

from umit.clann import som, matrix
from umit.zion.core import options, host, pmatrix
from umit.zion.scan import sniff, portscan, forge
from umit.core.BasePaths import UMIT_DB_DIR

FORGE_FILTER = 'src host %s and src port %s and dst host %s and dst port %s'
AMOUNT_OS_DETECTION = 100
AMOUNT_HONEYD_DETECTION = 5
SEND_INTERVAL = 0.1
SYNPROXY_INTERVAL = 1
METHOD_ALPHA = 1
METHOD_BETA = 2
EPOCHS = 500#1800
ALPHA_LIMIT = 0.1

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
        self.notify('update_status', "Host scanning started\n")

        if self.__option.has(options.OPTION_PORTS):
            ports = self.__option.get(options.OPTION_PORTS)
            ports = options.parse_posts_list(ports)
        else:
            ports = portscan.PORTS_DEFAULT


        scan = portscan.TCPConnectPortScan(self.__target)
        result = scan.scan(ports)
        
        for (target, port), status in result:
            target.add_port(host.Port(port, host.PROTOCOL_TCP, status))


        self.notify('scan_finished', self.__target[0])

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

    def do_forge(self, fields=None):
        """
        """
        mode = self.__option.get(options.OPTION_FORGE)

        addr = self.__option.get(options.OPTION_FORGE_ADDR)

        port = random.randint(1024, 65535)
        

        s = sniff.Sniff()

        if mode == options.FORGE_MODE_SYN:
            self.do_scan()


            self.notify('update_status', 'Capturing packets\n')
            print(fields)

            if fields!=None:
                s.fields = fields


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


        s.filter = FORGE_FILTER % (target.get_addr().addr, target_port,
                addr, port)
        print "_____________________________"
        print "src host %s and src port %s and dst host %s and dst port %s" % (target.get_addr().addr, target_port,addr, port)
        print "_____________________________"

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
            print "Packet capure Finish"
            packet.stop()
        except Exception, e:
            print 'Error:', e
        except KeyboardInterrupt:
            packet.stop()


    def run(self, outq=None):
        """
        """
        self.__outq = outq

        if self.__option.has(options.OPTION_HELP):

            print options.HELP_TEXT

        elif self.__option.has(options.OPTION_DETECT):

            self.notify('update_status', 'OS Detection Started\n')

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
            self.do_forge(['tcp.seq'])

            self.notify('update_status', 'Creating time series\n')

            print 'Calculating PRNG'
            Rt = self.calculate_PRNG()

            if Rt is not None:
                self.notify('update_status', 'Building attractors\n')

                print 'Creating attractors'
                self.__classification(Rt)

                self.notify('update_status', 'Performing matching\n')

                print 'Matching'
                result = self.__matching()

                self.notify('matching_finished', result)

            else:
                self.notify('update_status', 'No data to build attractors\n')
                result = None


        elif self.__option.has(options.OPTION_SYNPROXY):

            self.notify('update_status', 'Syn Proxy Detection Started\n\n')

            synproxy = self.synproxy_detection()
            if synproxy==True:
                print 'Target is synproxy'
            else:
                print 'Target isnt synproxy'

            self.notify('synproxy_finished', synproxy)

        elif self.__option.has(options.OPTION_HONEYD):

            self.notify('update_status', 'Honeyd Detection Started\n')

            honeyd = self.honeyd_detection()
            if honeyd==False:
                print 'Target isnt honeyd'
            else:
                print 'Target is honeyd'

            self.notify('honeyd_finished', honeyd)

        elif self.__option.has(options.OPTION_FORGE):

            self.notify('update_status', 'Forge started\n')

            print
            print 'Getting packets'
            print '---------------'

            self.do_forge()

        elif self.__option.has(options.OPTION_SCAN):

            self.notify('update_status', 'Scanning host\n')

            print
            print 'TCP SYN port scan results'
            print '-------------------------'

            self.do_scan()

        elif self.__option.has(options.OPTION_CAPTURE):

            print
            print 'Capturing packets'
            print '-----------------'

            self.do_capture()

        else:
            print options.HELP_TEXT


    def honeyd_detection(self):
        """ Detect if target are an honeyd. """
        # configure parameters for honeyd detection
        if not self.__option.has(options.OPTION_CAPTURE_AMOUNT):
            self.__option.add('--capture-amount',AMOUNT_HONEYD_DETECTION)
        self.__option.add('-f','syn')

        self.do_forge(['tcp.seq'])
        Rt = self.calculate_PRNG()
        print(Rt)


        if Rt is not None and len(Rt) > 0:

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



    def synproxy_detection(self):
        """ Detect if target is an syn proxy. """

        # configure parameters for honeyd detection
        if not self.__option.has(options.OPTION_CAPTURE_AMOUNT):
            self.__option.add('--capture-amount',1)
        self.__option.add('-f','syn')

        self.notify('update_status','Searching for open ports\n')

        target = self.__target[0]

        # search for open ports in target
        self.do_scan()
        ports = target.get_open_ports()

        if len(ports) > 0:

            self.notify('update_status','Generate random ports\n')

            # TODO: do a better rand port choice algorithm (maybe an UMPA function?)
            origin_port1 = random.randint(1024, 65535)
            while True:
                origin_port2 = random.randint(1024, 65535)
                if origin_port2!=origin_port1:
                    break

            s = sniff.Sniff()
            addr = self.__option.get(options.OPTION_FORGE_ADDR)

            self.notify('update_status','Sending packets\n')
            s.fields = ['tcp.seq']
            self.do_forge_mode_syn(s, target, ports[0], addr, origin_port1)
            isn1 = self.__capture_result[0][1]
            time.sleep(SYNPROXY_INTERVAL)
            self.do_forge_mode_syn(s, target, ports[0], addr, origin_port2)
            isn2 = self.__capture_result[0][1]
            time.sleep(SYNPROXY_INTERVAL)
            self.do_forge_mode_syn(s, target, ports[0], addr, origin_port1)
            isn3 = self.__capture_result[0][1]

            if isn1 != isn2 and isn1 == isn3:
                return True
            else:
                return False

        return None


    def calculate_PRNG(self):
        """
        Calculate Pseudo Random Number Generator from ISN captured.
        """

        if len(self.__capture_result) == 0:
            print 'Error: no results available'
            return None
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
        if Rt is not None:
            max_val = max(Rt)
            min_val = min(Rt)
            ratio = 2/(max_val-min_val)

            self.__som = som.new(2,(30,30))
            self.__matrix = matrix.new(len(Rt)-1,2)

            for i in range(len(Rt)-1):
                x = Rt[i+1]
                y = Rt[i]
                self.__attractors.append((x, y))
                matrix.set(self.__matrix, i, 0, x)
                matrix.set(self.__matrix, i, 1, y)

            self.notify('attractors_built', self.__attractors)

            som.caracterization(self.__som, self.__matrix, EPOCHS)

    def __matching(self):
        """
        Match fingerprint with database
        """
        dmin = sys.maxint
        id_min = None

        conn = sqlite3.connect(UMIT_DB_DIR+'/db.sqlite')
        c = conn.cursor()
        c.execute('SELECT software.pk, s_attractor.fp FROM software INNER JOIN fingerprint ON software.pk = fingerprint.fk_software INNER JOIN s_attractor ON s_attractor.pk = fingerprint.fk_sig1')

        for fingerprint in c:
            attractor = cPickle.loads(str(fingerprint[1]))
            base = attractor.convert()
            d = som.classification(self.__som, base, ALPHA_LIMIT, METHOD_ALPHA)
            if d < dmin:
                dmin = d
                id_min = fingerprint[0]

        details = None
        if id_min!=None:
            for vendor_name, os_name, os_version in c.execute('SELECT vendor.name, name.name, name.version FROM software INNER JOIN vendor ON software.fk_vendor = vendor.pk INNER JOIN name ON software.fk_name = name.pk WHERE software.pk = ?',(id_min,)):
                details = {'vendor_name': vendor_name, 'os_name': os_name, 'os_version': os_version, 'metric': dmin}
                print 'Vendor name: %s\nOS name: %s\nOS version: %s\nMetric: %d' % (vendor_name, os_name, os_version, dmin)
        else:
            print 'no fingerprints available in database'

        return details

    def get_attractors(self):
        """ Return the list of attractors. """
        return self.__attractors

    def notify(self, signal, param=None):
        """
        If a out queue exists, output the information.
        """
        if self.__outq!=None:
            self.__outq.put((signal, param))
