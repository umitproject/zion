# Copyright (C) 2009 Adriano Monteiro Marques.
#
# Author: Diogo Ricardo Marques Pinheiro <diogormpinheiro@gmail.com>
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

from umit.clann import matrix

class Matrix(object):
    
    def __init__(self, rows, cols):
        """
        """
        self.cols = cols
        self.rows = rows
        self.matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(0)
            self.matrix.append(row)
 
    def setitem(self, row, col, value):
        """
        """
        self.matrix[row][col] = value
 
    def getitem(self, row, col):
        """
        """
        return self.matrix[row][col]
    
    def convert(self):
        """
        Convert the matrix to C matrix.
        """
        mat = matrix.new(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                matrix.set(mat, i, j, self.matrix[i][j])
                
        return mat