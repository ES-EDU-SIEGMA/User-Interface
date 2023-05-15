
import java.io.*; 

public class Terminal{
	
	public void readDrinkNumber()   {
		int number;
		String input = null;
		
		System.out.println("1: Spezi");
		System.out.println("2: Super-Spezi");
		System.out.println("3: H2O");
	
		BufferedReader keyboard = null;
		keyboard = new BufferedReader(new InputStreamReader(System.in));
		
		
		
		try {
			input = keyboard.readLine();
		} catch (IOException e) {
			e.printStackTrace();
		}		


		number = Integer.parseInt(input);
		
		System.out.println("Auswahl ist " + number);
	}
}
