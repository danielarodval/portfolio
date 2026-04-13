/*
 * Daniel Rodriguez
 * COP 3503C - 0001
 * RP4: Breaking Bad
 */

import java.util.*;
import java.io.*;

public class breakingbad {

    // declaring static variables
    static Map<String, List<String>> graph = new HashMap<>();
    static Map<String, Integer> colors = new HashMap<>();
    static List<String> walterList =  new ArrayList<>(); // list of walter's items
    static List<String> jesseList =  new ArrayList<>(); // list of jesse's items
    static boolean isPossible = true;

    public static void main(String[] args) throws IOException { // catch to use the FastScanner thingy
        FastScanner stdin = new FastScanner(System.in);

        int n = stdin.nextInt(); // read in the number of elements
        for(int i = 0; i < n; i++) {
            String item = stdin.next();
            graph.put(item, new ArrayList<>());
            colors.put(item, -1); // -1 means not visited
        }

        int m = stdin.nextInt(); // read in sus pairs
        for(int i = 0; i < m; i++) {
            String item1 = stdin.next();
            String item2 = stdin.next();
            // add each item of pair as neighbor of other
            graph.get(item1).add(item2);
            graph.get(item2).add(item1);
        }

        // attempt two color graph
        for(String item : graph.keySet()) {
            if(colors.get(item) == -1) { //item no visited
                if(!dfs(item, 0)) { // init dfs with color 0
                    isPossible = false;
                    break;
                }
            }
        }
        
        // print eveyrthing
        if(isPossible) {
            walterList.forEach(item -> System.out.print(item + " "));
            System.out.println();
            jesseList.forEach(item -> System.out.print(item + " "));
        } else {
            System.out.println("impossible");
        }
    }

    static boolean dfs(String item, int color) { // depth first search is what dfs means
        if(colors.get(item) != -1) {
            return colors.get(item) == color; // check no color likey (conflict)
        }

        colors.put(item, color); // color curr item

        if(color == 0) { // add to matching list
            walterList.add(item);
        } else {
            jesseList.add(item);
        }

        for(String neighbor : graph.get(item)) { // check neighbors
            if(!dfs(neighbor, 1 - color)) {
                return false;
            }
        }

        return true;
    }
}

// FastScanner from redbluetree.java
class FastScanner {
 
	BufferedReader br;
	StringTokenizer st;
 
	public FastScanner(InputStream i) {
		br = new BufferedReader(new InputStreamReader(i));
		st = new StringTokenizer("");
	}
 
	public String next() throws IOException {
		if(st.hasMoreTokens())
			return st.nextToken();
		else
			st = new StringTokenizer(br.readLine());
		return next();
	}
 
	public int nextInt() throws IOException {
		return Integer.parseInt(next());
	}

	public long nextLong() throws IOException {
		return Long.parseLong(next());
	}
}