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
import java.awt.Color;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.awt.event.ActionEvent;

import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;

public class RankList extends JFrame {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JButton btnNewButton;
	/**
	 * Launch the application.
	 */
	public void Run() {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					RankList frame = new RankList();
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
	public RankList() {
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 600, 570);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblrankList = new JLabel("~~RANK LIST OF ARITHMETIC HELPER~~");
		lblrankList.setForeground(Color.RED);
		lblrankList.setFont(new Font("Tahoma", Font.BOLD | Font.ITALIC, 25));
		lblrankList.setBounds(20, 11, 541, 31);
		contentPane.add(lblrankList);
		//---------------------Strings---------------------
		String[] place = new String[10];
		for(int i = 0; i < 10; i++) {
			int temp = i+1;
			place[i] = "\t" + Integer.toString(temp) + ". ";
		}
		//---------------------TextFields---------------------
		JTextField txtPlay[] = new JTextField[11];
		txtPlay[1] = new JTextField();
		txtPlay[1].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[1].setForeground(Color.BLUE);
		txtPlay[1].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[1].setEditable(false);
		txtPlay[1].setColumns(10);
		txtPlay[1].setBackground(Color.WHITE);
		txtPlay[1].setBounds(20, 67, 500, 30);
		contentPane.add(txtPlay[1]);
		
		txtPlay[2] = new JTextField();
		txtPlay[2].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[2].setForeground(Color.BLUE);
		txtPlay[2].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[2].setEditable(false);
		txtPlay[2].setColumns(10);
		txtPlay[2].setBackground(Color.WHITE);
		txtPlay[2].setBounds(20, 106, 500, 30);
		contentPane.add(txtPlay[2]);
		
		txtPlay[3] = new JTextField();
		txtPlay[3].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[3].setForeground(Color.BLUE);
		txtPlay[3].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[3].setEditable(false);
		txtPlay[3].setColumns(10);
		txtPlay[3].setBackground(Color.WHITE);
		txtPlay[3].setBounds(20, 147, 500, 30);
		contentPane.add(txtPlay[3]);
		
		txtPlay[4] = new JTextField();
		txtPlay[4].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[4].setForeground(Color.BLUE);
		txtPlay[4].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[4].setEditable(false);
		txtPlay[4].setColumns(10);
		txtPlay[4].setBackground(Color.WHITE);
		txtPlay[4].setBounds(20, 188, 500, 30);
		contentPane.add(txtPlay[4]);
		
		txtPlay[5] = new JTextField();
		txtPlay[5].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[5].setForeground(Color.BLUE);
		txtPlay[5].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[5].setEditable(false);
		txtPlay[5].setColumns(10);
		txtPlay[5].setBackground(Color.WHITE);
		txtPlay[5].setBounds(20, 229, 500, 30);
		contentPane.add(txtPlay[5]);
		
		txtPlay[6] = new JTextField();
		txtPlay[6].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[6].setForeground(Color.BLUE);
		txtPlay[6].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[6].setEditable(false);
		txtPlay[6].setColumns(10);
		txtPlay[6].setBackground(Color.WHITE);
		txtPlay[6].setBounds(20, 268, 500, 30);
		contentPane.add(txtPlay[6]);
		
		txtPlay[7] = new JTextField();
		txtPlay[7].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[7].setForeground(Color.BLUE);
		txtPlay[7].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[7].setEditable(false);
		txtPlay[7].setColumns(10);
		txtPlay[7].setBackground(Color.WHITE);
		txtPlay[7].setBounds(20, 309, 500, 30);
		contentPane.add(txtPlay[7]);
		
		txtPlay[8] = new JTextField();
		txtPlay[8].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[8].setForeground(Color.BLUE);
		txtPlay[8].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[8].setEditable(false);
		txtPlay[8].setColumns(10);
		txtPlay[8].setBackground(Color.WHITE);
		txtPlay[8].setBounds(20, 350, 500, 30);
		contentPane.add(txtPlay[8]);
		
		txtPlay[9] = new JTextField();
		txtPlay[9].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[9].setForeground(Color.BLUE);
		txtPlay[9].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[9].setEditable(false);
		txtPlay[9].setColumns(10);
		txtPlay[9].setBackground(Color.WHITE);
		txtPlay[9].setBounds(20, 391, 500, 30);
		contentPane.add(txtPlay[9]);
		
		txtPlay[10] = new JTextField();
		txtPlay[10].setHorizontalAlignment(SwingConstants.LEFT);
		txtPlay[10].setForeground(Color.BLUE);
		txtPlay[10].setFont(new Font("Tahoma", Font.PLAIN, 20));
		txtPlay[10].setEditable(false);
		txtPlay[10].setColumns(10);
		txtPlay[10].setBackground(Color.WHITE);
		txtPlay[10].setBounds(20, 432, 500, 30);
		contentPane.add(txtPlay[10]);
		//---------------------Buttons---------------------
		btnNewButton = new JButton("MainWindow");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				//returns to main, and disposes of ranklist
				User use = new User();
				use.clear();
				ArithmeticHelperMain.main(null);
				dispose();
			}
		});
		btnNewButton.setFont(new Font("Tahoma", Font.PLAIN, 15));
		btnNewButton.setBounds(369, 481, 120, 30);
		contentPane.add(btnNewButton);
		
		JLabel lblName = new JLabel("Name");
		lblName.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblName.setBounds(156, 46, 49, 20);
		contentPane.add(lblName);
		
		JLabel lblScore = new JLabel("Score");
		lblScore.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblScore.setBounds(285, 46, 49, 20);
		contentPane.add(lblScore);
		//---------------------File Operations---------------------
		try {
			//picks directory
			String fName = "Records";
			File file = new File(fName);
			
			//starts file reader
			FileReader fr = new FileReader(file.getAbsoluteFile());
			BufferedReader br = new BufferedReader(fr);
			
			//declares variables to be used
			String line;
			int i = 0;
			//while to read first 10 and display them
			while ((line = br.readLine()) != null) {
				if (i < 10) {
					String temp = place[i];
					place[i] = temp + line;
					i++;
					//txtPlay[i].setText(place[i]);	
				}
			}
			for(int j = 0; j < 10; j++) {
				txtPlay[j+1].setText(place[j]);	
			}
			br.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
