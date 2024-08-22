#include <stdbool.h>
#include <math.h>
#include <stdio.h>

typedef struct
{
  int numerator;
  int denominator;
} Rational;

typedef enum {North, East, South, West} Cardinal;

typedef struct {
	Cardinal cardinal;
	int ox;
	int oy;
} Quadrant;

typedef struct {
	int x;
	int y;
} vec2;

typedef struct {
	int depth;
	Rational start_slope;
	Rational end_slope;
} Row;

#include "fovcalc.h"

void reduce(Rational *inrat, Rational *outrat) {
  int a, b, rem;

  if (inrat->numerator > inrat->denominator)
  {
    a = inrat->numerator;
    b = inrat->denominator;
  }
  else
  {
    a = inrat->denominator;
    b = inrat->numerator;
  }

  while (b != 0)
  {
    rem = a % b;
    a = b;
    b = rem;
  }

  outrat->numerator = inrat->numerator / a;
  outrat->denominator = inrat->denominator / a;
}

Rational multiply(Rational a, int b) {
	Rational out = {a.numerator * b, a.denominator};
	return (out);
}

int int_larger_than_rational(int b, Rational a) {
	int num = b*a.denominator;
	
	if (num > a.numerator) {
		return 1;
	} else if (num == a.numerator) {
		return 0;
	} else {
		return -1;
	}
}

float numerize(Rational a) {
	return (1.0f * a.numerator/a.denominator);
}

vec2 transform_quadrant(Quadrant q, int depth, int col) {
	vec2 v;
	
	if (q.cardinal == North) {
		v.x = q.ox + col;
		v.y = q.oy - depth;
	} 
	else if (q.cardinal == South) {
		v.x = q.ox - col;
		v.y = q.oy + depth;
	} 
	else if (q.cardinal == East) {
		v.x = q.ox + depth;
		v.y = q.oy + col;
	} 
	else if (q.cardinal == West) {
		v.x = q.ox - depth;
		v.y = q.oy - col;
	}
	
	//printf("in: %d; %d, %d, %d, %d || out: %d, %d\n", q.cardinal, depth, col, q.ox, q.oy, v.x, v.y);
	
	return (v);
}

Rational slope(int depth, int col) {
	Rational s = {2 * col - 1, 2 * depth};
	return (s);
}

bool is_symmetric(Row row, int col) {
	return ((int_larger_than_rational(col, multiply(row.start_slope, row.depth)) >= 0)
		&& (int_larger_than_rational(col, multiply(row.end_slope, row.depth)) <= 0));
}

int round_ties_up(float n) {
	return ((int) n + 0.5f);
}

int round_ties_down(float n) {
	if (n <= 0.5f) {
		return ((int) n);
	} else {
		return ((int) n + 1);
	}
}

Row next_row(Row row) {
	Row nr;
	nr.depth = row.depth + 1;
	nr.start_slope = row.start_slope;
	nr.end_slope = row.end_slope;
	return (nr);
}

int min_col(Row row) {
	return (round_ties_up(numerize(multiply(row.start_slope, row.depth))));
}
int max_col(Row row) {
	return (round_ties_down(numerize(multiply(row.end_slope, row.depth))));
}

int array_index (int x, int y, int max_width) {
	if (x == -1 || y == -1) {
		return (-1);
	}
	return (y * max_width + x);
}

int square(int n) {
	return (n*n);
}

bool tileOOB (Quadrant q, int x, int y, int max_width, int max_height) {
	if (square(q.ox - x) + square(q.oy - y) >= 144) {
		return true;
	}
	
	if (x < 0 || x >= max_width) {
		return true;
	}
	if (y < 0 || y >= max_height) {
		return true;
	}
	
	return false;
}

void calcFOV(int ox, int oy, const bool* obstacles, int max_width, int max_height, bool* shown_tiles) {
	size_t i, qi;
	int max_index = array_index(max_width-1, max_height-1, max_width);
	Rational a, b;
	Row first_row;
	
	// Hide all
	for (i=0; i<max_index; ++i) {
		shown_tiles[i] = false;
	}
	
	shown_tiles[array_index(ox, oy, max_width)] = true;
	
	for (qi=0; qi<4; ++qi) {
		Quadrant quadrant = {qi, ox, oy};
		
		a.numerator = -1;
		a.denominator = 1;
		b.numerator = 1;
		b.denominator = 1;
		
		first_row.depth = 1;
		first_row.start_slope = a;
		first_row.end_slope = b;
		
		scan(quadrant, first_row, obstacles, max_width, max_height, shown_tiles);
	}
}

bool is_wall(int index, const bool* obstacles) {
	if (index == -1) {
		return false;
	}
	
	return (obstacles[index]);
}

bool is_floor(int index, const bool* obstacles) {
	if (index == -1) {
		return false;
	}
	
	return (!obstacles[index]);
}

void scan(Quadrant quadrant, Row row, const bool* obstacles, int max_width, int max_height, bool* shown_tiles) {	
	int pretx = -1;
	int prety = -1;
	
	int minc = min_col(row);
	int maxc = max_col(row);
	
	int index, pindex;
	vec2 cur;
	
	printf("Scanning Q%d MX%d to MN%d with depth %d\n", quadrant.cardinal, maxc, minc, row.depth);
	
	Row nr;
	for (int col=minc; col <= maxc; col++) {
		cur = transform_quadrant(quadrant, row.depth, col);
		index = array_index(cur.x, cur.y, max_width);
		pindex = array_index(pretx, prety, max_width);
		//printf("Scanning q%d, row%d, col%d\n", quadrant.cardinal, row.depth, col);
		//printf("Pos %d, %d; Index i%d, p%d\n", cur.x, cur.y, index, pindex);
		
		if (tileOOB(quadrant, cur.x, cur.y, max_width, max_height)) {
			continue;
		}
		
		//printf("Tileinbounds\n");
		
		if (is_wall(index, obstacles) || is_symmetric(row, col)) {
			shown_tiles[index] = true;
		}
		
		if (is_wall(pindex, obstacles) && is_floor(index, obstacles)) {
			row.start_slope = slope(row.depth, col);
		}
		
		if (is_floor(pindex, obstacles) && is_wall(index, obstacles)) {
			nr = next_row(row);
			nr.end_slope = slope(row.depth, col);
			scan(quadrant, nr, obstacles, max_width, max_height, shown_tiles);
		}
		
		pretx = cur.x;
		prety = cur.y;
	}
	
	pindex = array_index(pretx, prety, max_width);
	if (is_floor (pindex, obstacles)) {
		scan(quadrant, next_row(row), obstacles, max_width, max_height, shown_tiles);
	}
}

void print_array(const bool* shown_tiles, bool*obstacles, int max_width, int max_height, int x, int y) {
	for (int row=0; row<max_height; row++) {
		for (int col=0; col<max_width; col++) {
			if ((col == x) && (row == y)) {
				printf("O");
			}
			else if (shown_tiles[array_index(col, row, max_width)]) {
				if (is_wall(array_index(col, row, max_width), obstacles)) {
					printf("#");
				}
				else {
					printf("+");
				}
			} else {
				printf("H");
			}
			
			printf(", ");
		}
		printf("\n");
	}
}

void main() {
	int max_width = 10, max_height = 10;
	int length = max_width*max_height;
	bool obstacles[length];
	bool shown_tiles[length];
	
	for (int i=0; i<length; i++) {
		obstacles[i] = 0;
	}
	obstacles[37] = true;
	obstacles[57] = true;
	obstacles[53] = true;
	
	int ox = 5, oy = 3;
	
	calcFOV(ox, oy, obstacles, max_width, max_height, shown_tiles);
	
	print_array(shown_tiles, obstacles, max_width, max_height, ox, oy);
}