/*
For Loops in Java
Passing Arrays in Java
*/
public class EnhancedForTest{
  public static void main(String[] args){
    int[] array = {87, 68, 94, 100, 83, 78, 85, 91, 76, 87};
    int total = 0;
    int highest;

    for (int number : array){
      total += number;
      if(highest < array[number]){
        highest = array[number];
      }
    }
    System.out.printf("Total of array elements: " + total)
    System.out.println("Highest number in array" + highest)

  }
}
/*

*/

public class Name{
  public static void main(String[] args){

  }
}
