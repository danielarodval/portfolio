import java.util.Random;

public class StudentGradesTest {

    public static void main(String[] args) {
    	try {
    	int ns = Integer.parseInt(args[0]);
    	int nc = Integer.parseInt(args[1]);

        String[] names = {"Adam Smith", "Nusair Ahmed", "Muhammad Mustafa", "Christian Thomsen", "Debashish Roy"};
        String[] courses =
                {"Java Programming", "Data Science", "Database Systems", "Computer Organization", "Data Structure"};
        double avgscore = 0;
        double topscore = 0;
        String topstudent = null;
        String topgrade = null;
        
        Random random = new Random();
        int low = 45;
		int high = 95;

        for (int i = 0; i < ns; i++) {

            double[] rscore = new double[5];
            
            for(int j = 0; j < nc; j++) {
            	rscore[j] = random.nextInt(high - low) + low;
            }

            StudentGrades studentGrades = new StudentGrades(names[i], rscore, courses, nc);
            studentGrades.displayGrades();
            System.out.println();         
 
            if (avgscore < studentGrades.getAverageScore()) {
            	avgscore = studentGrades.getAverageScore();
            	topscore = studentGrades.getAverageScore();
            	topstudent = studentGrades.getName();
            	topgrade = StudentGrades.getLetterGrade(studentGrades.getAverageScore());
            }
            //System.out.println(studentGrades.getName() + " Average Score: " + studentGrades.getAverageScore());
            //System.out.println(studentGrades.getName() + " Average Grade: " + StudentGrades.getLetterGrade(studentGrades.getAverageScore()));
        }
        System.out.println("Highest Average Student: " + topstudent);
        System.out.printf("\nAverage Score & Grade: " + topscore + ", " + topgrade);
    	}
		catch(ArrayIndexOutOfBoundsException e) {
		System.out.println("Too high of number on one of the variables");
		}
    }
}