/* University of Central Florida
* COP 3330 Spring 2019
* Final Project
* Author: <Daniel Rodriguez>
* PID: 4802087
*/ 
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
//used for passing variables with ease, as well as works with file
public class User {
	//gets all the inputs from the classes and stores them to be called for easier access
	public static String nickName = ArithmeticHelperMain.getNickName();
	public static String problemsText = ArithmeticHelperMain.getProblems();
	public static String digitsText = ArithmeticHelperMain.getDigits();
	public static String operand = ArithmeticHelperMain.getOperand();
	public static int problemsInt = Integer.parseInt(problemsText);
	public static int digitsInt = Integer.parseInt(digitsText);
	public static double problemsDoub = Double.parseDouble(problemsText);
	public static double[][] results = Problems.getResults();
	
	public void store() {
		nickName = ArithmeticHelperMain.getNickName();
		problemsText = ArithmeticHelperMain.getProblems();
		digitsText = ArithmeticHelperMain.getDigits();
		operand = ArithmeticHelperMain.getOperand();
		results = Problems.getResults();
	}
	
	public void clear() {
		nickName = null;
		problemsText = null;
		digitsText = null;
		operand = null;
		results = null;
	}
	
	//file writer implemented early to save data even if the user doesnt check
	public void fileWriter() {
		try {
			//picks directory
			String fName = "Records";
			File file = new File(fName);
			//checks if file exists to make it
			if (!file.exists()) {
				file.createNewFile();
			}
			//writer used to save name and score
			FileWriter fw = new FileWriter(file.getAbsoluteFile(), true);
			BufferedWriter bw = new BufferedWriter(fw, 1);
			String toFile = User.nickName + "\t" + Result.getScore() + "\n";
			//writes to the file	
			bw.write(toFile);
			bw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	//file sorter to be implemented after user data has been saved
	public void fileSorter() {
		try {
			//creates/finds file 
        	String fname = "Records"; 
        	File f = new File(fname); 
        	
        	if (!f.exists()) {
                f.createNewFile();
             }  
	    	//reads file and outputs
	    	FileReader fr = new FileReader(f.getAbsoluteFile());
	    	BufferedReader br = new BufferedReader(fr);
	    	//creates arraylist to hold player objects
	    	ArrayList<Player> playerScores = new ArrayList<Player>();
	    	//starts to read lines
	    	String line = br.readLine();
			//while to read the file and store scores in array
			while (line != null) {
				String[] playerDetail = line.split("\t");
				String name = playerDetail[0];
				double score = Double.valueOf(playerDetail[1]);
				//creating object for every player record and adds to arraylist
				playerScores.add(new Player(name, (int) score));	
				line = br.readLine();
			}
			br.close();
			//Sorting Arrays of playerscores based on score
			Collections.sort(playerScores, new scoreCompare());	
 			//creating buffered writer to write the newly formatted text
			FileWriter fw = new FileWriter(f.getAbsoluteFile());
       	 	BufferedWriter bw = new BufferedWriter(fw);
 			//writing all the player records 
 			for(Player player : playerScores) {
 				bw.write(player.name);
 				bw.write("\t" + player.score);
 				bw.newLine();
 			}
 			//close the stuff
 			bw.close();		
 			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	//player class
		class Player {
			String name;
			int score;
			
			public Player(String name, int score) {
				this.name = name;
				this.score = score;
			}
		}
		
		//Class to compare scores
		class scoreCompare implements Comparator<Player> {
			public int compare(Player s1, Player s2) {
				return s2.score - s1.score;
			}
		}
}
