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
import javax.swing.JTextField;
import java.awt.Color;
import java.awt.Dimension;

import javax.swing.SwingConstants;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.BorderLayout;
import java.awt.CardLayout;
import javax.swing.JScrollPane;
import javax.swing.ScrollPaneConstants;

public class History extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JTextField txtNumber1;
	private JTextField txtNumber2;
	private JTextField txtRealResult;
	private JTextField txtYourResult;
	private JPanel panel;
	private JScrollPane scrollPane;

	/**
	 * Launch the application.
	 */
	public void Run() {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					History frame = new History();
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
	public History() {
		setTitle("History");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 600, 550);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(new CardLayout(0, 0));
		//panel declared to be able to adjust and not change window size
		panel = new JPanel();
		contentPane.add(panel, "name_62895619052060");
		panel.setLayout(null);
		panel.setPreferredSize(getSize());
		
		JLabel lblYour = new JLabel("YOUR    PLAYING    RECORDS    BELOW");
		lblYour.setBounds(35, 50, 503, 31);
		panel.add(lblYour);
		lblYour.setForeground(Color.BLUE);
		lblYour.setFont(new Font("Tahoma", Font.BOLD, 25));
		//---------------------Text Fields---------------------
		txtNumber1 = new JTextField();
		txtNumber1.setBounds(10, 120, 130, 120);
		panel.add(txtNumber1);
		txtNumber1.setBackground(Color.WHITE);
		txtNumber1.setHorizontalAlignment(SwingConstants.CENTER);
		txtNumber1.setEditable(false);
		txtNumber1.setText("Number 1");
		txtNumber1.setForeground(Color.RED);
		txtNumber1.setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtNumber1.setColumns(10);
		
		txtNumber2 = new JTextField();
		txtNumber2.setBounds(146, 120, 130, 120);
		panel.add(txtNumber2);
		txtNumber2.setBackground(Color.WHITE);
		txtNumber2.setText("Number 2");
		txtNumber2.setHorizontalAlignment(SwingConstants.CENTER);
		txtNumber2.setForeground(Color.RED);
		txtNumber2.setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtNumber2.setEditable(false);
		txtNumber2.setColumns(10);
		
		txtRealResult = new JTextField();
		txtRealResult.setBounds(283, 120, 130, 120);
		panel.add(txtRealResult);
		txtRealResult.setBackground(Color.WHITE);
		txtRealResult.setText("Real Result");
		txtRealResult.setHorizontalAlignment(SwingConstants.CENTER);
		txtRealResult.setForeground(Color.RED);
		txtRealResult.setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtRealResult.setEditable(false);
		txtRealResult.setColumns(10);
		
		txtYourResult = new JTextField();
		txtYourResult.setBounds(419, 120, 130, 120);
		panel.add(txtYourResult);
		txtYourResult.setBackground(Color.WHITE);
		txtYourResult.setText("Your Result");
		txtYourResult.setHorizontalAlignment(SwingConstants.CENTER);
		txtYourResult.setForeground(Color.RED);
		txtYourResult.setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtYourResult.setEditable(false);
		txtYourResult.setColumns(10);
		
		//---------------------Buttons---------------------
		JButton btnRank = new JButton("Rank List");
		btnRank.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				RankList rank = new RankList();
				rank.Run();
				dispose();
			}
		});
		btnRank.setBounds(283, 393, 130, 120);
		panel.add(btnRank);
		btnRank.setFont(new Font("Tahoma", Font.PLAIN, 20));
		btnRank.setBackground(Color.WHITE);
		
		JButton btnFinish = new JButton("Finish");
		btnFinish.setBounds(419, 393, 130, 120);
		panel.add(btnFinish);
		btnFinish.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
			}
		});
		btnFinish.setFont(new Font("Tahoma", Font.PLAIN, 20));
		btnFinish.setBackground(Color.WHITE);
		//scroll pane adjusting size
		scrollPane = new JScrollPane(panel);
		scrollPane.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		this.getContentPane().add(scrollPane, BorderLayout.CENTER);
		panel.setLayout(null);
		
		//---------------------Sets User Inputs---------------------
		double[][] results = User.results;
		int size = User.problemsInt;
		//creates expandable textfields depending on users set amount of problems
		JTextField txtNum1[] = new JTextField[size];
		JTextField txtNum2[] = new JTextField[size];
		JTextField txtResult[] = new JTextField[size];
		JTextField txtAnswer[] = new JTextField[size];
		
		//creates and adjusts panel to fit and add results
		for (int i = 0; i < results.length; i++) {	
			//adjusts bounds according to the amount of problems
			Dimension sizeDyn = new Dimension(600, (550 + (131 * i)));
			panel.setPreferredSize(sizeDyn);
			//First number repeated on amount of columns/problems
			txtNum1[i] = new JTextField();
			txtNum1[i].setBackground(Color.WHITE);
			txtNum1[i].setHorizontalAlignment(SwingConstants.CENTER);
			txtNum1[i].setForeground(Color.BLUE);
			txtNum1[i].setFont(new Font("Tahoma", Font.PLAIN, 20));
			txtNum1[i].setEditable(false);
			txtNum1[i].setColumns(10);
			txtNum1[i].setBounds(10, (251 + (131 * i)), 130, 120);
			panel.add(txtNum1[i]);
			txtNum1[i].setText(Integer.toString((int)results[i][0]));
			//Second number repeated on user input
			txtNum2[i] = new JTextField();
			txtNum2[i].setBackground(Color.WHITE);
			txtNum2[i].setHorizontalAlignment(SwingConstants.CENTER);
			txtNum2[i].setForeground(Color.BLUE);
			txtNum2[i].setFont(new Font("Tahoma", Font.PLAIN, 20));
			txtNum2[i].setEditable(false);
			txtNum2[i].setColumns(10);
			txtNum2[i].setBounds(146, (251 + (131 * i)), 130, 120);
			panel.add(txtNum2[i]);
			txtNum2[i].setText(Integer.toString((int)results[i][1]));
			//Real answer repeated
			txtResult[i] = new JTextField();
			txtResult[i].setBackground(Color.WHITE);
			txtResult[i].setHorizontalAlignment(SwingConstants.CENTER);
			txtResult[i].setForeground(Color.BLUE);
			txtResult[i].setFont(new Font("Tahoma", Font.PLAIN, 20));
			txtResult[i].setEditable(false);
			txtResult[i].setColumns(10);
			txtResult[i].setBounds(283, (251 + (131 * i)), 130, 120);
			panel.add(txtResult[i]);
			txtResult[i].setText(Double.toString(results[i][3]));
			//User answer repeated
			txtAnswer[i] = new JTextField();
			txtAnswer[i].setBackground(Color.WHITE);
			txtAnswer[i].setHorizontalAlignment(SwingConstants.CENTER);
			txtAnswer[i].setForeground(Color.BLUE);
			txtAnswer[i].setFont(new Font("Tahoma", Font.PLAIN, 20));
			txtAnswer[i].setEditable(false);
			txtAnswer[i].setColumns(10);
			txtAnswer[i].setBounds(419, (251 + (131 * i)), 130, 120);
			panel.add(txtAnswer[i]);
			txtAnswer[i].setText(Double.toString(results[i][2]));
			//adjusts button positions
			btnRank.setBounds(283, 393 + (131 * i), 130, 120);
			btnFinish.setBounds(419, 393 + (131 * i), 130, 120);
		}
	}
}
