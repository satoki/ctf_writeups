# Recursion Reverse:Reverse Engineering:100pts
Jimmy needs some help figuring out how computers process text, help him out!  
[AscII.java](AscII.java)  

# Solution
AscII.javaは以下のようになっている。  
```java:AscII.java
import java.util.Scanner;
public class AscII {
	static int num = 0;
	
	public static void main(String[] args) {
		 Scanner sc = new Scanner(System.in);
		 System.out.print("Enter your  guess: ");
		 String guess = sc.nextLine();
		 
		 if (guess.length()!= 12) 
			 System.out.println("Sorry, thats wrong.");
		 else {
			 if(flagTransformed(guess).equals("I$N]=6YiVwC")) 
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
		
		char[] temp = new char[12];		
		for(int i = 11; i >= 0; i--) 
			temp[11-i] = transformed[i];
			
		return new String(temp);	
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
```
12文字のflagにpickNumを足して%127したものをリバースしている。  
リバースを戻して入力と照らし合わせればflagが得られる。  
AscII2.javaで行える。  
```bash
$ javac AscII2.java
$ java AscII2
A___________
CcR ou3I/
nope
$ java AscII2
As__________
CwR ou3I/
nope
$ java AscII2
AscII is key
CwViY6=]N$I
Yup the flag is flag{AscII is key}
```

## flag{AscII is key}