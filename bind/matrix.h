/**
 * Copyright (C) 2009 Joao Paulo de Souza Medeiros.
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

#ifndef BIND_MATRIX_H
#define BIND_MATRIX_H

#include <Python.h>

#include "code/matrix.h"

static PyObject *MatrixError;

static void
delete(struct matrix *a);

/**
 *
 */
static char new__doc__[] = "Create a new matrix";

static PyObject*
new(PyObject *self, PyObject *args);

/**
 *
 */
static char get__doc__[] = "Get a matrix value";

static PyObject*
get(PyObject *self, PyObject *args);

/**
 *
 */
static char set__doc__[] = "Set a matrix value";

static PyObject*
set(PyObject *self, PyObject *args);

/**
 *
 */
static char fill__doc__[] = "Fill a matrix with a value";

static PyObject*
fill(PyObject *self, PyObject *args);

/**
 *
 */
static char identity__doc__[] = "Create an identity matrix";

static PyObject*
identity(PyObject *self, PyObject *args);

/**
 *
 */
static PyMethodDef MatrixMethods[] =
{
    {"new", new, METH_VARARGS, new__doc__},
    {"get", get, METH_VARARGS, get__doc__},
    {"set", set, METH_VARARGS, set__doc__},
    {"fill", fill, METH_VARARGS, fill__doc__},
    {"identity", identity, METH_VARARGS, identity__doc__},
    {NULL, NULL, 0, NULL}
};

/**
 *
 */
static char module__doc__[] = "CLANN matrix module";

PyMODINIT_FUNC
initmatrix(void);

#endif
