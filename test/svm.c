#include "../code/svm.h"
#include "../code/matrix.h"
#include "../code/reader.h"

int main(int argc, char **argv)
{
    struct svm s;
    struct matrix x, d;

    clann_initialize();

    reader_read_double_data_file(argv[1], &x, &d);

    svm_initialize(&s, x.cols, x.rows);
    svm_compute_weights(&s, &x, &d);

    return 0;
}
