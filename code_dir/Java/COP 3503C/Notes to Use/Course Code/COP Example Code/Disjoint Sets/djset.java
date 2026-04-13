// Arup Guha
// 1/23/2018
// Disjoint Set Implementation with Path Compression
// Written in COP 3503 class

import java.util.*;

public class djset {

	final public static int N = 10;

	public int[] parent;

	// Creates a disjoint set of size n (0, 1, ..., n-1)
	public djset(int n) {
		parent = new int[n];
		for (int i=0; i<n; i++)
			parent[i] = i;
	}

	public int find(int v) {

		// I am the club president!!! (root of the tree)
		if (parent[v] == v) return v;

		// Find my parent's root.
		int res = find(parent[v]);

		// Attach me directly to the root of my tree.
		parent[v] = res;
		return res;
	}

	public boolean union(int v1, int v2) {

		// Find respective roots.
		int rootv1 = find(v1);
		int rootv2 = find(v2);

		// No union done, v1, v2 already together.
		if (rootv1 == rootv2) return false;

		// Attach tree of v2 to tree of v1.
		parent[rootv2] = rootv1;
		return true;
	}

	// For testing.
	public void print() {
		for (int i=0; i<parent.length; i++)
			System.out.print(parent[i]+" ");
		System.out.println();
	}

	// Run a little test.
	public static void main(String[] args) {

		djset set = new djset(N);
		Random r = new Random();
		int numUnion = 0;

		// Union N-1 times.
		while (numUnion < N-1) {

			// Make v1 and v2 two distinct values.
			int v1 = r.nextInt(N);
			int v2 = v1;
			while (v2 == v1) v2 = r.nextInt(N);

			System.out.println("Union of "+v1+" and "+v2);
			boolean res = set.union(v1, v2);

			// Already in the same tree/set.
			if (!res)
				System.out.println("Already together");

			// Merge them.
			else {
				System.out.println("Merged the two trees.");
				numUnion++;
			}

			// Let's look at the set.
			set.print();
		}

	}
}
