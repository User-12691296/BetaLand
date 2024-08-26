#include <stdio.h>
#include <stdbool.h>

void print(bool* array, int length);
void change(bool* array, int length);

void main() {
	int i, length = 10;
	bool array[length];
	
	for (i=0; i<length; ++i) {
		array[i] = false;
	}
	
	print(array, length);
	
	change(array, length);
	
	print(array, length);
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