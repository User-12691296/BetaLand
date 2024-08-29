#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <limits.h>

typedef struct Node {
	int x, y;
	int f, g, h;
	struct Node *parent;
} Node;

int max(int a, int b) {
	if (a > b) {
		return a;
	}
	return b;
}

int array_index (int col, int row, int max_width) {
	return (row * max_width + col);
}

int isValid(int col, int row, int max_width, int max_height) {
    return (row >= 0) && (row < max_height) && (col >= 0) && (col < max_width);
}

int isUnblocked(int grid[], int col, int row, int max_width) {
    return grid[array_index(col, row, max_width)] == 1;
}

int isDestination(int col, int row, int dCol, int dRow) {
    return row == dRow && col == dCol;
}

int square(int n) {
	return n*n;
}

int calculateHValue(int col, int row, int dCol, int dRow) {
    return (square(max(abs(row - dRow), abs(col - dCol))));
}

int tracePath(Node nodes[], int dCol, int dRow, int sCol, int sRow, int max_width) {
	printf("Path is");
	
	Node current = nodes[array_index(dCol, dRow, max_width)];
	
	int i=0;
	
	while (!(current.x == sCol && current.y == sRow) && i<100) {
		printf(" <- (%d, %d)", current.x, current.y, current.parent -> x, current.parent -> y);
		
		current = *current.parent;
		
		i++;
	}
	
	printf(" <- (%d, %d)\n", current.x, current.y);
}

void aStarSearch(int* grid, int sCol, int sRow, int dCol, int dRow, int max_width, int max_height) {
	// If the source or destination is out of range
    if (!isValid(sCol, sRow, max_width, max_height) || !isValid(dCol, dRow, max_width, max_height)) {
        printf("Source or destination is invalid\n");
        return;
    }
    // If the source or destination cell is blocked
    if (!isUnblocked(grid, sCol, sRow, max_width) || !isUnblocked(grid, dCol, dRow, max_width)) {
        printf("Source or destination is blocked\n");
        return;
    }
    // If the destination cell is the same as source cell
    if (isDestination(sCol, sRow, dCol, dRow)) {
        printf("We are already at the destination\n");
        return;
    }
	
	Node nodes[max_height*max_width];
	
	Node openList[max_width*max_height];
	int openListSize = 0;
	
	int closedList[max_height*max_width];
	
	// Initialise array
	int index;
	for (int i=0; i<max_width; i++) {
		for (int j=0; j<max_height; j++) {
			index = array_index(i, j, max_width);
			closedList[index] = 0;
			
			nodes[index].x = i;
			nodes[index].y = j;
			
			nodes[index].f = INT_MAX;
			nodes[index].g = INT_MAX;
			nodes[index].h = INT_MAX;
		}
	}
	
	// Start node
	int col = sCol;
	int row = sRow;
	index = array_index(col, row, max_width);
	nodes[index].g = 0;
	nodes[index].h = calculateHValue(col, row, sCol, sRow);
	nodes[index].f = nodes[index].g + nodes[index].h;
	openList[openListSize++] = nodes[index];
	
	// Loop until destination found
	int found = 0;
	while (openListSize > 0) {
		// Get the node with lowest f
		int minF = INT_MAX;
		int minIndex = -1;
		for (int i=0; i<openListSize; i++) {
			if (openList[i].f < minF) {
				minF = openList[i].f;
				minIndex = i;
			}
		}
		
		// Make it the current node and remove it from future checks
		Node current = openList[minIndex];
		col = current.x;
		row = current.y;
		index = array_index(col, row, max_width);
		
		openList[minIndex] = openList[--openListSize];
		closedList[index] = 1;
		
		//if (!(col==sCol && row==sRow)){
		//	printf("Lowest tile is (%d, %d) P (%d, %d)\n", col, row, current.parent -> x, current.parent -> y);
		//}
		
		if (isDestination(col, row, dCol, dRow)) {
			tracePath(nodes, dCol, dRow, sCol, sRow, max_width);
			found = 1;
			return;
		}
		
		// Loop through all neighbors
		int nbrsX[] = {0, -1, 0, 1, -1, 1, -1, 1};
		int nbrsY[] = {-1, 0, 1, 0, -1, -1, 1, 1};
		int nbrIndex;
		for (int i=0; i<8; i++) {
			int nbrCol = col + nbrsX[i];
			int nbrRow = row + nbrsY[i];
			nbrIndex = array_index(nbrCol, nbrRow, max_width);
			
			//printf("Scanning nbr (%d, %d)\n", nbrCol, nbrRow);
			
			// If tile is on the map
			if (isValid(nbrCol, nbrRow, max_width, max_height)) {				
				if (closedList[nbrIndex] == 0 && isUnblocked(grid, nbrCol, nbrRow, max_width)) {
					int gNew = current.g + 1.0;
					
					if (gNew < nodes[nbrIndex].g) {
						nodes[nbrIndex].parent = &nodes[index];
						nodes[nbrIndex].g = gNew;
						nodes[nbrIndex].h = calculateHValue(nbrCol, nbrRow, dCol, dRow);
						nodes[nbrIndex].f = nodes[nbrIndex].g + nodes[nbrIndex].h;
						openList[openListSize++] = nodes[nbrIndex];
					}
				}
			}
		}
	}
	
	if (!found) {
		printf("Not found\n");
	}

}

int main() {
    // Grid representation where 1 is an open cell and 0 is a blocked cell
    int grid[5*5] =
        {
            1, 0, 1, 1, 1,
            1, 0, 1, 0, 0,
            1, 0, 0, 1, 1,
            1, 0, 0, 0, 1,
            1, 1, 1, 1, 0};
    // Source and destination coordinates
    int sCol = 0, sRow = 0;
    int dCol = 4, dRow = 0;
    aStarSearch(grid, sCol, sRow, dCol, dRow, 5, 5);
    return 0;
}