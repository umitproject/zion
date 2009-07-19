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

#include "bind/som.h"

void
delete(struct som *s)
{
    som_finalize(s);
    free((void *) s);
}

PyObject*
size(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *m = NULL;

    if (!PyArg_ParseTuple(args, "O", &m))
        return NULL;

    /**
     * Call the function
     */
    struct som *a = (struct som *) PyCObject_AsVoidPtr(m);

    /**
     * Convert output
     */
    return Py_BuildValue("II", a->grid.x_len, a->grid.y_len);
}

PyMODINIT_FUNC
initmatrix(void)
{
    PyObject *m;

    m = Py_InitModule4("som",
            SOMMethods,
            module__doc__,
            (PyObject *)NULL,
            PYTHON_API_VERSION);

    if (m == NULL)
        return;

    SOMError = PyErr_NewException("som.error", NULL, NULL);
    Py_INCREF(SOMError);
    PyModule_AddObject(m, "error", SOMError);

    if (PyErr_Occurred())
        Py_FatalError("can't initialize module som");
}
