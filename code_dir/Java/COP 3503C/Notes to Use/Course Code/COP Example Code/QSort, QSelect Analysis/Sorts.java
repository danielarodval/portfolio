// Arup Guha
// 7/16/2006
// Several of the sorts coded up for COP 3503 class...
/*** Edited/Fixed on 2/13/2024 ***/

import java.io.*;
import java.util.Random;
import java.lang.Math;

public class Sorts {

    final static int SIZE = 1000000;
    final static int RANGE = 1000000;
	final static int NUMQSELTESTS = 2000;
	
	// This is specifically for counting the sum of the array sizes in
	// calls to quickselect, which is a proxy for its runtime.
	public static long steps;
	
	// Part of my object.
    public int[] values;
	public Random gen;

    public static void main(String[] args) {
		testQuickSelect();
    }
	
	// Tests Quick Sort.
	public static void testQuickSort() {
		
		// Create our object.
		Sorts x = new Sorts();
		
		// Time and sort.
		long sT = System.currentTimeMillis();
		x.QuickSort(0, SIZE-1);
		long eT = System.currentTimeMillis();
		
		// Print out our result.
		if (!x.isSorted())
			System.out.println("Quick Sort failed.");
		else 
			System.out.println("Quick Sort succeeded. Time = "+(eT-sT)+" ms.");
	}
	
	// Tests Merge Sort.
	public static void testMergeSort() {
		
		// Create our object.
		Sorts x = new Sorts();
		
		// Time and test our sort.
		long sT = System.currentTimeMillis();
		x.MergeSort(0, SIZE-1);
		long eT = System.currentTimeMillis();
		
		// Print out our result.
		if (!x.isSorted())
			System.out.println("Merge Sort failed.");
		else 
			System.out.println("Merge Sort succeeded. Time = "+(eT-sT)+" ms.");
	}
	
	// Test Shell Sort.
	public static void testShellSort() {
		
		// Create our object.
		Sorts x = new Sorts();
		
		// Time and test our sort.
		long sT = System.currentTimeMillis();
		x.ShellSort();
		long eT = System.currentTimeMillis();
		
		// Print our result.
		if (!x.isSorted())
			System.out.println("Shell Sort failed.");
		else 
			System.out.println("Shell Sort succeeded. Time = "+(eT-sT)+" ms.");
	}
	
	// Test Counting Sort. NOTE: Don't run this with RANGE more than a few million.
	public static void testCountingSort() {
		
		// Create our object.
		Sorts x = new Sorts();
		
		// Time and test our sort.
		long sT = System.currentTimeMillis();
		x.CountingSort();
		long eT = System.currentTimeMillis();
		
		// Print our result.
		if (!x.isSorted())
			System.out.println("Counting Sort failed.");
		else 
			System.out.println("Counting Sort succeeded. Time = "+(eT-sT)+" ms.");
	}
	
	// Test Quick Select.
	public static void testQuickSelect() {
		
		// Create our object.
		Sorts x = new Sorts();	

		// Store random queries here and results.
		int[] place = new int[NUMQSELTESTS];
		int[] res = new int[NUMQSELTESTS];
		
		// Time and test NUMQSELTESTS times.
		long sT = System.currentTimeMillis();
		for (int i=0; i<NUMQSELTESTS; i++) {
			place[i] = x.gen.nextInt(SIZE);
			res[i] = x.QuickSelect(0, SIZE-1, place[i]);
		}
		long eT = System.currentTimeMillis();
		
		// Sort it to check.
		x.QuickSort(0, SIZE-1);
		
		// Just in case.
		if (!x.isSorted()) System.out.println("Test failed.");
		
		// See if any test failed.
		boolean worked = true;
		for (int i=0; i<NUMQSELTESTS; i++)
			if (x.values[place[i]] != res[i])
				worked = false;
			
		// Print results.
		if (!worked) System.out.println("Quick select didn't work.");
		else {
			System.out.println("All tests worked in "+(eT-sT)+ " ms.");
			
			/*** Note: This proves that our analysis, which shows a hidden
			           constant of just above 3, is fairly accurate. Namely,
					   in the set of all recursive calls from the initial,
					   the sum of array sizes is a bit more than 3 times the
					   original array size. That tiny leftover is the log part.
			***/
			System.out.println("Average steps = "+(1.0*steps/NUMQSELTESTS));
		}
	}

    // Constructor creates a sort object with random integers out of order.
    public Sorts() {
		gen = new Random();
		values = new int[SIZE];
		for (int i=0;i<values.length;i++)
			values[i] = gen.nextInt(RANGE);
	}

    // Prints out all the integers in the sort object in the current order
    // that they are stored.
    public void Print() {
		for (int i=0; i<values.length; i++)
			System.out.print(values[i]+" ");
		System.out.println();
    }

    // Implements the Counting Sort.
    public void CountingSort() {
	
		int[] temp = new int[RANGE]; // Temp array to store frequencies.
		int i,j;
		int counter;

		// Initialize and fill in temp array.
		for (i=0; i < temp.length; i++)
			temp[i] = 0;
		for (i=0; i < values.length; i++)
			temp[values[i]]++;

		// Copy values back into Sort object.
		i = 0;
		counter = 0;
		while (i < temp.length) {
			for (j=0;j<temp[i];j++) {
				values[counter] = i;
				counter++;
			}
			i++;
		}
	}

    // Pre-condition: low <= k <= high and low and high are valid indexes 
	//                into the Sorts object.
	// Post-condition: returns the value that would be in index k (0-based)
	//                 if the values in indexes [low,high] were sorted.
    public int QuickSelect(int low, int high, int k) {
		
		// Only one answer.
		if (low == high) return values[low];
		
		// Split it.
		int mid = Partition(low, high);
		
		// Go to the right of index mid.
		if (k > mid)
			return QuickSelect(mid+1, high, k);
		
		// We found it at index mid.
		else if (k == mid)
			return values[mid];
		
		// Must be on left side.
		else
			return QuickSelect(low, mid-1, k);
    }

    // Merges the elements from indeces low to high of the sort object.
    // mid is the last array index for the first set of numbers.
    public void Merge(int low, int mid, int high) {

		// Stores sorted list.
		int[] temp = new int[high - low + 1]; 
		
		// i is index into left, j into right, k into temp.
		int i = low, j = mid+1;
		
		// Go through each index in the new array in order.
		for (int k=0; k<temp.length; k++) {
			
			// Value must come from left side.
			if (j>high || (i<=mid && values[i] < values[j]))
				temp[k] = values[i++];
			
			// If not left, then right.
			else
				temp[k] = values[j++];
		}
		
		// Copy back.
		i = low;
		for (int k=0; k<temp.length; k++,i++)
			values[i] = temp[k];
	}

    // Performs a Merge Sort on the sort object.
    public void MergeSort(int low, int high) {
	
		// Done.
		if (low >= high) return;
		
		// Recursively sort left and right halves.
	    int mid = (low + high)/2;
	    MergeSort(low, mid);
	    MergeSort(mid+1,high);
		
		// Merge Together.
	    Merge(low,mid,high);
    }

    // Partitions the elements in the sort object in between array indexes
    // low and high, inclusive.
    public int Partition(int low, int high) {
		
		// My steps counter.
		steps += (high - low + 1);
	
		// Pick a random pivot.
		int rIdx = gen.nextInt(high-low+1) + low;
		int tmp = values[rIdx];
		values[rIdx] = values[low];
		values[low] = tmp;
		int part_elem = values[low];
		
		// i is low side, j is high side.
		int i = low+1;
		int j = high;

		// Loops until array is partitioned.
		while (i<=j) {
			
			// Move up low ptr until it finds a value out of range.
			while (i<=j && values[i]< part_elem) i++;
			
			// Same here with the high pointer.
			while (i<=j && values[j] >= part_elem) j--;

			// Swaps them, if necessary.
			if (i<j) {
				int temp = values[i];
				values[i] = values[j];
				values[j] = temp;
			}
		}
		
		// Swap partition element into place.
		int temp = values[j];
		values[j] = values[low];
		values[low] = temp;
		
		return j; // Return index of partition element.
    }

    // Implements a Quick Sort on the Sort object.
    public void QuickSort(int low, int high) {

		// Done.
		if (low >= high) return;
	
		// Find partition index.
	    int mid = Partition(low, high);
		
		// Sort left.
	    QuickSort(low, mid-1);
		
		// Sort right.
	    QuickSort(mid + 1, high);
    }
	
	// Returns true iff this object is sorted.
	public boolean isSorted() {
		for (int i=0; i<values.length-1; i++)
			if (values[i] > values[i+1])
				return false;
		return true;
	}

    // Implements a Shell Sort on the Sort object.
    public void ShellSort() {
	
		int gap = values.length/2;
		
		// Loops through the last pass, which sorts the entire list.
		while (gap > 0) {	

			// Loops for each "new" gap value.
			for (int i = gap; i < values.length; i++) {
				int temp = values[i];
				int j = i;
				
				// Performs one iteration of an insertion sort.
				while (j >= gap && temp < values[j - gap]) {
					values[j] = values[j - gap];
					j = j - gap;
				}
				values[j] = temp;
			}
			gap = gap/2; // Decreases gap.
		}
    }
}




