#include <stdio.h>
#include "mylib.h"

void test_empty(void) {
    puts("Hello from C");
}

float test_add(float x, float y) {
    return x + y;
}

void test_passing_array(int *data, int len) {
    // Modifying the array
    for(int i = 0; i < len; ++i) {
        data[i] = -i;
    }
}

void test_numpy(const double* indatav, size_t size, double *outdatav) {
	size_t i;
	for (i=0; i < size; ++i) {
		outdatav[i] = indatav[i] *2.0;
	}
}