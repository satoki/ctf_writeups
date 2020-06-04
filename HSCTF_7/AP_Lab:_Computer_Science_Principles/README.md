# AP Lab: Computer Science Principles:Reverse Engineering:100pts
This activity will ask you to reverse a basic program and solve an introductory reversing challenge. You will be given an output that is to be used in order to reconstruct the input, which is the flag.  
[ComputerSciencePrinciples.java](ComputerSciencePrinciples.java)  

# Solution
ComputerSciencePrinciples.javaは以下のようになっている。  
```java:ComputerSciencePrinciples.java
import java.util.Scanner;
public class ComputerSciencePrinciples
{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String inp = sc.nextLine();
        if (inp.length()!=18) {
            System.out.println("Your input is incorrect.");
            System.exit(0);
        }
        inp=shift2(shift(inp));
        if (inp.equals("inagzgkpm)Wl&Tg&io")) {
            System.out.println("Correct. Your input is the flag.");
        }
        else {
            System.out.println("Your input is incorrect.");
        }
        System.out.println(inp);
    }
    public static String shift(String input) {
        String ret = "";
        for (int i = 0; i<input.length(); i++) {
            ret+=(char)(input.charAt(i)-i);
        }
        return ret;
    }
    public static String shift2(String input) {
        String ret = "";
        for (int i = 0; i<input.length(); i++) {
            ret+=(char)(input.charAt(i)+Integer.toString((int)input.charAt(i)).length());
        }
        return ret;
    }
}
```
どうやら入力をshiftした後、shift2しているので逆を行えばよい。  
shiftでは引いて、shift2では足しているようなので書き換える。  
ComputerSciencePrinciples2.javaにその動作を記述し実行する。  
```bash
$ javac ComputerSciencePrinciples2.java
$ java ComputerSciencePrinciples2
flag{intr0_t0_r3v}
$ javac ComputerSciencePrinciples.java
$ java ComputerSciencePrinciples
flag{intr0_t0_r3v}
Correct. Your input is the flag.
inagzgkpm)Wl&Tg&io
```

## flag{intr0_t0_r3v}