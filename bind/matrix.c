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

#include <Python.h>

#include "../code/matrix.h"

static PyObject *MatrixError;

static char matrix_new__doc__[] =
""
;

static PyObject*
matrix_new(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    unsigned int rows, cols;

    if (!PyArg_ParseTuple(args, "II", &rows, &cols))
        return NULL;

    /**
     * Call the function
     */
    struct matrix* a;

    matrix_initialize(a, rows, cols);

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(a, (void *)&matrix_finalize);
}

static PyMethodDef MatrixMethods[] =
{
    {"matrix_new",  matrix_new, METH_VARARGS, matrix_new__doc__},
    {NULL, NULL, 0, NULL}
};

static char matrix_module__doc__[] =
""
;

PyMODINIT_FUNC
init_matrix(void)
{
    PyObject *m;

    m = Py_InitModule4("matrix",
            MatrixMethods,
            matrix_module__doc__,
            (PyObject *)NULL,
            PYTHON_API_VERSION);
    if (m == NULL)
        return;

    MatrixError = PyErr_NewException("matrix.error", NULL, NULL);
    Py_INCREF(MatrixError);
    PyModule_AddObject(m, "error", MatrixError);

    if (PyErr_Occurred())
        Py_FatalError("can't initialize module matrix");

}
