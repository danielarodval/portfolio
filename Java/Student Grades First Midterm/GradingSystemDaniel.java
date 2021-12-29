/*University of Central Florida
 *COP 3330 Spring 2019
 *Assignment #1
 *Author: Daniel Rodriguez
 */

import java.util.Arrays;
import java.util.Scanner;
public class GradingSystem {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		Scanner reader = new Scanner(System.in);
		
		System.out.print("Name: ");
		String name = reader.nextLine();
		System.out.print("# of Classes: ");
		int classes = reader.nextInt();
		
		String[] classnames = new String[classes];
		int[] grades = new int[classes];
		char[] lettergrade = new char[classes];
		
		for(int i = 0; i < classes; i++) {
			System.out.print("Name of Class: ");
			classnames[i] = reader.next();
			System.out.print("Grade: ");
			grades[i] = reader.nextInt();
		}
		
		int lg;
		for(int i = 0; i < classes; i++) {
			if(grades[i] >= 90) {
				lg = 1;
			}else if(grades[i] >= 80) {
				lg = 2;
			}else if(grades[i] >= 70) {
				lg = 3;
			}else if(grades[i] >= 60) {
				lg = 4;
			}else {
				lg = 5;
			}
			switch (lg){
			case 1:
				lettergrade[i] = 'A';
				break;
			case 2:
				lettergrade[i] = 'B';
				break;
			case 3:
				lettergrade[i] = 'C';
				break;
			case 4:
				lettergrade[i] = 'D';
				break;
			case 5:
				lettergrade[i] = 'F';
				break;
			}
		}
		
		System.out.print("\nGrades for " + name + "\nClasses\t\tScore\t\tGrade" + "\n-------------------------------------\n");
		
		for(int i = 0; i < classes; i++) {
			System.out.print(classnames[i] + "\t\t" + grades[i] + "\t\t" + lettergrade[i] + "\n");
		}
		
		int totalgrades = 0;
		for(int i = 0; i < classes; i++) {
			totalgrades += grades[i];
		}
		int totalscore = 0;
		totalscore = classes * 100;
		System.out.println("\nTotal Score out of " + totalscore + ":\t" + totalgrades);
		
		int highgrades = 0;
		for(int i = 0; i < classes; i++) {
			if (grades[i] > highgrades) {
				highgrades = grades[i];
			}
		}
		System.out.println("Highest Score out of " + classes + " Classes:\t"+ highgrades);
		
		int averagegrades = 0;
		averagegrades = totalgrades / classes;
		if(averagegrades >= 90) {
			lettergrade[1] = 'A';
		}else if(averagegrades >= 80) {
			lettergrade[1] = 'B';
		}else if(averagegrades >= 70) {
			lettergrade[1] = 'C';
		}else if(averagegrades >= 60) {
			lettergrade[1] = 'D';
		}else {
			lettergrade[1] = 'F';
		}
		System.out.println("Average Score: " + averagegrades);
		System.out.println("Average Grade: " + lettergrade [1]);
	}

}
