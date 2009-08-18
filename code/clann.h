/**
 * Copyright (C) 2008-2009 Adriano Monteiro Marques
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

#ifndef CLANN_H
#define CLANN_H

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define CLANN_S_PRINTF      "%.1Lf"
#define CLANN_PRINTF        "%.10Lf"
#define CLANN_SCANF         "%Lf"
#define CLANN_POW           powl
#define CLANN_SQRT          sqrtl
#define CLANN_EXP           expl
#define CLANN_LOG           logl
#define CLANN_SIN           sinl
#define CLANN_COS           cosl
#define CLANN_ATAN2         atan2l
#define CLANN_FABS          fabsl

#define CLANN_VERBOSE       0
#define CLANN_DEBUG         1

#define FILE_HEADER_MLP     "MLP"
#define FILE_HEADER_SOM     "SOM"
#define FILE_HEADER_TLFN    "TLFN"
#define FILE_HEADER_NARX    "NARX"

#define CLANN_SWAP(a,b)     {(a) += (b); (b) = (a) - (b); (a) -= (b);}

typedef long double clann_type;

/**
 *
 */
inline void
clann_shuffle(unsigned int *list,
              unsigned int length);

/**
 *
 */
inline void
clann_initialize(void);

/**
 *
 */
inline clann_type
clann_nrand(void);

/**
 *
 */
inline clann_type
clann_rand(const clann_type min,
           const clann_type max);

/**
 *
 */
long int clann_randint(const clann_type min,
                       const clann_type max);

/**
 *
 */
inline clann_type
clann_factorial(const unsigned int v);

/**
 *
 */
inline clann_type
clann_binomial(const unsigned int n,
               const unsigned int k);

/**
 *
 */
inline unsigned int
clann_nextpow2(unsigned int n);

#endif
