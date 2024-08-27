#pragma once

#ifdef __cplusplus
extern "C" {
#endif

void reduce(Rational *inrat, Rational *outrat);
Rational multiply(Rational a, int b);
vec2 transform_quadrant(Quadrant q, int depth, int col);
Rational slope(int depth, int col);
bool is_symmetric(Row row, int col);
int round_ties_up(float n);
int round_ties_down(float n);
Row next_row(Row row);
int min_col(Row row);
int max_col(Row row);
int array_index (int x, int y, int max_width);
int square(int n);
bool tileOOB (Quadrant q, int x, int y, int max_width, int max_height, int range);
void calcFOV(int ox, int oy, const bool* obstacles, int max_width, int max_height, bool* shown_tiles, int range);
bool is_wall(int index, const bool* obstacles);
bool is_floor(int index, const bool* obstacles);
void scan(Quadrant quadrant, Row row, const bool* obstacles, int max_width, int max_height, bool* shown_tiles, int range);

#ifdef __cplusplus
}
#endif