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

#include "som.h"

clann_type *z,
           *o,
           sz = 0.07,
           so = 0.5,
           r = 0.07;


void
som_initialize(struct som *ann,
               unsigned int input_size,
               unsigned int *dimension)
{
    ann->input_size = input_size;
    ann->width = (dimension[0] > dimension[1] ? dimension[0] : dimension[1]);
    ann->learning_rate = 0.1;
    ann->const_1 = 1000 / CLANN_LOG(ann->width);
    ann->const_2 = 1000;
    ann->step = 1;
    ann->epoch = 0;

    ann->grid.x_len = dimension[0];
    ann->grid.y_len = dimension[1];

    matrix_initialize(&ann->grid.weights,
                      ann->grid.x_len * ann->grid.y_len,
                      ann->input_size);

    unsigned int i, j, k;
    for (i = 0; i < ann->grid.x_len; i++)
        for (j = 0; j < ann->grid.y_len; j++)
            for (k = 0; k < ann->input_size; k++)
                som_grid_get_weights(&ann->grid, i, j)[k] = clann_rand(-1, 1);
}

void
som_finalize(struct som *ann)
{
    matrix_finalize(&ann->grid.weights);
}

clann_type*
som_grid_get_weights(struct som_grid *grid,
                     unsigned int i,
                     unsigned int j)
{
    return matrix_value(&grid->weights, i * grid->y_len + j, 0);
}

void
som_training(struct som *ann,
             struct matrix *x,
             unsigned int epochs)
{
    clann_type winner[2], *sample, *neuron, d, min, aux;
    unsigned int i, j, k, mess[x->rows];

    for (i = 0; i < x->rows; i++)
        mess[i] = i;

    while (ann->epoch < epochs)
    {
	printf("epoch: %d\n",ann->epoch);
        clann_shuffle(mess, x->rows);

        aux = CLANN_EXP(-((clann_type) ann->epoch / ann->const_2));
        ann->actual_learning_rate = ann->learning_rate * aux;

        aux = ann->width * CLANN_EXP(-(clann_type) ann->epoch / ann->const_1);
        ann->actual_width = 2 * CLANN_POW(aux, 2);

        for (k = 0; k < x->rows; k++)
        {
            min = (clann_type) INT_MAX;

            sample = matrix_value(x, mess[k], 0);

            for (i = 0; i < ann->grid.x_len; i++)
                for (j = 0; j < ann->grid.y_len; j++)
                {
                    neuron = som_grid_get_weights(&ann->grid, i, j);
                    d = metric_euclidean(sample, neuron, x->cols);

                    if (d < min)
                    {
                        min = d;
                        winner[0] = (clann_type) i;
                        winner[1] = (clann_type) j;
                    }
                }

            som_adjust_weights(ann, sample, winner);
        }

#if CLANN_VERBOSE
        printf("N. [SOM] Width: "CLANN_PRINTF", Rate: "CLANN_PRINTF" (%d).\n",
               ann->actual_width,
               ann->actual_learning_rate,
               ann->epoch);
#endif
        ann->epoch += ann->step;
    }
}

void
som_adjust_weights(struct som *ann,
                   clann_type *x,
                   clann_type *winner)
{
    clann_type *w, h, p[2];
    unsigned int i, j, k;

    for (i = 0; i < ann->grid.x_len; i++)
        for (j = 0; j < ann->grid.y_len; j++)
        {
            p[0] = (clann_type) i;
            p[1] = (clann_type) j;

            h = CLANN_POW(metric_euclidean(p, winner, 2), 2);
            h = CLANN_EXP(-h / ann->actual_width);

            w = som_grid_get_weights(&ann->grid, i, j);

            for (k = 0; k < ann->input_size; k++)
                w[k] += ann->actual_learning_rate * h * (x[k] - w[k]);
        }
}

int
som_save(struct som *ann,
         const char *file)
{
    FILE *fd;

    if ((fd = fopen(file, "w")))
    {
        unsigned int i, j;

        fprintf(fd, "%s\n", FILE_HEADER_SOM);

        fprintf(fd, "%d ", ann->grid.x_len);
        fprintf(fd, "%d\n", ann->grid.y_len);

        fprintf(fd, "%d ", ann->input_size);
        fprintf(fd, CLANN_PRINTF" ", ann->width);
        fprintf(fd, CLANN_PRINTF" ", ann->learning_rate);
        fprintf(fd, CLANN_PRINTF" ", ann->const_1);
        fprintf(fd, CLANN_PRINTF"\n", ann->const_2);

        for (i = 0; i < ann->grid.weights.rows; i++)
        {
            fprintf(fd,
                    CLANN_PRINTF,
                    *matrix_value(&ann->grid.weights, i, 0));

            for (j = 1; j < ann->grid.weights.cols; j++)
                fprintf(fd,
                        " " CLANN_PRINTF,
                        *matrix_value(&ann->grid.weights, i, j));

            fprintf(fd, "\n");
        }

        fclose(fd);

        return 1;
    }

    printf("E. [SOM] Can not open/create file to write.\n");

    return 0;
}

int
som_open(struct som *ann,
         const char *file)
{
    return 0;
}

void
som_caracterization(struct som *ann,
             	   struct matrix *x,
             	   unsigned int epochs)
{
    clann_type n_scale[2], z_scale[2];
    unsigned int i, j;
    clann_type d, cx, cy, *w, *t, *p, *a, *b;

    ann->grid.orientation = malloc(sizeof(clann_type) * ann->grid.weights.rows);
    ann->grid.density = malloc(sizeof(clann_type) * ann->grid.weights.rows);

    for (i = 0; i < ann->grid.weights.rows; i++)
    {
        ann->grid.orientation[i] = 0;
        ann->grid.density[i] = 0;
    }

    n_scale[MIN] = (clann_type) -1.0;
    n_scale[MAX] = (clann_type)  1.0;

    printf("Training SOM\n");
    som_training(ann, x, epochs);

    t = malloc(sizeof(clann_type) * ann->grid.weights.rows);

    for (i = 0; i < ann->grid.weights.rows; i++)
        t[i] = 0;

    /**
     * Density
     */
    printf("Calculating density\n");
    for (i = 0; i < x->rows; i++)
    {
        p = matrix_value(x, i, 0);

        z_scale[MIN] = (clann_type) INT_MAX;
        z_scale[MAX] = (clann_type) - INT_MAX;

        for (j = 0; j < ann->grid.weights.rows; j++)
        {
            w = matrix_value(&ann->grid.weights, j, 0);

            d = CLANN_POW(metric_euclidean(p, w, 2), 2.0);
            d = function_green_gaussian(&sz, &d);

            t[j] += d;

            if (t[j] < z_scale[MIN])
                z_scale[MIN] = t[j];

            if (t[j] > z_scale[MAX])
                z_scale[MAX] = t[j];
        }

        for (j = 0; j < ann->grid.weights.rows; j++)
            ann->grid.density[j] = metric_scale(t[j], z_scale, n_scale);
    }

    /**
     * Orientation
     */
    printf("Calculating orientation\n");
    for (j = 0; j < ann->grid.weights.rows; j++)
    {
        w = matrix_value(&ann->grid.weights, j, 0);

        cx = 0;
        cy = 0;

        for (i = 0; i < x->rows - 1; i++)
        {
            a = matrix_value(x, i, 0);
            b = matrix_value(x, i + 1, 0);

            d = CLANN_POW(metric_euclidean(a, w, 2), 2.0);
            d = function_green_gaussian(&so, &d);

            cx += (b[X] - a[X]) * d;
            cy += (b[Y] - a[Y]) * d;
        }

        ann->grid.orientation[j] = CLANN_ATAN2(cy, cx);
    }

    /**
     * Normalization
     */
    printf("Normalization\n");
    clann_type x_scale[2], y_scale[2];

    x_scale[MIN] = (clann_type) INT_MAX;
    x_scale[MAX] = (clann_type) - INT_MAX;
    y_scale[MIN] = (clann_type) INT_MAX;
    y_scale[MAX] = (clann_type) - INT_MAX;

    for (j = 0; j < ann->grid.weights.rows; j++)
    {
        w = matrix_value(&ann->grid.weights, j, 0);

        //if (z[j] < MIN_DENSITY)
        //    continue;

        if (w[X] < x_scale[MIN])
            x_scale[MIN] = w[X];

        if (w[X] > x_scale[MAX])
            x_scale[MAX] = w[X];

        if (w[Y] < y_scale[MIN])
            y_scale[MIN] = w[Y];

        if (w[Y] > y_scale[MAX])
            y_scale[MAX] = w[Y];
    }

    for (j = 0; j < ann->grid.weights.rows; j++)
    {
        w = matrix_value(&ann->grid.weights, j, 0);

        w[X] = metric_scale(w[X], x_scale, n_scale);
        w[Y] = metric_scale(w[Y], y_scale, n_scale);
    }
}
