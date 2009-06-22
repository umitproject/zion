#include "../code/clann.h"
#include "../code/rbf.h"
#include "../code/matrix.h"
#include "../code/reader.h"

int main(int argc, char **argv)
{
    struct rbf r;
    struct matrix x, d, input_val;
    unsigned int i;

    clann_initialize();

    reader_read_double_data_file(argv[1], &x, &d);

    matrix_initialize(&input_val, 1, 2);

    *matrix_value(&input_val, 0, 0) = 1;
    *matrix_value(&input_val, 0, 1) = 1;

    rbf_initialize(&r, 2, 1, 4, 2);
    rbf_learn(&r, &x, &d);
    rbf_compute_output(&r, &input_val.values[0]);

    for (i = 0; i < r.output_size; i++)
        printf("output[%d]= " CLANN_PRINTF " \n", i, r.output[i]);

    return 0;
}
