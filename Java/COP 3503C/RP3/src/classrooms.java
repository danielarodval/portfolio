/*
 * Classrooms problem on Kattis
 * 
 * The new semester is about to begin, and finding classrooms for orientation activities is always a headache.
 * 
 * There are k classrooms on campus and n proposed activies that need to be assigned a venue.
 * Every proposed activiety has a specific staring time si and ending time fi.
 * Any such an activity should take place at one of the classrooms.
 * Any of the k classrooms is big enough to hold any of the proposed acitivities, and each classroom can hold at most one acitvity at any time.
 * No two proposed activities can take place at the same classroom at the same time.
 * Even if two proposed activities overlap momentarily (the ending time of one activity equals the starting time aonther activity), they cannot be assigned to the same classroom.
 * 
 * There are so many proposed activities that there may not be enough classrooms to hold all the activities. It is desirable to have as many activities as possible. At most how many proposed activities can be assigned to a classroom?
 * 
 * Input:
 * The first line contains two positive integers n and k (1 <= k <= n <= 10^5), representing the number of proposed activities and the number of classrooms, respectively.
 * The following n lines each contains two positive integers: the ith line among these n lines contains si and fi (1 <= si <= fi <= 10^9), indicating the starting time and ending time of proposed activity i.
 * 
 * Output:
 * Output an integer indicating the maximum number proposed activites that can be scheduled.
 * 
 * Sample Input 1:
 * 4 2
 * 1 4
 * 2 9
 * 4 7
 * 5 8
 * 
 * Sample Output 1:
 * 3
 */
import java.util.*;

public class classrooms {
    public static void main(String[] args) {
        Scanner stdin = new Scanner(System.in);

        int n = stdin.nextInt(); // number of activities
        int k = stdin.nextInt(); // number of classrooms

        //store activities in a list of pairs (end, start)
        List<int[]> activities = new ArrayList<>();

        for (int loop = 0; loop < n; loop++) {
            int start = stdin.nextInt();
            int end = stdin.nextInt();
            activities.add(new int[]{end, start});
        }

        // sort activities by end time
        activities.sort(Comparator.comparingInt(a -> a[0]));

        // p queue for next available time
        PriorityQueue<Integer> availableClassrooms = new PriorityQueue<>();
        for (int i = 0; i < k; i++) {
            availableClassrooms.add(0);
        }

        int count = 0;

        for (int[] activity : activities) {
            int start = activity[1];
            int end = activity[0];

            if (availableClassrooms.peek() <= start) {
                availableClassrooms.poll();
                availableClassrooms.add(end);
                count++;
            }
        }

        System.out.println(count);

        stdin.close();
    }
}