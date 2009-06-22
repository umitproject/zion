#include <stdio.h>
#include <stdlib.h>
#include "../code/clann.h"
#include "../code/matrix.h"

#define M 4
#define N 3

int main(int argc, char** argv)
{
    struct matrix a, b;
    unsigned i, j;

    clann_initialize();

    matrix_initialize(&a, M, N);

    *matrix_value(&a, 0, 0) = 1;
    *matrix_value(&a, 0, 1) = 2;
    *matrix_value(&a, 0, 2) = 6;

    *matrix_value(&a, 1, 0) = 3;
    *matrix_value(&a, 1, 1) = 5;
    *matrix_value(&a, 1, 2) = 4;

    *matrix_value(&a, 2, 0) = 2;
    *matrix_value(&a, 2, 1) = 6;
    *matrix_value(&a, 2, 2) = 8;

    *matrix_value(&a, 3, 0) = 1;
    *matrix_value(&a, 3, 1) = 0;
    *matrix_value(&a, 3, 2) = 2;

    if (matrix_pseudo_inverse(&a, &b) != NULL)
    {
        printf("Pseudo-inverse:\n");
        for (i = 0; i < N; i++)
        {
            for (j = 0; j < M; j++)
                printf(CLANN_PRINTF " ", *matrix_value(&b, i, j));

            printf("\n");
        }
    }
    else
        printf("No pseudo-inverse.\n");

    return 0;
}
