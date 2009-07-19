/**
 * Copyright (C) 2008 Joao Paulo de Souza Medeiros.
 *
 * Author(s): João Paulo de Souza Medeiros <ignotus21@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 */

#ifndef READER_H
#define READER_H

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "clann.h"
#include "matrix.h"


/**
 * Extract a vector from a line of numbers
 */
void
reader_extract_numbers(struct matrix *m,
                       const char *line);

/**
 * Reader for input data files
 */
int
reader_read_double_data_file(const char *path,
                             struct matrix *x,
                             struct matrix *d);

/**
 * Reader for time series files
 */
int
reader_read_data_file(const char *path,
                      struct matrix *v);

#endif
