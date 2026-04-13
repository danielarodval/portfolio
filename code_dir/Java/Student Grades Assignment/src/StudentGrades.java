/* University of Central Florida
 * COP 3330 Spring 2019
 * Assignment #2
 * Daniel Rodriguez
 */
public class StudentGrades {
	
    private static int studentCounter = 0;
    private String studentName;
    private double[] scores;
    private String[][] coursesLetterGrade;
    private int classes;


    public StudentGrades(String name) {
        studentName = name;
        studentCounter += 1;
        coursesLetterGrade = new String[2][2];
    }

    public StudentGrades(String studentName, double[] scores, String[] courses, int classes) {
        this.studentName = studentName;
        this.scores = scores;
        this.classes = classes;
        coursesLetterGrade = new String[scores.length][2];
        for(int i = 0; i < courses.length; i++) {
            coursesLetterGrade[i][0] = courses[i];
            coursesLetterGrade[i][1] = getLetterGrade(scores[i]);
        }
        studentCounter += 1;
    }

    public static String getLetterGrade(double score) {
        if (score >= 90) {
            return "A";
        }else if (score >= 80) {
            return "B";
        }else if (score >= 70) {
            return "C";
        }else if (score >= 60) {
            return "D";
        }else {
            return "F";
        }
    }

    public String getName() {
        return studentName;
    }

    public double getAverageScore() {
        double average = 0.0;
        for (double score : scores) {
            average += score;
        }
        return average / classes;
    }
    
    public void displayGrades() {
        System.out.println("Student Name: " + studentName);
        System.out.println(String.format("%-25s%20s%10s", "Course Name", "Letter Grade", "Score"));
        for (int i = 0; i < classes; i++) {
            System.out.println(String.format("%-25s%9.2s%21.2f",coursesLetterGrade[i][0],coursesLetterGrade[i][1],scores[i]));
        }
    }

    public static int getStudentCounter() {
        return studentCounter;
    }
}

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