// Arup Guha
// Started on 2/5/2022, "finished" on 2/8/2022
// Skip List Implementation

import java.util.*;

public class skiplistset {

	final public static int NEG_INF = Integer.MIN_VALUE;
	final public static int POS_INF = Integer.MAX_VALUE;
	
	public static Random rndObj = new Random();
	
	private ArrayList<node> levels;
	private int size;
	
	// Makes an empty list.
	public skiplistset() {

		// Initially, I am just one level with min and max.
		levels = new ArrayList<node>();
		levels.add(buildLevel(0));
		size = 1;
	}

	// This builds level id to be an empty level.
	public node buildLevel(int id) {
		node first = new node(NEG_INF, id);
		node last = new node(POS_INF, id);
		first.next = last;
		last.prev = first;		
		return first;
	}
	
	// Returns a list of nodes at each level that are right before value.
	public ArrayList<node> search(int value) {
		
		// Store answers here.
		ArrayList<node> res = new ArrayList<node>();
		node cur = levels.get(size-1);
		
		// We search from top, so that we can skip terms.
		for (int i=size-1; i>=0; i--) {
			
			// Go down this level until we're right before an equal or bigger item.	
			while (cur.next.data < value) cur = cur.next;
			
			// This is the floor of value on this list, so add it.
			res.add(cur);
				
			// Go down to the next level.	
			if (i>0) cur = cur.down;
		}
		
		// So the list will be in the proper order, since I built it backwards.
		Collections.reverse(res);
		
		// Stores all of the relevant pointers.
		return res;
	}
	
	// Inserts value into the set, returns true iff the value was inserted. (False means the
	// value was already in the set.
	public boolean insert(int value) {
				
		// Find all the "previous" nodes.
		ArrayList<node> beforeList = search(value);
		
		// This value is already in the set.
		if (beforeList.get(0).next.data == value) return false;
		
		// Temp pointer I will use.
		node curn = null;
		
		int i = 0;
		
		// Farthest we'll go up the lists.
		while (i <= size) {
			
			// Get out 50% of the time, unless first time.
			int val = i==0 ? 1 : rndObj.nextInt(2);
			if (val == 0) break;
			
			// We've decided to create this node.
			node newn = new node(value, i);
			
			// Not necessary for bottom level.
			if (i > 0) {
				curn.up = newn;
				newn.down = curn;
			}
			
			// Special case where we are adding a new level to our list.
			// We add the level and then connect it to the rest of the lists.
			if (i == size) {
				node nextL = buildLevel(size);
				levels.add(nextL);
				connectLastLevel();
				beforeList.add(nextL);
			}
			
			// Lots of patching...
			node tmpLow = beforeList.get(i);
			node tmpNext = tmpLow.next;
			newn.prev = tmpLow;
			newn.next = tmpNext;
			tmpLow.next = newn;
			tmpNext.prev = newn;
			
			// Need to update the object's size and get out.
			if (i == size) {
				size++;
				break;
			}
			
			// Go up next level.
			i++;
			curn = newn;
		}
		
		// We inserted it.
		return true;
	}
	
	// Deletes value from the list. Returns true if value was in the list and was deleted.
	// Returns false if value wasn't in the list and takes no action.
	public boolean delete(int value) {
		
		// See if it's in the list or not.
		ArrayList<node> beforeList = search(value);
		node bottom = beforeList.get(0);
		
		// If not, indicate that we can't delete it.
		if (bottom.next.data != value) return false;
		
		// This is who we delete.
		node cur = bottom.next;
		
		// Go up the skip list.
		while (cur != null) {
			
			// Get the two to patch.
			node pNode = cur.prev;
			node nNode = cur.next;
			
			// Patch!
			pNode.next = nNode;
			nNode.prev = pNode;
			
			// Go up one level.
			cur = cur.up;
		}
		
		// Just in case we can trim.
		if (size > 1 && topLevelSize() == 2) {
			levels.remove(size-1);
			size--;
		}
	
		// Delete is completed.
		return true;
	}
	
	// Returns the number of items on the top level.
	private int topLevelSize() {
		node cur = levels.get(size-1);
		int sz = 0;
		while (cur != null) {
			cur = cur.next;
			sz++;
		}
		return sz;
	}
	
	// Connects the last level to the rest of the lists.
	public void connectLastLevel() {
		
		// We can obtain both of these.
		node top = levels.get(levels.size()-1);
		node below = levels.get(levels.size()-2);
		
		// Link left sides up and down.
		top.down = below;
		below.up = top;
		
		// End of top list.
		top = top.next;
		
		// Go to end of second to top list.
		while (below.data != POS_INF) below = below.next;
		
		// Link right sides up and down.
		top.down = below;
		below.up = top;
	}
	
	// For debugging.
	public void printAllLevels() {
		System.out.println(levels.size()+" and "+size);
		for (int i=0; i<size; i++) {
			System.out.print("Level "+i+": ");
			printLevel(i);
		}
		System.out.println("---------------------------");
	}
	
	// Prints level id. For debugging.
	public void printLevel(int id) {
		node cur = levels.get(id);
		while (cur != null) {
			System.out.print(cur.data+" ");
			cur = cur.next;
		}
		System.out.println();
	}
	
	// String version of the list. Just prints the bottom level.
	public String toString() {
		StringBuffer sb = new StringBuffer();
		sb.append("Levels "+size+": List is ");
		node cur = levels.get(0);
		while (cur.data != POS_INF) {
			if (cur.data != NEG_INF) 
				sb.append(cur.data+"");
			if (cur.next.data != POS_INF)
				sb.append(", ");
			cur = cur.next;
		}
		return sb.toString();
	}
	
	// Basic insert test.
	public static void basicInsertTest() {
		
		// Create the object.
		skiplistset mine = new skiplistset();
		
		// Do 100 inserts.
		for (int i=0; i<100; i++) {
			
			// Generate the item.
			int item = rndObj.nextInt(1000);
			System.out.println("Gen "+item);
			
			// Insert it.
			boolean flag = mine.insert(item);
			
			// Print what happened.
			if (flag)
				System.out.println("Inserted "+item);
			else
				System.out.println("Rejected "+item);
			
			// See all the lists.
			mine.printAllLevels();
		}		
	}
	
	// Just for timing purposes.
	public static void speedInsertTest() {
		skiplistset mine = new skiplistset();
		for (int i=0; i<1000000; i++) {
			int item = rndObj.nextInt(1000000000);
			mine.insert(item);
		}		
	}
	
	// I tested the Skip List agains Java's TreeSet.
	public static void tsInsertTest() {
		TreeSet<Integer> mine = new TreeSet<Integer>();
		for (int i=0; i<1000000; i++) {
			int item = rndObj.nextInt(1000000000);
			mine.add(item);
		}		
	}	
	
	// Testing both inserts and deletes together.
	public static void basicInsertDeleteTest() {
		
		// Create the object.
		skiplistset mine = new skiplistset();
		
		// Do 40 operations.
		for (int i=0; i<40; i++) {
			
			// Get the next item and action.
			int item = rndObj.nextInt(10);
			int action = rndObj.nextInt(4);
			
			// I am making 75% inserts.
			if (action > 0) {
			
				// Print log of insert.
				System.out.println("Inserting "+item);
				boolean flag = mine.insert(item);
				if (flag)
					System.out.println("Inserted "+item);
				else
					System.out.println("Rejected "+item);
			}
			
			// 25% deletes.
			else {
				
				// Same here.
				boolean flag = mine.delete(item);
				if (flag)
					System.out.println("Deleted "+item);
				else
					System.out.println(item+" can not be deleted.");
			}
			
			// Ta da!
			mine.printAllLevels();
		}		
	}	
	
	// Performs a large test with inserts followed by deletes in a pattern.
	public static void largeTestPattern() {
		
		// Make a list of items to insert, then delete.
		int[] insert = new int[1000000];
		for (int i=0; i<1000000; i++)
			insert[i] = (7*i+2)%2000000;
		int[] del = new int[1000000];
		for (int i=0; i<1000000; i++)
			del[i] = (5*i+1)%2000000;
		
		// Set up skip list.
		skiplistset myset = new skiplistset();
		
		// Start timer.
		long sSkip = System.currentTimeMillis();
		
		// Insert all.
		for (int i=0; i<1000000; i++)
			myset.insert(insert[i]);
		
		// Delete ones on this list that are in the first list.
		for (int i=0; i<1000000; i++)
			myset.delete(del[i]);
		
		// End timer and print.
		long eSkip = System.currentTimeMillis();
		System.out.println("Skip list actions took "+(eSkip-sSkip)+" ms.");
		
		// Now do it with a tree st.
		TreeSet<Integer> ts = new TreeSet<Integer>();
		
		long sTS = System.currentTimeMillis();
		
		for (int i=0; i<1000000; i++)
			ts.add(insert[i]);		
		
		for (int i=0; i<1000000; i++)
			if (ts.contains(del[i]))
				ts.remove(del[i]);
			
		long eTS = System.currentTimeMillis();
		System.out.println("tree set actions took "+(eTS-sTS)+" ms.");
		
		// Get both sets of numbers sorted in a list.
		ArrayList<Integer> skipOrder = myset.getList();
		ArrayList<Integer> tsOrder = get(ts);
		
		// Print if it worked or not.
		if (!equal(skipOrder, tsOrder))
			System.out.println("Didn't work.");
		else
			System.out.println("Worked!");
	}
	
	// A large test of random inserts followed by random deletes.
	public static void largeTestRandom() {
		
		// Make a list of items to insert, then delete.
		int[] insert = new int[1000000];
		for (int i=0; i<1000000; i++)
			insert[i] = rndObj.nextInt(2000000);
		int[] del = new int[1000000];
		for (int i=0; i<1000000; i++)
			del[i] = rndObj.nextInt(2000000);
		
		// Set up skip list.
		skiplistset myset = new skiplistset();
		
		// Start timer.
		long sSkip = System.currentTimeMillis();
		
		// Insert all.
		for (int i=0; i<1000000; i++)
			myset.insert(insert[i]);
		
		// Delete ones on this list that are in the first list.
		for (int i=0; i<1000000; i++)
			myset.delete(del[i]);
		
		// End timer and print.
		long eSkip = System.currentTimeMillis();
		System.out.println("Skip list actions took "+(eSkip-sSkip)+" ms.");
		
		// Now do it with a tree st.
		TreeSet<Integer> ts = new TreeSet<Integer>();
		
		long sTS = System.currentTimeMillis();
		
		for (int i=0; i<1000000; i++)
			ts.add(insert[i]);		
		
		for (int i=0; i<1000000; i++)
			if (ts.contains(del[i]))
				ts.remove(del[i]);
			
		long eTS = System.currentTimeMillis();
		System.out.println("tree set actions took "+(eTS-sTS)+" ms.");
		
		// Get both sets of numbers sorted in a list.
		ArrayList<Integer> skipOrder = myset.getList();
		ArrayList<Integer> tsOrder = get(ts);
		
		// Print if it worked or not.
		if (!equal(skipOrder, tsOrder))
			System.out.println("Didn't work.");
		else
			System.out.println("Worked!");
	}
	
	// Returns true iff lists a and b are equal (same # of terms in the same order)
	public static boolean equal(ArrayList<Integer> a, ArrayList<Integer> b) {
		
		// Can't be equal.
		if (a.size() != b.size()) return false;
		
		// See if anything is unequal.
		for (int i=0; i<a.size(); i++)
			if (!a.get(i).equals( b.get(i)))
				return false;
			
		// Good if we get here.
		return true;
	}
	
	// Returns all the items in the skip list in order.
	public ArrayList<Integer> getList() {
		node bottom = levels.get(0);
		ArrayList<Integer> res = new ArrayList<Integer>();
		bottom = bottom.next;
		while (bottom.data != POS_INF) {
			res.add(bottom.data);
			bottom = bottom.next;
		}
		return res;
	}
	
	// Returns all items of the treeset in order.
	public static ArrayList<Integer> get(TreeSet<Integer> ts) {
		ArrayList<Integer> res = new ArrayList<Integer>();
		while (ts.size() > 0) res.add(ts.pollFirst());
		return res;
	}
	
	public static void main(String[] args) {
		largeTestPattern();
	}
	
}

class node {

	public int data;
	public node next;
	public node prev;
	public node up;
	public node down;
	public int level;

	public node(int myval, int mylev) {
		data = myval;
		level = mylev;
		next = null;
		prev = null;
		up = null;
		down = null;
	}

}