/*
 * Daniel Rodriguez
 * COP 3503C - 0001
 */
import java.util.*;
// make interval with start and end time 
class Interval implements Comparable<Interval> {
    int start;
    int end;

    // constructor for interval
    Interval(int start, int end) {
        this.start = start;
        this.end = end;
    }

    // compare intervals by end time
    @Override
    public int compareTo(Interval other) {
        if (this.end == other.end) { // if end time is the same compare start
            return this.start - other.start;
        }
        return this.end - other.end;
    }
}

// make pair with available time and classroom id
class Pair implements Comparable<Pair> {
    int availableTime;
    int classroomId;

    // constructor for pair
    Pair(int availableTime, int classroomId) {
        this.availableTime = availableTime;
        this.classroomId = classroomId;
    }

    // compare pairs by available time
    @Override
    public int compareTo(Pair other) {
        if (this.availableTime == other.availableTime) { // if available time is the same compare classroom id
            return this.classroomId - other.classroomId;
        }
        return this.availableTime - other.availableTime;
    }
}

public class classrooms {
    public static void main(String[] args) {
        Scanner stdin = new Scanner(System.in);

        int n = stdin.nextInt(); // number of activities
        int k = stdin.nextInt(); // number of classrooms

        // store activities in custom list
        List<Interval> intervals = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            int start = stdin.nextInt();
            int end = stdin.nextInt();
            intervals.add(new Interval(start, end));
        }
        Collections.sort(intervals); // sort activities by end time
        
        // tree set for next available time
        TreeSet<Pair> availableClassrooms = new TreeSet<>();
        for (int i = 0; i < k; i++) {
            availableClassrooms.add(new Pair(0, i));
        }

        int count = 0;
        for (Interval interval : intervals) {
            // find the next available classroom
            Pair query = availableClassrooms.floor(new Pair(interval.start, k));
            if (query != null) { // if there is an available classroom
                int temp = query.classroomId; // temp close classroom id
                availableClassrooms.remove(query); // remove classroom from available
                availableClassrooms.add(new Pair(interval.end + 1, temp)); // add classroom with new available time
                count++;
            }
        }

        System.out.println(count);
    }
}
