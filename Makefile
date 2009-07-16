default: all

all:
	cd code; cc -ggdb -Wall -c *.c
	cd test; cc -ggdb -Wall -lm matrix.c -o matrix \
		../code/matrix.o \
		../code/clann.o \
		../code/reader.o
	cd test; cc -ggdb -Wall -lm fft.c -o fft \
		../code/fft.o \
		../code/matrix.o \
		../code/clann.o \
		../code/statistic.o \
		../code/reader.o
	cd test; cc -ggdb -Wall -lm rbf.c -o rbf \
		../code/rbf.o \
		../code/matrix.o \
		../code/neuron.o \
		../code/function.o \
		../code/clann.o \
		../code/lms.o \
		../code/reader.o
	cd test; cc -ggdb -Wall -lm svm.c -o svm \
		../code/svm.o \
		../code/ilpso.o \
		../code/matrix.o \
		../code/neuron.o \
		../code/function.o \
		../code/clann.o \
		../code/reader.o
	cd bind; python setup.py build

clean:
	cd code; rm *.o
	cd bind; rm -rf build
