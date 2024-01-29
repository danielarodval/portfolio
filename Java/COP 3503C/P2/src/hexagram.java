/*
 * 
 * Daniel Rodriguez
 * COP 3503C
 */

import java.util.*;

public class hexagram {

    public static boolean zero(int[] puzzle) {
        for (int i = 0; i < 12; i++)
            if (puzzle[i] != 0)
                return false; // check if all zeros
        return true; // all zeros
    }

    public static int countSol(int[] puzzle, boolean[] used, int position, int magic) {
        // base case
        if (position == 12) {
            if (isValidHexagram(puzzle, magic))
                return 1;
            return 0;
        }

        int count = 0;

        // recursive case
        for (int i = 0; i < 12; i++) {
            if (!used[i]) {
                used[i] = true;
                int temp = puzzle[position]; // save current value
                puzzle[position] = puzzle[i]; // swap
                if (canBeValid(puzzle, position, magic)) { // check if valid
                    count += countSol(puzzle, used, position + 1, magic); // recurse
                }
                puzzle[position] = temp; // backtrack
                used[i] = false;
            }
        }

        return count;
    }

    public static boolean isValidHexagram(int[] puzzle, int magic) {
        int[][] lines = {
                { 0, 1, 2, 5 }, // top line of upper triangle
                { 0, 1, 4, 6 }, // left line of upper triangle
                { 2, 1, 4, 7 }, // right line of upper triangle
                { 3, 1, 4, 8 }, // left line of lower triangle
                { 5, 2, 4, 8 }, // right line of lower triangle
                { 3, 6, 7, 8 } // bottom line of lower triangle
        };

        for (int[] line : lines) {
            int sum = 0;
            for (int i : line)
                sum += puzzle[i];
            if (sum != magic) {
                // System.out.println("Line " + Arrays.toString(line));
                return false;
            }
        }

        return true;
    }

    public static boolean canBeValid(int[] puzzle, int position, int magic) {
        if (position >= 4 && position <= 8) {
            int sum = 0;
            
            for (int i = 0; i < 4; i++)
                sum += puzzle[i];

            if (sum > magic) // check if sum  big 
                return false;

            // System.out.println("Sum: " + sum);
        }

        return true;
    }

    public static void main(String[] args) {
        Scanner stdin = new Scanner(System.in);
        int[] puzzle = new int[12];
        int magic = 0;

        while (true) {
            // declare other variables here
            magic = 0;
            // read input for one case
            for (int i = 0; i < 12; i++) {
                puzzle[i] = stdin.nextInt();
                magic += puzzle[i]; // get magic sum
            }

            // process information
            if (zero(puzzle))
                break; // end loop if all zeros

            magic /= 6;
            int solution = countSol(puzzle, new boolean[12], 0, magic);

            // output answer for one case
            // System.out.println("Magic Solution: " + magic);
            // System.out.println("Number of Solutions: " + solution);
            System.out.println(solution);
        }

        stdin.close();
    }
}