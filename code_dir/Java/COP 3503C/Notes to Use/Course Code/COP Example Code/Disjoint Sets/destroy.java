// Arup Guha
// 2/10/2022
// Solution to COP 3503 Program #3: Destroying Connections

import java.util.*;

public class destroy {

	public static void main(String[] args) {
	
		// Get basic parameters.
		Scanner stdin = new Scanner(System.in);
		int numV = stdin.nextInt();
		int numE = stdin.nextInt();
		int numD = stdin.nextInt();
		
		// Store edges as pairs.
		int[][] edges = new int[numE][2];
		for (int i=0; i<numE; i++) {
			edges[i][0] = stdin.nextInt()-1;
			edges[i][1] = stdin.nextInt()-1;
		}
		
		// At first we say everything is in.
		boolean[] in = new boolean[numE];
		Arrays.fill(in, true);
		
		// Store the edges in the order that they get destroyed, marking them as out,
		// for now.
		int[] destroy = new int[numD];
		for (int i=0; i<numD; i++) {
			destroy[i] = stdin.nextInt()-1;
			in[destroy[i]] = false;
		}
		
		// Create my disjoint set.
		djset dj = new djset(numV);
		
		// Add in all edges that never got destroyed.
		for (int i=0; i<numE; i++)
			if (in[i])
				dj.union(edges[i][0], edges[i][1]);
		
		// Store all results here.
		long[] res = new long[numD+1];
		res[numD] = dj.getConnectivity();
		
		// No go backwards through the history, adding in destroyed edges.
		for (int i=numD-1; i>=0; i--) {
		
			// Put together!
			dj.union(edges[destroy[i]][0], edges[destroy[i]][1]);
		
			// Store new answer.
			res[i] = dj.getConnectivity();
		}

		// Ta da!
		for (int i=0; i<=numD; i++)
			System.out.println(res[i]);

	}
}

class djset {

	private int[] par;
	private long[] size;
	private long sumSizeSq;
	
	// Creates a new disjoint set of n items.
	public djset(int n) {
	
		// Allocate memory for both arrays.
		par = new int[n];
		size = new long[n];
		
		// Initialize to separate sets of size 1.
		for (int i=0; i<n; i++) {
			par[i] = i;
			size[i] = 1;
		}
		sumSizeSq = n;
	}	
	
	// Find function with path compression.
	public int find(int v) {
		if (par[v] == v) return v;
		return par[v] = find(par[v]);
	}
	
	// Unions the set storing u with the set storing v. If both are in the same set, no action is taken
	// and false is returned.
	public boolean union(int u, int v) {
	
		// Get both parents.
		u = find(u);
		v = find(v);
		
		// Nothing to be done.
		if (u == v) return false;
		
		// New size.
		long newSize = size[u] + size[v];
		sumSizeSq += (newSize*newSize - (size[u]*size[u] + size[v]*size[v]));
		
		// Note: mathematically, this is equivalent to 
		// sumSizeSq += 2*size[u]*size[v];
		
		// Merge trees and update sizes.
		par[v] = u;
		size[u] += size[v];
		size[v] = -1;
		return true;
	}
	
	// Returns the connectivity of the set.
	public long getConnectivity() {
		return sumSizeSq;
	}
}