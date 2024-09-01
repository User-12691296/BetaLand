#include <stdio.h>
#include <stdbool.h>

void print(bool* array, int length);
void change(bool* array, int length);
void dimension(int* flat_array, int width, int height);

void main() {
	int i, length = 10;
	bool array[length];
	int iarray[length];
	
	for (i=0; i<length; ++i) {
		array[i] = false;
		iarray[i] = 0;
	}
	
	print(array, length);
	
	change(array, length);
	
	print(array, length);
	
	dimension(iarray, 2, 5);
}

void change(bool* array, int length) {
	int i;
	
	for (i=0; i<length; ++i) {
		array[i] = true;
	}
}

void print(bool* array, int length)
{
    int i;
    for(i = 0 ; i < length ; i++)
        printf("%d ", array[i]);
    printf("\n");
}

void dimension(int* flat_array, int width, int height) {
	int (*reshaped)[width] = (void *)flat_array;
	
	int i, j;
	
	for (i=0; i<height; i++){
		for (j=0; j<width; j++){
			printf("%d, ", reshaped[i][j]);
		}
		printf("\n");
	}
}

int array_index(int col, int row, int width) {
	return (col + row*width);
}

int test_array_reshaping(int* array, int width, int height) {
	int i, j;
	for (i=0; i<height; i++) {
		for (j=0; j<width; j++) {
			// If the array contains anything other than zeroes, return negative
			if (!(array[array_index(col, row)] == 0)) {
				return (-1);
			}
		}
	}
	// If the array is clean, return good array
	return (0);
}