// Arup Guha
// 2/7/2018
// Example for COP 3503: Radix sort of array of ints (on bytes)

import java.util.*;

public class radix {

	final public static int HALFBYTE = (1<<7);
	final public static int FULLBYTE = (1<<8)-1;
	final public static int BYTESIZE = 8;
	final public static int N = 10000000;

	public static void main(String[] args) {

		// Make two copies of a random array.
		Random r = new Random();
		int[] arr = new int[N];
		for (int i=0; i<N; i++)
			arr[i] = r.nextInt();
		int[] arrcopy = Arrays.copyOf(arr, N);

		long start = System.currentTimeMillis();
		arr = radixSortByte(arr);
		long end = System.currentTimeMillis();

		// Print if it's sorted.
		if (isSorted(arr))
			System.out.println("Sorted!!!");
		else
			System.out.println("Sorry, this didn't work.");

		System.out.println("Time was "+(end-start)+" ms.");

		// Test against Arrays.sort!
		start = System.currentTimeMillis();
		Arrays.sort(arrcopy);
		end = System.currentTimeMillis();
		System.out.println("Arrays.sort took "+(end-start)+" ms.");
	}

	// Counting sort treating each byte as a unite.
	public static int[] countingSortByte(int[] arr, int block, boolean neg) {

		// Find how many of this byte are each value.
		int[] freq = new int[1<<BYTESIZE];
		for (int i=0; i<arr.length; i++) {
			int index = !neg ? ((arr[i]>>(block*BYTESIZE))&FULLBYTE) : (((arr[i]>>(block*BYTESIZE))+HALFBYTE)&FULLBYTE);
			freq[index]++;
		}

		// Cumulative frequency.
		freq[0]--;
		for (int i=1; i<=FULLBYTE; i++)
			freq[i] += freq[i-1];

		// Store values in their correct slots, staying stable.
		int[] res = new int[arr.length];
		for (int i=arr.length-1; i>=0; i--) {
			int index = !neg ? ((arr[i]>>(block*BYTESIZE))&FULLBYTE) : (((arr[i]>>(block*BYTESIZE))+HALFBYTE)&FULLBYTE);
			res[freq[index]--] = arr[i];
		}
		return res;
	}

	// Radix sort by byte, go byte by byte.
	public static int[] radixSortByte(int[] arr) {
		for (int i=0; i<4; i++)
			arr = countingSortByte(arr, i, i==3);
		return arr;
	}

	// For long arrays...
	public static boolean isSorted(int[] arr) {
		for (int i=0; i<arr.length-1; i++)
			if (arr[i] > arr[i+1])
				return false;
		return true;
	}

	// Add for testing...
	public static void print(int[] arr) {
		for (int i=0; i<arr.length; i++)
			System.out.print(arr[i]+" ");
		System.out.println();
	}
}