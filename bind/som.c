/**
 * Copyright (C) 2009 Adriano Monteiro Marques
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
delete_matrix(struct matrix *a)
{
    matrix_finalize(a);
    free((void *) a);
}

void
delete_som(struct som *s)
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

PyObject*
new(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    unsigned int i, d[2];

    if (!PyArg_ParseTuple(args, "I(II)", &i, &d[0], &d[1]))
        return NULL;

    /**
     * Call the function
     */
    struct som *a = (struct som *) malloc(sizeof(struct som));

    som_initialize(a, i, d);

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(a, (void *) delete_som);
}

PyObject*
get(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    unsigned int row, col;
    PyObject *m = NULL;

    if (!PyArg_ParseTuple(args, "OII", &m, &row, &col))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *n = (struct matrix *) malloc(sizeof(struct matrix));
    struct som *a = (struct som *) PyCObject_AsVoidPtr(m);

    if (row >= a->grid.y_len || col >= a->grid.x_len)
    {
        PyErr_SetString(PyExc_IndexError, "indexes exceed output size");
        return NULL;
    }

    n->rows = 1;
    n->cols = a->grid.x_len;
    n->values = som_grid_get_weights(&a->grid, row, col);

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(n, NULL);
}

PyObject*
train(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *s = NULL,
             *m = NULL;
    unsigned int i;

    if (!PyArg_ParseTuple(args, "OOI", &s, &m, &i))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *n = (struct matrix *) PyCObject_AsVoidPtr(m);
    struct som *a = (struct som *) PyCObject_AsVoidPtr(s);

    if (i < 1)
    {
        PyErr_SetString(PyExc_IndexError,
                "number of iterations must be positive");
        return NULL;
    }

    som_training(a, n, i);

    /**
     * Convert output
     */
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject*
classification(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *s = NULL,
             *m = NULL;
    unsigned int metric, method, i, j;
    float limit_aux;
    struct matrix ba, pa;
    clann_type limit;


    if (!PyArg_ParseTuple(args, "OOfI", &s, &m, &limit_aux, &method))
        return NULL;

    limit = (clann_type) limit_aux;

    /**
     * Call the function
     */
    struct matrix *b = (struct matrix *) PyCObject_AsVoidPtr(m);
    struct som *a = (struct som *) PyCObject_AsVoidPtr(s);

    if(method==1)
    {

        /* for hausdorff_limit only P and Pi are needed */
        matrix_initialize(&pa, a->grid.weights.rows, a->grid.weights.cols);
        matrix_initialize(&ba, b->rows, b->cols - 1);
                
        for (i = 0; i < a->grid.weights.rows; i++)
        {
            for (j = 0; j < a->grid.weights.cols - 1; j++)
                *matrix_value(&pa, i, j) = *matrix_value(&a->grid.weights, i, j);
            *matrix_value(&pa, i, a->grid.weights.cols-1) = a->grid.density[i];
        }

        for (i = 0; i < b->rows; i++)
            for (j = 0; j < b->cols - 1; j++)
                *matrix_value(&ba, i, j) = *matrix_value(b, i, j);
                
        metric = metric_hausdorff_limit_symmetric(&pa, &ba, limit);
    }
    else
    {
        matrix_initialize(&pa, a->grid.weights.rows, a->grid.weights.cols + 2);
        
        for (i = 0; i < a->grid.weights.rows; i++)
            for (j = 0; j < a->grid.weights.cols - 1; j++)
                *matrix_value(&pa, i, j) = *matrix_value(&(a->grid.weights), i, j);
            *matrix_value(&pa, i, a->grid.weights.cols-1) = a->grid.density[i];
            *matrix_value(&pa, i, a->grid.weights.cols) = a->grid.orientation[i];
            
        metric = metric_hausdorff_angle_symmetric(&pa, b, limit);
    }
    
    /**
     * Convert output
     */
    return Py_BuildValue("I", metric);
}

PyObject*
caracterization(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *s = NULL,
             *m = NULL;
    unsigned int i;

    if (!PyArg_ParseTuple(args, "OOI", &s, &m, &i))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *n = (struct matrix *) PyCObject_AsVoidPtr(m);
    struct som *a = (struct som *) PyCObject_AsVoidPtr(s);

    if (i < 1)
    {
        PyErr_SetString(PyExc_IndexError,
                "number of iterations must be positive");
        return NULL;
    }

    som_caracterization(a, n, i);

    /**
     * Convert output
     */
    Py_INCREF(Py_None);
    return Py_None;
}

PyMODINIT_FUNC
initsom(void)
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
