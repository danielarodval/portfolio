/* COP 3330 Spring 2019. Midterm Exam
 * This code is written by: Daniel Rodriguez
 */

import java.util.Scanner;
import java.lang.Math;

class Calculator {
	private double num1;
	private double num2;
	
	public Calculator(double num1, double num2) {
		System.out.println("Add() result is: " + add(num1, num2));
		System.out.println("Sub() result is: " + sub(num1, num2));
		System.out.println("Mul() result is: " + mul(num1, num2));
		System.out.println("Div() result is: " + div(num1, num2));
	}
	
	public void setNum1(double num1) {
		this.num1 = num1;
	}
	
	public void setNum2(double num2) {
		this.num2 = num2;
	}
	
	public double getNum1(double num1) {
		return num1;
	}
	
	public double getNum2(double num2) {
		return num2;
	}
	
	public double add(double num1, double num2) {
		double sum;
		sum = num1 + num2;
		return sum;
	}
	
	public double sub(double num1, double num2) {
		double diff;
		diff = num1 - num2;
		return diff;
	}
	
	public double mul(double num1, double num2) {
		double product;
		product = num1 * num2;
		return product;
	}
	
	public double div(double num1, double num2) {
		double quotient;
		double rquotient;
		quotient = num1 / num2;
		rquotient = Math.round(quotient * 1000.0) / 1000.0;
		return rquotient;
	}	
}

class ScientificCalculator extends Calculator{

	ScientificCalculator(double num1, double num2){
		super(num1, num2);
	}
	
	
	public double power(double num1, double num2) {
		double power;
		power = Math.pow(getNum1(num1), getNum2(num2));
		return power;
	}

	public int remainder(double num1, double num2) {
		int remain;
		int rnum1 = (int) getNum1(num1);
		int rnum2 = (int) getNum2(num2);
		remain = Math.floorMod(rnum1, rnum2);
		return remain;
	}
	
	public double sinNum1(double num1) {
		double radian;
		double sin;
		double rsin;
		radian = Math.toRadians(getNum1(num1));
		sin = Math.sin(radian);
		rsin = Math.round(sin * 1000.0) / 1000.0;
		return rsin;
		
	}
	
	public double sqrtNum1(double num1) {
		double root;
		double rroot;
		root = Math.sqrt(getNum1(num1));
		rroot = Math.round(root * 1000.0) / 1000.0;
		return rroot;
	}
	
	public void Calculator(double num1, double num2) {
		System.out.println("Power() result is: " + power(getNum1(num1), getNum2(num2)));
		System.out.println("Remainder() result is: " + remainder(getNum1(num1), getNum2(num2)));
		System.out.println("SinNum1() result is: " + sinNum1(getNum1(num1)));
		System.out.println("SqrtNum1() result is: " + sqrtNum1(getNum1(num1)));
	}
}


public class CalculatorTest {
	public static void main(String[] args) {
		Scanner scan = new Scanner(System.in);
		
		System.out.print("Enter number 1: ");
		double num1 = scan.nextDouble();
		System.out.print("Enter number 2: ");
		double num2 = scan.nextDouble();
		System.out.println();
		
		ScientificCalculator calc = new ScientificCalculator(num1, num2);
		calc.Calculator(num1, num2);
		scan.close();
	}
}