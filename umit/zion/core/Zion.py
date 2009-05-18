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

OPTIONS = {"-v": "VERBOSE",
           "-s": "SCAN",
           "-i": "INTERVAL",
           "-a": "AMOUNT",
           "-l": "LIST",
           "-d": "DETECT"}

class Options(object):
    """
    """
    def __init__(self):
        """
        """
        pass

    def add_option(self, option, value):
        """
        """
        if option in OPTIONS.keys():
            setattr(self, OPTIONS[option], value)

class Zion(object):
    """
    """
    def __init__(self, option, target):
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
        while True:
