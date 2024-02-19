/*
 * Daniel Rodriguez
 * COP 3503C
 * Section 0001
 * Program #3
 */

 import java.util.Scanner;

 public class connect {
    private static class DisJointSet {
        private int[] parent;
        private int[] rank;
        private int[] size; // size of each set
        private long totalConnectivity = 0; // sum of the sizes squared of each component

        public DisJointSet(int n) {
            parent = new int[n];
            rank = new int[n];
            size = new int[n];

            for(int i = 0; i < n; i++) { // initialize the disjoint set
                parent[i] = i;
                rank[i] = 0;
                size[i] = 1;
                totalConnectivity += 1;
            }
        }

        public int find(int u) {
            if(parent[u] != u) { // if u is not the root of the set
                parent[u] = find(parent[u]);
            }

            return parent[u];
        }

        public boolean union(int u, int v) {
            int rootU = find(u);
            int rootV = find(v);

            if(rootU == rootV) return false; // already connected
            
            if(rank[rootU] < rank[rootV]) { // if the rank of u is less than the rank of v
                parent[rootU] = rootV; // make v the parent of u
                size[rootV] += size[rootU]; // add the size of u to the size of v
                // casting to long
                totalConnectivity += ((long) (size[rootV] * size[rootV]) - (long) (size[rootU] * size[rootU]) - (long) ((size[rootV] - size[rootU]) * (size[rootV] - size[rootU])));
            } else if(rank[rootU] > rank[rootV]) { // etc
                parent[rootV] = rootU;
                size[rootU] += size[rootV];
                totalConnectivity += ((long) (size[rootU] * size[rootU]) - (long) (size[rootV] * size[rootV]) - (long) ((size[rootU] - size[rootV]) * (size[rootU] - size[rootV])));
            } else {
                parent[rootV] = rootU;
                rank[rootU]++;
                size[rootU] += size[rootV];
                totalConnectivity += ((long) (size[rootU] * size[rootU]) - (long) (size[rootV] * size[rootV]) - (long) ((size[rootU] - size[rootV]) * (size[rootU] - size[rootV])));
            }

            return true;
        }

        public long getConnectivity() {
            return totalConnectivity;
        }

        public int getNumSets() { // get the number of sets
            int numSets = 0;

            for(int i = 0; i < parent.length; i++) { // count the number of roots
                if(parent[i] == i) numSets++; // if the parent of i is i, then i is the root of the set
            }

            return numSets;
        }
    }

    public static long gcd(long a, long b) {
        if(b == 0) return a;
        return gcd(b, a % b);
    }

    public static void main(String[] args) {
        Scanner stdin = new Scanner(System.in);

        int n = stdin.nextInt();
        int m = stdin.nextInt();

        DisJointSet ds = new DisJointSet(n);

        for(int i = 0; i < m; i++) {
            int operation = stdin.nextInt();

            if(operation == 1) { // union
                int u = stdin.nextInt() - 1;
                int v = stdin.nextInt() - 1;

                ds.union(u,v);
            }else if(operation == 2) { // get connectivity
                long connectivity = ds.getConnectivity();
                long numSets = ds.getNumSets();
                //System.out.println(connectivity + "/" + numSets);
                System.out.println((connectivity / gcd(connectivity, numSets)) + "/" + (numSets / gcd(connectivity, numSets)));
            }else{ // invalid operation
                System.out.println("Invalid operation");
            }
        }
        stdin.close();
    }
 }