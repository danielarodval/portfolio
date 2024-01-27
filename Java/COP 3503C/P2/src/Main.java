import java.util.Scanner;

/*
 * There are four unique ways of assigning the numbers to the vertices of the hexagram such that all of the sets of four numbers lines have the same sum (57 in this case).
 * All other ways may be obtained from these by rotation and/or reflection.
 * 
 * Given 12 distinct numbers, in how many ways, disregarding rotations and reflections, can you assign the number to the vertices such that the sum of the numbers along each of 6 straight lines passing through 4 vertices is the same?
 * 
 * The Input
 * There will be several test cases in the input.
 * Each test case will consist of twelve unique positive integers on a single line, with single spaces separating them.
 * All of the numbers will be less than 1,000,000.
 * The input will end with a line with twelve 0's.
 * 
 * The Output
 * For each test case, output the number of ways the numbers can be assigned to vertices such that the sum along each line of the hexagram is the same.
 * Put each answer on its own line.
 * Output no extra spaces, and do not separate answers with blank lines.
 * 
 * Sample Input
 * 3 17 15 18 11 22 12 23 21 7 9 13
 * 1 2 3 4 5 6 7 8 9 10 11 13
 * 0 0 0 0 0 0 0 0 0 0 0 0
 * 
 * Sample Output
 * 4
 * 0
 */

public class Main {

    public static boolean zero(int[] puzzle) {
        for (int i=0; i<12; i++) if (puzzle[i] != 0) return false;
        return true;
    }

    public static int answer(int[] puzzle) {
        int sum = 0;
        for (int i=0; i<12; i++) sum += puzzle[i];
        return sum / 6;
    }
    public static void main(String[] args) {

        //System.out.printf("Hello and welcome!");

        Scanner stdin = new Scanner(System.in);
        int[] puzzle = new int[12];

        for (int i=0; i<12; i++) puzzle[i] = stdin.nextInt();

        while (!zero(puzzle)) {
            //System.out.printf("The puzzle is: ");
            //for (int i=0; i<12; i++) System.out.printf("%d ", puzzle[i]);
            //System.out.printf("\n");

            System.out.printf("The answer is: %d\n", answer(puzzle));

            for (int i=0; i<12; i++) puzzle[i] = stdin.nextInt();
        }

        stdin.close();
    }
}