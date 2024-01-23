// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
/*
Daniel Rodriguez
COP 3503C
 */
import java.util.*;

public class sga {
    public static void main(String[] args) {
        //scan lines in (1)
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        sc.nextLine();

        //init nested map (1)
        Map<Character, Map<String, Integer>> nameMap = new HashMap<>();

        //reading names and populating nested map (n)
        for (int i = 0; i < n; i++){
            //reads in names
            String name = sc.nextLine();
            //gets first letter of each name
            char firstLetter = name.charAt(0);

            nameMap.putIfAbsent(firstLetter, new HashMap<>());
            Map<String, Integer> names = nameMap.get(firstLetter);
            names.put(name, names.getOrDefault(name, 0) + 1);
        }

        long totalPairs = 0;
        //calculating total pairs (n)
        for (Map<String, Integer> names : nameMap.values()){
            long sum = 0;
            long squareSum = 0;

            for (int count : names.values()){
                sum += count;
                squareSum += (long) count * count;
            }
            //System.out.println(sum);
            //System.out.println(squareSum);

            totalPairs += sum * sum - squareSum;
        }

        System.out.println(totalPairs);
    }
}