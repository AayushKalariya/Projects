package a;
import java.util.Scanner;


public class Game {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		Scanner input  = new Scanner(System.in);
		System.out.println("Please Enter a Word for the other player to Guess(All lowercase);");
		String x = input.nextLine();
		for(int i =   0; i < 10; i++) {
			System.out.println();
		}
		GameTester p = new GameTester(x);
		String w = null;
		while(!(x.equals(w))) {
			System.out.println("Enter a guess:");
			 w = input.nextLine();
			 System.out.println(p.Guesser(w));
			 if (p.Guesser(w).equals(x)) {
				 System.out.println("Great job you guess the word!");
				 
			 }
		}
		
		
		
	}
	}


