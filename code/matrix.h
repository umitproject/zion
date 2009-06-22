/**
 * Copyright (C) 2008 Joao Paulo de Souza Medeiros.
 *
 * Author(s): Joao Paulo de Souza Medeiros <ignotus21@gmail.com>
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

#ifndef MATRIX_H
#define MATRIX_H

#include <stdlib.h>
#include "clann.h"


/**
 * Matrix structure
 */
struct matrix
{
    clann_type *values;
    unsigned int rows;
    unsigned int cols;
    clann_type max;
    clann_type min;
};


/**
 * Initialize an given matrix
 */
inline void
matrix_initialize(struct matrix *a,
                  const unsigned int rows,
                  const unsigned int cols);

/**
 * Initialize an given matrix
 */
inline void
matrix_finalize(struct matrix *a);

/**
 * Return an matrix element
 */
inline clann_type*
matrix_value(const struct matrix *a,
             const unsigned int i,
             const unsigned int j);

/**
 *
 */
inline void
matrix_fill(struct matrix *a,
            const clann_type v,
            const unsigned int rows,
            const unsigned int cols);

/**
 *
 */
inline void
matrix_identity(struct matrix *a,
                const unsigned int n);

/**
 *
 */
inline void
matrix_copy(const struct matrix *a,
            struct matrix *b);

/**
 *
 */
inline void
matrix_transpose(const struct matrix *a,
                 struct matrix *b);

/**
 *
 */
inline struct matrix*
matrix_product(const struct matrix *a,
               const struct matrix *b,
               struct matrix *c);

/**
 *
 */
inline struct matrix*
matrix_inverse(const struct matrix *a,
               struct matrix *b);

/**
 *
 */
inline struct matrix*
matrix_pseudo_inverse(const struct matrix *a,
                      struct matrix *b);

#endif
