#include <stdio.h>
#include <stdlib.h>
#include "../code/clann.h"
#include "../code/reader.h"
#include "../code/statistic.h"
#include "../code/fft.h"

int main(int argc, char** argv)
{
    struct matrix x;
    unsigned int i;
    clann_type mean;

    clann_initialize();

    reader_read_data_file(argv[1], &x);

    mean = statistic_mean_matrix_col(&x, 0);

    unsigned int n = x.rows;
    complex *cx = malloc(sizeof(complex) * n);

    for (i = 0; i < x.rows; i++)
    {
        cx[i] = *matrix_value(&x, i, 0) - mean;

        if (x.cols > 1)
            cx[i] += *matrix_value(&x, i, 1) * I;
    }

    fft(&cx, &n, FFT_FORWARD);

    for (i = 0; i < n; i++)
        printf("%f %fi\n",
                creal(cx[i]),
                cimag(cx[i]));

    return 0;
}
