import java.util.Scanner;
public class AscII2 {
	static int num = 0;
	
	public static void main(String[] args) {
		 Scanner sc = new Scanner(System.in);
		 String guess = sc.nextLine();
		 
		 if (guess.length()!= 12) 
			 System.out.println("Sorry, thats wrong.");
		 else {
			 System.out.println(flagTransformed(guess));
			 if(flagTransformed(guess).equals("CwViY6=]N$I")/*("I$N]=6YiVwC")*/) 
				 System.out.println("Yup the flag is flag{" + guess + "}");			 
			 else 
				 System.out.println("nope"); 
		 }
	}
	
	public static String flagTransformed(String guess) {
		char[] transformed = new char[12];
		
		for(int i = 0; i < 12; i++) {
			num = 1;
			transformed[i] = (char)(((int)guess.charAt(i) + pickNum(i + 1)) % 127);	
		}
			
		return new String(transformed);	
	}
	
	private static int pickNum(int i) {
		
		for(int x = 0; x <= i; x++)
			num+=x;
		
		if(num % 2 == 0)
			return num;
		else 
			num = pickNum(num);
		
		return num;		
	}	 
}