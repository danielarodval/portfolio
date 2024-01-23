/*
Daniel Rodriguez
COP 3503C
 */

import java.util.*;
public class dyslectionary {

    //function to sort the hashmap by a singular value
    public static HashMap<String, String> sortByValue(HashMap<String, String> toSort){
        List<Map.Entry<String, String> > list = new LinkedList<>(toSort.entrySet());
        //System.out.println(list);
        list.sort(Map.Entry.comparingByValue());

        HashMap<String, String> temp = new LinkedHashMap<>();

        for (Map.Entry<String, String> aa : list){
            temp.put(aa.getKey(), aa.getValue());
            //System.out.println(aa);
        }

        return temp;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (true){
            //init variables
            HashMap<String, String> dyslectionary = new HashMap<>();
            String word;
            int maxLength = 0;

            //read in inputs until a blank line is found
            while(sc.hasNextLine() && !(word=sc.nextLine()).isEmpty()){
                //reverse the word
                String reversed = new StringBuilder(word).reverse().toString();
                dyslectionary.put(word, reversed);

                //get the length of the longest word
                if (word.length() > maxLength) maxLength = word.length();
            }

            //sort hashmap
            dyslectionary = sortByValue(dyslectionary);

            //print hashmap
            for (Map.Entry<String, String> en : dyslectionary.entrySet()){
                System.out.println(" ".repeat(maxLength - en.getKey().length())+en.getKey());

            }

            if (!sc.hasNextLine()) {
                break;
            }
            System.out.println();
        }
    }
}
