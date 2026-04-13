// Arup Guha
// 1/25/2022
// Solution to Artwork (2016 NCPC) illustrating neat use of a disjoint set.
// Written in COP 3503 class after teaching a disjoint set.
// https://open.kattis.com/problems/artwork

import java.util.*;

public class artwork {
	
	// Directions I can move to merge regions.
	final public static int[] DX = {-1,0,0,1};
	final public static int[] DY = {0,-1,1,0};
	
	public static int r;
	public static int c;
	public static int numS;
	public static int[][] strokes;
	
	public static int[][] paint;
	
	public static void main(String[] args) {
		
		// Read dimensions and # of strokes.
		Scanner stdin = new Scanner(System.in);
		r = stdin.nextInt();
		c = stdin.nextInt();
		numS = stdin.nextInt();
		
		// Store all strokes.
		strokes = new int[numS][4];
		for (int i=0; i<numS; i++)
			for (int j=0; j<4; j++)
				strokes[i][j] = stdin.nextInt()-1;
			
		// Set up canvas.
		paint = new int[r][c];
		for (int i=0; i<numS; i++)
			addStroke(i);
		
		// Here is my disjoint set!
		djset dj = new djset(r*c);
		
		int numBlack = 0;
		
		// Union together all adjacent white squares.
		for (int x=0; x<r; x++) {
			for (int y=0; y<c; y++) {
				
				// Skip non-white squares.
				if (paint[x][y] != 0) {
					numBlack++;
					continue;
				}
				
				// Try merging all neighbors with (x, y)
				tryMerge(x, y, dj);
			}
		}
		
		// Store all results here.
		int[] res = new int[numS];
		res[numS-1] = dj.numC - numBlack;
		
		// Now, let's "undo" some brush strokes.
		for (int i=numS-1; i>=0; i--) {
			
			if (strokes[i][0] == strokes[i][2]) {
			
				// Unpaint!
				for (int y=strokes[i][1]; y<=strokes[i][3]; y++) {
					paint[strokes[i][0]][y]--;
					
					// Now this square turns from black to white.
					if (paint[strokes[i][0]][y] == 0) {
						tryMerge(strokes[i][0], y, dj);
						numBlack--;
					}
				}
			}
		
			// Vertical stroke.
			else {
			
				// Unpaint.
				for (int x=strokes[i][0]; x<=strokes[i][2]; x++) {
					paint[x][strokes[i][1]]--;
					
					// Square has turned from black to white.
					if (paint[x][strokes[i][1]] == 0) {
						tryMerge(x, strokes[i][1], dj);
						numBlack--;
					}
				}
			}
			
			// Now we can answer this!
			if (i>0) res[i-1] = dj.numC - numBlack;
		}			
			
		// Ta da!
		for (int i=0; i<numS; i++)
			System.out.println(res[i]);
	}
	
	// Try merging the square at (x,y) with all of its neighbors.
	public static void tryMerge(int x, int y, djset dj) {
		
		// Look in each direction.
		for (int dir=0; dir<DX.length; dir++) {
					
			// Square in direction dir from (x,y).
			int nX = x + DX[dir];
			int nY = y + DY[dir]; 
					
			// Can't go out of bounds.
			if (!inbounds(nX, nY)) continue;
					
			// Neighbor square isn't white.
			if (paint[nX][nY] != 0) continue;
					
			// Union these two squares. Since 0 <= y < c, x*c + y is unique.
			dj.union(x*c+y, nX*c+nY);
		
		}
	}		
	
	// Adds stroke i to the canvas.
	public static void addStroke(int i) {
		
		// Horizontal stroke.
		if (strokes[i][0] == strokes[i][2]) {
			
			// Paint for all the different y values in range.
			for (int y=strokes[i][1]; y<=strokes[i][3]; y++)
				paint[strokes[i][0]][y]++;
		}
		
		// Vertical stroke.
		else {
			
			// Paint for all the different x values in range.
			for (int x=strokes[i][0]; x<=strokes[i][2]; x++)
				paint[x][strokes[i][1]]++;
		}
	}
	
	// Returns true iff (x,y) is in the grid.
	public static boolean inbounds(int x, int y) {
		return x >= 0 && x < r && y >= 0 && y < c;
	}

}

class djset {

	public int n;
	public int[] par;
	public int numC;
	
	// Makes an initial disjoint set of n different sets.
	public djset(int myn) {
		n = myn;
		par = new int[n];
		for (int i=0; i<n; i++)
			par[i] = i;
		numC = n;
	}
	
	// Returns the root of the tree storing v.
	public int find(int v) {
	
		// done!
		if (par[v] == v) return v;
		
		// Otherwise recursively find and update my parent to be the root!
		return par[v] = find(par[v]);
	}
	
	// Unions the sets containing u and v, returns false if they are in the same
	// set already and does nothing. Otherwise, the sets get unioned and true is returned.
	public boolean union(int u, int v) {
	
		// Get roots.
		u = find(u);
		v = find(v);
		
		// Together already.
		if (u == v) return false;
		
		// Attach v to u and return.
		par[v] = u;
		numC--;
		return true;
	}

}