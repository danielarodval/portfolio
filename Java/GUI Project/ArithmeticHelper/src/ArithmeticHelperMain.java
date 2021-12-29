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
import javax.swing.SwingConstants;
import java.awt.Font;
import javax.swing.JTextField;
import javax.swing.JComboBox;
import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.util.Random;
import java.awt.Color;

public class ArithmeticHelperMain extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JTextField txtName;
	private JTextField txtProblems;
	private JTextField txtNumber;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					ArithmeticHelperMain frame = new ArithmeticHelperMain();
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
	public static String nickName = new String();
	public static String problems = new String();
	public static String digits = new String();
	public static String operand = new String();
	
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public ArithmeticHelperMain() {
		setTitle("Arithmetic Helper");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 450, 350);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		//---------------------Labels---------------------
		JLabel lblTitle = new JLabel("Welcome");
		lblTitle.setBounds(110, 11, 201, 40);
		lblTitle.setHorizontalAlignment(SwingConstants.CENTER);
		lblTitle.setFont(new Font("Tahoma", Font.PLAIN, 30));
		contentPane.add(lblTitle);
		
		JLabel lblSubTitle = new JLabel("Arithmetic Helper");
		lblSubTitle.setBounds(68, 47, 276, 40);
		lblSubTitle.setFont(new Font("Tahoma", Font.PLAIN, 30));
		lblSubTitle.setHorizontalAlignment(SwingConstants.CENTER);
		contentPane.add(lblSubTitle);
		
		JLabel lblName = new JLabel("Please Enter Your Nickname: ");
		lblName.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblName.setBounds(35, 91, 221, 40);
		contentPane.add(lblName);
		
		JLabel lblProblem = new JLabel("Please Enter Number of Problems:");
		lblProblem.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblProblem.setBounds(35, 128, 265, 40);
		contentPane.add(lblProblem);
		
		JLabel lblNumber = new JLabel("Please Enter Number of Digits:");
		lblNumber.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNumber.setBounds(35, 166, 239, 40);
		contentPane.add(lblNumber);
		
		JLabel lblType = new JLabel("Choose the Type of Operation:");
		lblType.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblType.setBounds(35, 201, 239, 40);
		contentPane.add(lblType);
		//---------------------TextFields---------------------
		txtName = new JTextField();
		txtName.setFont(new Font("Tahoma", Font.PLAIN, 15));
		txtName.setForeground(Color.BLUE);
		txtName.setBounds(234, 103, 96, 20);
		contentPane.add(txtName);
		txtName.setColumns(10);
		
		txtProblems = new JTextField();
		txtProblems.setFont(new Font("Tahoma", Font.PLAIN, 15));
		txtProblems.setForeground(Color.BLUE);
		txtProblems.setBounds(268, 140, 96, 20);
		contentPane.add(txtProblems);
		txtProblems.setColumns(10);
		
		txtNumber = new JTextField();
		txtNumber.setFont(new Font("Tahoma", Font.PLAIN, 15));
		txtNumber.setForeground(Color.BLUE);
		txtNumber.setBounds(245, 178, 96, 20);
		contentPane.add(txtNumber);
		txtNumber.setColumns(10);
		//---------------------ComboBox---------------------
		JComboBox comboBox = new JComboBox();
		comboBox.setFont(new Font("Tahoma", Font.PLAIN, 15));
		comboBox.setForeground(Color.BLUE);
		comboBox.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String tempOperand = (String) comboBox.getSelectedItem();
				//sets operand which is passed through classes, as well as generates random if selected
				if(tempOperand.contains("Select")) {
					operand = null;
				}else if(tempOperand.contains("+")) {
					operand = "+";
				}else if(tempOperand.contains("-")) {
					operand = "-";
				}else if(tempOperand.contains("*")) {
					operand = "*";
				}else if(tempOperand.contains("/")) {
					operand = "/";
				}else if(tempOperand == "Random") {
					Random rand = new Random();
					int n = rand.nextInt(4);
					if (n == 0) {
						operand = "+";
					}else if (n == 1) {
						operand = "-";
					}else if (n == 2) {
						operand = "*";
					}else if (n == 3) {
						operand = "/";
					}
				}
				//checks if an operand is selected
				if(tempOperand.contains("Select")) {
					
				}else {
					//checks if user has input numbers into boxes
					if (isNumeric(txtProblems.getText()) == true && isNumeric(txtNumber.getText()) == true) {
						nickName = txtName.getText();
						problems = txtProblems.getText();
						digits = txtNumber.getText();
						User use = new User();
						use.store();
						Start start = new Start();
						start.Run();
						dispose();
					} else {
						JOptionPane.showMessageDialog(null, "Please enter a valid number!");
					}
				}
			}
		});
		comboBox.setModel(new DefaultComboBoxModel(new String[] {"--Select--", "Addition [+]", "Subtraction [-]", "Multiplication [*]", "Division [/]", "Random"}));
		comboBox.setBounds(245, 212, 135, 22);
		contentPane.add(comboBox);
		//---------------------Buttons---------------------
		JButton btnClose = new JButton("Close");
		btnClose.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null, "Thank you for using Arithmetic Helper");
				System.exit(0);
			}
		});
		btnClose.setBounds(80, 252, 89, 44);
		contentPane.add(btnClose);
		
		JButton btnProject = new JButton("Behind This Project");
		btnProject.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null, "Alright so here's the situation, I wrote, I hate it, "
						+ "but I loved it, this took me forever to do. \nNot exaggerating. Straightup took me "
						+ "like 24 hours straight, I started like a week ago. \nSomewhere in this program I wrote "
						+ "about how I reached a 12 hour mark and wanted to cry. \nBut I'm here now, finalizing "
						+ "my behind the project. Please give me an A, I troubleshooted \nthe heck out of this "
						+ "and using my roommates as test dummies. Give 30/30 oh also my \nname is Daniel"
						+ " Rodriguez and yeah I don't know if I labeled everything.");
			}
		});
		btnProject.setBounds(196, 252, 149, 44);
		contentPane.add(btnProject);
	}
	//---------------------Getters && Setters to Pass to Other Classes---------------------
	public void setNickName(String nickName) {
		ArithmeticHelperMain.nickName = nickName;
	}
	
	public static String getNickName() {
		return nickName;
	}
	
	public void setProblems(String problems) {
		ArithmeticHelperMain.problems = problems;
	}
	
	public static String getProblems() {
		return problems;
	}
	
	public void setDigits(String digits) {
		ArithmeticHelperMain.digits = digits;
	}
	
	public static String getDigits() {
		return digits;
	}
	
	public void setOperand(String operand) {
		ArithmeticHelperMain.operand = operand;
	}
	
	public static String getOperand() {
		return operand;	
	}
	//---------------------Checks String for Numbers---------------------
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
