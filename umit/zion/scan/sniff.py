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

import pcap
import struct

import umpa.sniffing

class Frame(object):
    """
    """
    header_size = None   # Base header size.
    header_format = None

    def __init__(self, buffer):
        """
        """
        self._raw = buffer

    def __str__(self):
        """
        """
        s = ['+ Frame']
        raw = struct.unpack('B' * len(self._raw), self._raw)
        col = 16

        for i in range(len(raw) / col):
            s.append('| ' + '%.2x ' * col % (raw[i * col: (i + 1) * col]))

        rest = len(raw) % col
        i = len(raw) / col
        if rest:
            s.append('| ' + '%.2x ' * rest % (raw[i * col: i * col + rest]))

        s[-1] = s[-1].replace('| ', '|_')

        return '\n'.join(s)

class SLL(Frame):
    """
    """
    # FIXME: seems that SLL protocol allow headers bigger than 16 bytes. So, a
    # complete disassemble is needed to avoid problems.
    header_size = 16
    header_format = '>HHH8BH'

    def __init__(self, buffer):
        """
        """
        super(SLL, self).__init__(buffer)
        self.payload = self._raw[self.header_size:]
        self._fields = struct.unpack(self.header_format,
                self._raw[:self.header_size])

        # Assuming structure found in: `libpcap/pcap/sll.h,v 1.3'

        self.pkttype = self._fields[0]
        self.hatype = self._fields[1]
        self.halen = self._fields[2]
        self.addr = ':'.join(['%.2x'] * 8) % (self._fields[3:11])
        self.protocol = self._fields[11]

    def __str__(self):
        """
        """
        s = ['+ SLL']
        s.append('| (pkttype 0x%.4x)' % self.pkttype)
        s.append('| (hatype 0x%.4x)' % self.hatype)
        s.append('| (halen 0x%.4x)' % self.halen)
        s.append('| (addr %s)' % self.addr)
        s.append('|_(protocol 0x%.4x)' % self.protocol)

        return "\n".join(s)

class Ethernet(Frame):
    """
    """
    header_size = 14
    header_format = '>6B6BH'

    def __init__(self, buffer):
        """
        """
        super(Ethernet, self).__init__(buffer)
        self.payload = self._raw[self.header_size:]
        self._fields = struct.unpack(self.header_format,
                self._raw[:self.header_size])

        self.dst = ':'.join(['%.2x'] * 6) % (self._fields[0:6])
        self.src = ':'.join(['%.2x'] * 6) % (self._fields[6:12])
        self.type = self._fields[12]

    def __str__(self):
        """
        """
        s = ['+ Ethernet']
        s.append('| (dst %s)' % self.dst)
        s.append('| (src %s)' % self.src)
        s.append('|_(type 0x%.4x)' % self.type)

        return '\n'.join(s)

class IPv4(Frame):
    """
    """
    header_size = 20
    header_format = '>BBHHHBBH4B4B'

    def __init__(self, buffer):
        """
        """
        super(IPv4, self).__init__(buffer)
        self._fields = struct.unpack(self.header_format,
                self._raw[:self.header_size])

        self.version = self._fields[0] >> 4
        self.hdr_len = self._fields[0] & 0x0F
        self.tos = self._fields[1]
        self.len = self._fields[2]
        self.id = self._fields[3]
        self.flags = (self._fields[4] & 0xE000) >> 13
        self.frag_offset = (self._fields[4] & 0x1fff)
        self.ttl = self._fields[5]
        self.proto = self._fields[6]
        self.checksum = self._fields[7]
        self.src = '%d.%d.%d.%d' % (self._fields[8:12])
        self.dst = '%d.%d.%d.%d' % (self._fields[12:16])

        # FIXME: verify header size
        self.payload = self._raw[self.header_size:]

    def __str__(self):
        """
        """
        s = ['+ IPv4']
        s.append('| (version 0x%x)' % self.version)
        s.append('| (hdr_len 0x%x)' % self.hdr_len)
        s.append('| (tos 0x%.2x)' % self.tos)
        s.append('| (len 0x%.4x)' % self.len)
        s.append('| (id 0x%.4x)' % self.id)
        s.append('| (flags 0x%x)' % self.flags)
        s.append('| (frag_offset 0x%.4x)' % self.frag_offset)
        s.append('| (ttl 0x%.2x)' % self.ttl)
        s.append('| (proto 0x%.2x)' % self.proto)
        s.append('| (checksum 0x%.2x)' % self.checksum)
        s.append('| (src %s)' % self.src)
        s.append('|_(dst %s)' % self.dst)

        return '\n'.join(s)

class IPv6(Frame):
    """
    """
    header_size = 40
    header_format = '>IHBB8H8H'

    def __init__(self, buffer):
        """
        """
        super(IPv6, self).__init__(buffer)
        self.payload = self._raw[self.header_size:]
        self._fields = struct.unpack(self.header_format,
                self._raw[:self.header_size])

        self.version = self._fields[0] >> 28
        self.clas = (self._fields[0] & 0x0FF00000) >> 8 # Should be self.class
        self.flow = (self._fields[0] & 0x000FFFFF)
        self.plen = self._fields[1]
        self.nxt = self._fields[2]
        self.hlim = self._fields[3]
        self.dst = ':'.join(["%.4x"] * 8) % (self._fields[4:12])
        self.src = ':'.join(["%.4x"] * 8) % (self._fields[12:20])

    def __str__(self):
        """
        """
        s = ['+ IPv6']
        s.append('| (version 0x%x)' % self.version)
        s.append('| (clas 0x%.2x)' % self.clas)
        s.append('| (flow 0x%.3x)' % self.flow)
        s.append('| (plen 0x%.4x)' % self.plen)
        s.append('| (nxt 0x%.2x)' % self.nxt)
        s.append('| (hlim 0x%.2x)' % self.hlim)
        s.append('| (src %s)' % self.src)
        s.append('|_(dst %s)' % self.dst)

        return '\n'.join(s)

class TCP(Frame):
    """
    """
    header_size = 20
    header_format = '>HHIIBBHHH'

    def __init__(self, buffer):
        """
        """
        super(TCP, self).__init__(buffer)
        self._fields = struct.unpack(self.header_format,
                self._raw[:self.header_size])

        self.srcport = self._fields[0]
        self.dstport = self._fields[1]
        self.seq = self._fields[2]
        self.ack = self._fields[3]
        self.hdr_len = self._fields[4] >> 4
        self.reserved = self._fields[4] & 0x0F
        self.flags = self._fields[5]
        self.window_size = self._fields[6]
        self.checksum = self._fields[7]
        self.urgent_pointer = self._fields[8]

        # FIXME: verify header size
        self.payload = self._raw[self.header_size:]

    def __str__(self):
        """
        """
        s = ['+ TCP']

        s.append('| (srcport %d)' % self.srcport)
        s.append('| (dstport %d)' % self.dstport)
        s.append('| (seq %d)' % self.seq)
        s.append('| (ack %d)' % self.ack)
        s.append('| (hdr_len 0x%x)' % self.hdr_len)
        s.append('| (reserved 0x%x)' % self.reserved)
        s.append('| (flags 0x%.2x)' % self.flags)
        s.append('| (window_size 0x%.4x)' % self.window_size)
        s.append('| (checksum 0x%.4x)' % self.checksum)
        s.append('|_(urgent_pointer 0x%.4x)' % self.urgent_pointer)

        return "\n".join(s)

FRAME_TYPES = {'sll': SLL,
               'ether': Ethernet,
               'ipv4': IPv4,
               'ipv6': IPv6,
               'tcp': TCP}

class Packet(object):
    """
    """
    def __init__(self, timestamp, buffer, linktype):
        """
        """
        self.__timestamp = timestamp
        self.__linktype = linktype
        self.__buffer = buffer
        self.__packet = None

    def get_timestamp(self):
        """
        """
        return self.__timestamp

    def get_packet(self):
        """
        """
        return self.__packet

    def disassemble(self):
        """
        """
        self.__packet = []
        next_type = None

        # Disassembling first frame.
        # There are two options to make this work right:
        #
        #   1. Disassembly the link layer and see what the next protocol on
        #      their data fields;
        #   2. Ignore the first `n' bytes of link layer data. Where `n' stands
        #      for size of link layer protocol header.
        #
        # The second one can fail when the link layer protocol has a variable
        # header length. So, is not correct do this way. Moreover, we can be
        # sure what is the next protocol without looking at link layer header.
        # For while we will assume that IP is next packet when the link layer
        # disassembling is not implemented
        if self.__linktype == pcap.DLT_EN10MB:
            e = Ethernet(self.__buffer)
            self.__packet.append(e)
            next_type = e.type
        elif self.__linktype == pcap.DLT_LINUX_SLL:
            s = SLL(self.__buffer)
            self.__packet.append(s)
            # Bytes 15 and 16 of SLL says the next protocol.
            next_type = s.protocol
        else:
            # If the link layer type is unknown return all payload as a base
            # frame.
            f = Frame(self.__buffer)
            self.__packet.append(f)
            return self.__packet

        # Disassembling second frame.
        # For a while we are using hexadecimal of Ethernet a SLL next protocol
        # fields to identify next frames. Maybe this can be changed for keep
        # compatibility with other link layer protocols.
        if next_type == 0x0800:
            i = IPv4(self.__packet[-1].payload)
            self.__packet.append(i)
            next_type = i.proto
        elif next_type == 0x86DD:
            i = IPv6(self.__packet[-1].payload)
            self.__packet.append(i)
            next_type = i.nxt
        else:
            f = Frame(self.__packet[-1].payload)
            self.__packet.append(f)
            return self.__packet

        # Disassembling third frame.
        # For a while we are using IPv4 protocol and IPv6 next header fields to
        # check what the next protocol header.
        if next_type == 0x06:
            t = TCP(self.__packet[-1].payload)
            self.__packet.append(t)
        else:
            f = Frame(self.__packet[-1].payload)
            self.__packet.append(f)
            return self.__packet

        if len(self.__packet[-1].payload):
            f = Frame(self.__packet[-1].payload)
            self.__packet.append(f)

        return self.__packet

    def get_field(self, field):
        """
        """
        proto, attr = field.split('.')

        if proto in FRAME_TYPES.keys():
            for p in self.__packet:
                if hasattr(p, attr) and type(p) == FRAME_TYPES[proto]:
                    return getattr(p, attr)

        return None

    def __str__(self):
        """
        """
        s = ['timestamp %f' % self.__timestamp]

        for p in self.__packet:
            s.append(p.__str__())

        return '\n'.join(s)

class Device(object):
    """
    """
    def __init__(self, name):
        """
        """
        self.name = name
        try:
            self.naddr, self.mask = pcap.lookupnet(self.name)
        except:
            self.naddr, self.mask = None, None

class Sniff(object):
    """
    """
    def __init__(self, filter='', fields=[], amount=None):
        """
        """
        self.amount = amount
        self.filter = filter
        self.fields = fields

        self.packets = []
        self.devices = {}
        for d in umpa.sniffing.get_available_devices():
            self.devices[d] = Device(d)

    def start(self, device):
        """
        """
        capture = pcap.pcap(device)
        capture.setfilter(self.filter)
        number = 0

        for timestamp, packet in capture:
            p = Packet(timestamp, packet, capture.datalink())
            p.disassemble()
            self.packets.append(p)
            number += 1

            if len(self.fields):
                s = []
                for f in self.fields:
                    s.append(str(p.get_field(f)))
                print '(timestamp %f)' % p.get_timestamp(),', '.join(s)
            else:
                print '\n', p

            if number == self.amount:
                break
