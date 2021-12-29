/* University of Central Florida
* COP 3330 Spring 2019
* Final Project
* Author: <Daniel Rodriguez>
* PID: 4802087
*/ 
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import javax.swing.JOptionPane;

import java.awt.Font;
import javax.swing.SwingConstants;
import java.util.Random;
import javax.swing.JTextField;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Color;

public class Problems extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;

	/**
	 * Launch the application.
	 */
	public void Run(int n) {
		//sets counter to the initial input of user
		counter = n;
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Problems frame = new Problems();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	//declaring variables to be used in passing to other classes
	
	public static int counter;
	private int num1;
	private int num2;
	private double answer;
	private long start = System.currentTimeMillis();
	public static double[][] results = new double[User.problemsInt][5];
	
	
	private JTextField textField;
	
	public Problems() {
		setTitle("Arithmetic Helper");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 450, 300);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		//---------------------Randomly Generates Numbers for User---------------------
		Random rand = new Random();
		StringBuilder randNum1 = new StringBuilder();
		StringBuilder randNum2 = new StringBuilder("1");
		//makes the random numbers 0-9, 10-99, 100-999
		for(int i = 0; i < User.digitsInt; i++) {
			
			randNum1.append("9");
			if (User.digitsInt > 1) {
				if (i >= 2) {
					randNum2.append("0");
				}
			}else {
				randNum2.delete(0, 1);
				randNum2.append("0");
			}
		}
		int rnum1 = Integer.parseInt(randNum1.toString());
		int rnum2 = Integer.parseInt(randNum2.toString());
		
		num1 = rand.nextInt(rnum1 - rnum2) - rnum2;
		num2 = rand.nextInt(rnum1 - rnum2) - rnum2;
		//---------------------Labels for/from User---------------------
		JLabel lblProblems = new JLabel("###Problem "
				+ counter
				+ " of "
				+ User.problemsText
				+ "###");
		lblProblems.setForeground(Color.BLUE);
		lblProblems.setFont(new Font("Tahoma", Font.PLAIN, 20));
		lblProblems.setBounds(67, 46, 275, 25);
		contentPane.add(lblProblems);
		
		JLabel lblTitle = new JLabel("***Helper***");
		lblTitle.setForeground(Color.BLUE);
		lblTitle.setHorizontalAlignment(SwingConstants.CENTER);
		lblTitle.setFont(new Font("Tahoma", Font.PLAIN, 30));
		lblTitle.setBounds(0, 11, 436, 37);
		contentPane.add(lblTitle);
		
		JLabel lblNum1 = new JLabel("First Number: "
				+ num1);
		lblNum1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNum1.setBounds(90, 70, 210, 25);
		contentPane.add(lblNum1);
		
		JLabel lblNum2 = new JLabel("Second Number: "
				+ num2);
		lblNum2.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNum2.setBounds(90, 120, 210, 25);
		contentPane.add(lblNum2);
		
		JLabel lblOperation = new JLabel("Operation: ");
		lblOperation.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblOperation.setBounds(90, 95, 210, 25);
		contentPane.add(lblOperation);
		
		JLabel lblResult = new JLabel("Enter Result:");
		lblResult.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblResult.setBounds(67, 156, 87, 25);
		contentPane.add(lblResult);
		
		textField = new JTextField();
		textField.setForeground(Color.BLUE);
		textField.setFont(new Font("Tahoma", Font.PLAIN, 15));
		textField.setBounds(153, 158, 134, 24);
		contentPane.add(textField);
		textField.setColumns(10);
		
		JLabel lblPressNextTo = new JLabel("Press Next to See the Next Problem");
		lblPressNextTo.setHorizontalAlignment(SwingConstants.CENTER);
		lblPressNextTo.setBounds(90, 192, 235, 14);
		contentPane.add(lblPressNextTo);
		
		JButton btnNext = new JButton("Next");
		btnNext.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String response = textField.getText();
				if (isNumeric(response) == true) {
					//saves data into 2d array, in counter represents rows and the info is saved in columns
					results[counter-1][0] = num1;
					results[counter-1][1] = num2;
					results[counter-1][2] = Double.parseDouble(textField.getText());
					results[counter-1][3] = answer;
					long end = System.currentTimeMillis();
					results[counter-1][4] = end-start;
					//repeats the statement depending on how many problems user asked for		
					if(counter < User.problemsInt) {
						counter++;
						//moves to next instance of problem
						Run(counter);
						dispose();
					}else {
						//goes to next window
						Result res = new Result();
						res.Run();
						dispose();
						/*
						 * the user here has an option to exit after result, in order
						 * retain the data entered by the user without having to go
						 * to the end of the program, the necessary components are ran here
						 * user class handles all of it, taking from the later classes
						 * as well because result is the only one with the time functions
						 * and i didn't want to implement that into user
						 * I have thus far clocked in 24 hours of coding, and i feel like death
						 * incarnate
						 */
						User use = new User();
						use.fileWriter();
						use.fileSorter();
					}
				}else {
					JOptionPane.showMessageDialog(null, "Please enter a valid number!");
				}
			}
		});
		btnNext.setFont(new Font("Tahoma", Font.PLAIN, 15));
		btnNext.setBounds(166, 217, 89, 23);
		contentPane.add(btnNext);
		//---------------------Sets User Inputs---------------------
		String operand = User.operand;
		if(operand == "+") {
			lblTitle.setText("***Addition Helper***");
			lblOperation.setText("Operation: Addition(+)");
			double temp = num1 + num2;
			String round = String.format("%f", temp);
			answer = Double.parseDouble(round);
		}else if (operand == "-") {
			lblTitle.setText("***Subtraction Helper***");
			lblOperation.setText("Operation: Subtraction(-)");
			double temp = num1 - num2;
			String round = String.format("%f", temp);
			answer = Double.parseDouble(round);
		}else if (operand == "*") {
			lblTitle.setText("***Multiplication Helper***");
			lblOperation.setText("Operation: Multiplication(*)");
			double temp = num1 * num2;
			String round = String.format("%f", temp);
			answer = Double.parseDouble(round);
		}else if (operand == "/") {
			lblTitle.setText("***Division Helper***");
			lblOperation.setText("Operation: Division(/)");
			//if either is zero formatting doesnt work and crashes
			if (num1 != 0 && num2 != 0) {
				double temp = num1 / num2;
				String round = String.format("%2f", temp);
				answer = Double.parseDouble(round);
			}else {
				answer = num1 / num2;
			}
		}
	}
	//---------------------Getters and Setters---------------------
	public void setResults(double[][] results) {
		Problems.results = results;
	}
	
	public static double[][] getResults() {
		return results;
	}
	//---------------------Checks Strings for Numbers---------------------
	@SuppressWarnings("unused")
	public static boolean isNumeric(String strNum) {
	    try {
	        double d = Double.parseDouble(strNum);
	    } catch (NumberFormatException | NullPointerException nfe) {
	        return false;
	    }
	    return true;
	}
}
