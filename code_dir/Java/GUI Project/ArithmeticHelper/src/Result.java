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
import java.awt.Font;
import javax.swing.SwingConstants;
import javax.swing.JButton;
import java.awt.Color;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class Result extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;

	/**
	 * Launch the application.
	 */
	public void Run() {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Result frame = new Result();
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
	private static double correct = 0;
	private static long totalTime;
	private static double score;
	public Result() {
		setTitle("Result");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 466, 310);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblarithmeticHelperResult = new JLabel("***Arithmetic Helper Result***");
		lblarithmeticHelperResult.setForeground(Color.BLUE);
		lblarithmeticHelperResult.setHorizontalAlignment(SwingConstants.CENTER);
		lblarithmeticHelperResult.setFont(new Font("Tahoma", Font.PLAIN, 30));
		lblarithmeticHelperResult.setBounds(10, 11, 436, 37);
		contentPane.add(lblarithmeticHelperResult);
		
		JLabel lblPlayerName = new JLabel("Player Name: "
				+ User.nickName);
		lblPlayerName.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblPlayerName.setBounds(69, 48, 312, 20);
		contentPane.add(lblPlayerName);
		
		JLabel lblNumberOfProblems = new JLabel("Number of Problems: "
				+ User.problemsText);
		lblNumberOfProblems.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNumberOfProblems.setBounds(69, 69, 312, 20);
		contentPane.add(lblNumberOfProblems);
		
		JLabel lblCorrect = new JLabel("Correct: "
				+ (int) correct);
		lblCorrect.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblCorrect.setBounds(69, 89, 312, 20);
		contentPane.add(lblCorrect);
		
		JLabel lblTotalTimeTaken = new JLabel("Total Time Taken: "
				+ totalTime/1000/60/24
				+ " Hours "
				+ totalTime/1000/60
				+ " Minutes "
				+ totalTime/1000
				+ " Seconds ");
		lblTotalTimeTaken.setForeground(Color.RED);
		lblTotalTimeTaken.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblTotalTimeTaken.setBounds(20, 120, 436, 20);
		contentPane.add(lblTotalTimeTaken);
		//finds average time then rounds it to get minutes
		double averageTime = (((totalTime/1000) / User.problemsDoub) / 60);
		String strAverage = String.format("%.3f", averageTime);
		
		JLabel lblAverageTimeTaken = new JLabel("Average Time Taken for Each Problem: "
				+ strAverage
				+ " minutes");
		lblAverageTimeTaken.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblAverageTimeTaken.setBounds(69, 151, 387, 20);
		contentPane.add(lblAverageTimeTaken);
		
		JLabel lblPercentageOfCorrect = new JLabel("Percentage of Correct: "
				+ (correct / User.problemsDoub * 100)
				+ "%");
		lblPercentageOfCorrect.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblPercentageOfCorrect.setBounds(69, 169, 312, 20);
		contentPane.add(lblPercentageOfCorrect);
		
		JLabel lblScoreAchieved = new JLabel("Score Achieved: "
				+ (int) score);
		lblScoreAchieved.setForeground(Color.RED);
		lblScoreAchieved.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblScoreAchieved.setBounds(20, 200, 312, 20);
		contentPane.add(lblScoreAchieved);
		
		JButton btnHistory = new JButton("History");
		btnHistory.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				History his = new History();
				his.Run();
				correct = 0;
				dispose();
			}
		});
		btnHistory.setFont(new Font("Tahoma", Font.PLAIN, 15));
		btnHistory.setBounds(244, 231, 89, 23);
		contentPane.add(btnHistory);
		
		JButton btnFinish = new JButton("Finish");
		btnFinish.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});
		btnFinish.setFont(new Font("Tahoma", Font.PLAIN, 15));
		btnFinish.setBounds(117, 231, 89, 23);
		contentPane.add(btnFinish);
		//---------------------Sets User Inputs---------------------
		double[][] results = User.results;
		for (int i = 0; i < results.length; i++) {
			totalTime+=results[i][4];
			if (results[i][2] == results[i][3]) {
				correct+=1;
			}
		}
		//200 points for every correct answer, and the excess time is rewards in half points, 120 excess correct is 60 extra points
		score = ((correct * 200) + (((correct * 60) - (totalTime / 1000)) * .5));
	}
	public void setScore(double score) {
		Result.score = score;
	}
	
	public static double getScore() {
		return score;
	}
}
