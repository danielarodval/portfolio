/* University of Central Florida
* COP 3330 Spring 2019
* Final Project
* Author: <Daniel Rodriguez>
* PID: 4802087
*/ 
import java.awt.EventQueue;
import java.awt.Font;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import javax.swing.border.EmptyBorder;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Color;

public class Start extends JFrame {

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
					Start frame = new Start();
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
	public Start() {
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		setBounds(100, 100, 700, 250);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		//---------------------Main Panel with User's Inputs---------------------
		JLabel lblTitle = new JLabel("***Helper***");
		lblTitle.setForeground(Color.BLUE);
		lblTitle.setHorizontalAlignment(SwingConstants.CENTER);
		lblTitle.setFont(new Font("Tahoma", Font.PLAIN, 30));
		lblTitle.setBounds(10, 0, 666, 55);
		contentPane.add(lblTitle);
		
		JLabel label = new JLabel("Your Name: "
				+ User.nickName);
		label.setForeground(Color.BLUE);
		label.setFont(new Font("Tahoma", Font.PLAIN, 15));
		label.setBounds(182, 66, 312, 20);
		contentPane.add(label);
		
		JLabel label_1 = new JLabel("Your Number of Problems: "
				+ User.problemsText);
		label_1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		label_1.setBounds(182, 90, 254, 20);
		contentPane.add(label_1);
		
		JLabel label_2 = new JLabel("Your Number of Digits: "
				+ User.digitsText);
		label_2.setFont(new Font("Tahoma", Font.PLAIN, 15));
		label_2.setBounds(182, 116, 283, 20);
		contentPane.add(label_2);
		//---------------------Button---------------------
		JLabel label_3 = new JLabel("Press Start to Start the Quiz");
		label_3.setFont(new Font("Tahoma", Font.PLAIN, 15));
		label_3.setBounds(206, 157, 189, 20);
		contentPane.add(label_3);
		
		JButton button = new JButton("Start");
		button.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Problems prob = new Problems();
				//calls run of problems and inputs the first out of # input
				prob.Run(1);
				dispose();
			}
		});
		button.setFont(new Font("Tahoma", Font.PLAIN, 15));
		button.setBounds(405, 158, 89, 23);
		contentPane.add(button);
		//---------------------Sets Titles According to User Inputs---------------------
		String operand = User.operand;
		if(operand == "+") {
			lblTitle.setText("***Addition Helper***");
			setTitle("Addition Helper");
		}else if (operand == "-") {
			lblTitle.setText("***Subtraction Helper***");
			setTitle("Subtraction Helper");
		}else if (operand == "*") {
			lblTitle.setText("***Multiplication Helper***");
			setTitle("Multiplication Helper");
		}else if (operand == "/") {
			lblTitle.setText("***Division Helper***");
			setTitle("Division Helper");
		}
	}
}
