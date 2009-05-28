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

import struct

class Frame(object):
    """
    """
    header_size = None   # Base header size for those that have variable length
    header_format = None

    def __init__(self, buffer):
        """
        """
        self._raw = buffer

    def __str__(self):
        """
        """
        s = ["+ Frame"]
        raw = struct.unpack('B' * len(self._raw), self._raw)
        col = 16

        for i in range(len(raw) / col):
            s.append("| " + "%.2x " * col % (raw[i * col: (i + 1) * col]))

        rest = len(raw) % col
        i = len(raw) / col
        if rest:
            s.append("| " + "%.2x " * rest % (raw[i * col: i * col + rest]))

        s[-1] = s[-1].replace("| ", "|_")

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

        self.dst = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (self._fields[0:6])
        self.src = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (self._fields[6:12])
        self.type = self._fields[12]

    def __str__(self):
        """
        """
        s = ["+ Ethernet"]
        s.append("| (dst %s)" % self.dst)
        s.append("| (src %s)" % self.src)
        s.append("|_(type 0x%.4x)" % self.type)

        return "\n".join(s)

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
        self.src = "%d.%d.%d.%d" % (self._fields[8:12])
        self.dst = "%d.%d.%d.%d" % (self._fields[12:16])

        # FIXME: verify header size
        self.payload = self._raw[self.header_size:]

    def __str__(self):
        """
        """
        s = ["+ IPv4"]
        s.append("| (version 0x%x)" % self.version)
        s.append("| (hdr_len 0x%x)" % self.hdr_len)
        s.append("| (tos 0x%.2x)" % self.tos)
        s.append("| (len 0x%.4x)" % self.len)
        s.append("| (id 0x%.4x)" % self.id)
        s.append("| (flags 0x%x)" % self.flags)
        s.append("| (frag_offset 0x%.4x)" % self.frag_offset)
        s.append("| (ttl 0x%.2x)" % self.ttl)
        s.append("| (proto 0x%.2x)" % self.proto)
        s.append("| (checksum 0x%.2x)" % self.checksum)
        s.append("| (src %s)" % self.src)
        s.append("|_(dst %s)" % self.dst)

        return "\n".join(s)

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
        self.dst = ":".join(["%.4x"] * 8) % (self._fields[4:12])
        self.src = ":".join(["%.4x"] * 8) % (self._fields[12:20])

    def __str__(self):
        """
        """
        s = ["+ IPv6"]
        s.append("| (version 0x%x)" % self.version)
        s.append("| (clas 0x%.2x)" % self.clas)
        s.append("| (flow 0x%.3x)" % self.flow)
        s.append("| (plen 0x%.4x)" % self.plen)
        s.append("| (nxt 0x%.2x)" % self.nxt)
        s.append("| (hlim 0x%.2x)" % self.hlim)
        s.append("| (src %s)" % self.src)
        s.append("|_(dst %s)" % self.dst)

        return "\n".join(s)

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
        s = ["+ TCP"]

        s.append("| (srcport %d)" % self.srcport)
        s.append("| (dstport %d)" % self.dstport)
        s.append("| (seq %d)" % self.seq)
        s.append("| (ack %d)" % self.ack)
        s.append("| (hdr_len 0x%x)" % self.hdr_len)
        s.append("| (reserved 0x%x)" % self.reserved)
        s.append("| (flags 0x%.2x)" % self.flags)
        s.append("| (window_size 0x%.4x)" % self.window_size)
        s.append("| (checksum 0x%.4x)" % self.checksum)
        s.append("|_(urgent_pointer 0x%.4x)" % self.urgent_pointer)

        return "\n".join(s)

class Packet(object):
    """
    """
    def __init__(self, timestamp, buffer):
        """
        """
        self.__timestamp = timestamp
        self.__buffer = buffer

    def disassemble(self):
        """
        """
        # FIXME: consider the use of another first frame instead Ethernet as
        # first frame.
        next_type = None
        p = []

        # Disassemble first frame.
        e = Ethernet(self.__buffer)
        p.append(e)
        next_type = e.type

        # Disassemble second frame.
        if next_type == 0x0800:
            i = IPv4(p[-1].payload)
            p.append(i)
            next_type = i.proto
        elif next_type == 0x86DD:
            i = IPv6(p[-1].payload)
            p.append(i)
            next_type = i.nxt
        else:
            f = Frame(p[-1].payload)
            p.append(f)
            return p

        # Disassemble third frame.
        if next_type == 0x06:
            t = TCP(p[-1].payload)
            p.append(t)
        else:
            f = Frame(p[-1].payload)
            p.append(f)
            return p

        if len(p[-1].payload):
            f = Frame(p[-1].payload)
            p.append(f)

        return p
