

import java.util.Arrays;
import java.util.Scanner;

public class InputProgram
{
	public static void main(String[] args) 
	{
		Scanner kbd = new Scanner(System.in); 
		int option1 = Arrays.asList(args).indexOf("-o");
		int option2 = Arrays.asList(args).indexOf("-t");
		boolean option3 = Arrays.asList(args).contains("-h"); 
		
		System.out.println("Standard Input: ");
		while(kbd.hasNext())  //loop
		{
			System.out.println(kbd.nextLine());
		}
		
		kbd.close(); 
		
		
		System.out.println("Command line arguments: ");
		if(option1 >= 0)
			System.out.println("option 1: " + args[option1 + 1]);
		
		if(option2 >= 0)
			System.out.println("option 2: " + args[option2 + 1]);
		
		if(option3)
			System.out.println("option 3 ");

	}
}