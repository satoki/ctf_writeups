# AP Lab: English Language:Reverse Engineering:100pts
The AP English Language activity will ask you to reverse a program about manipulating strings and arrays. Again, an output will be given where you have to reconstruct an input.  
[EnglishLanguage.java](EnglishLanguage.java)  

# Solution
EnglishLanguage.javaは以下のようになっている。  
```java:EnglishLanguage.java
import java.util.Scanner;
public class EnglishLanguage
{
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String inp = sc.nextLine();
        if (inp.length()!=23) {
            System.out.println("Your input is incorrect.");
            System.exit(0);
        }
        for (int i = 0; i<3; i++) {
            inp=transpose(inp);
            inp=xor(inp);
        }
        if (inp.equals("1dd3|y_3tttb5g`q]^dhn3j")) {
            System.out.println("Correct. Your input is the flag.");
        }
        else {
            System.out.println("Your input is incorrect.");
        }
    }
    public static String transpose(String input) {
        int[] transpose = {11,18,15,19,8,17,5,2,12,6,21,0,22,7,13,14,4,16,20,1,3,10,9};
        String ret = "";
        for (int i: transpose) {
            ret+=input.charAt(i);
        }
        return ret;
    }
    public static String xor(String input) {
        int[] xor = {4,1,3,1,2,1,3,0,1,4,3,1,2,0,1,4,1,2,3,2,1,0,3};
        String ret = "";
        for (int i = 0; i<input.length(); i++) {
            ret+=(char)(input.charAt(i)^xor[i]) ;
        }
        return ret;
    }
}
```

どうやら入力をtransposeした後、xorしているので逆を行えばよい。  
transposeでは入力を指定した順序に入れ替えているので復元し、xorはもう一度xorすることにより元に戻る性質を使う。  
EnglishLanguage2.javaにその動作を記述し実行する。  
```bash
$ javac EnglishLanguage2.java
$ java EnglishLanguage2
flag{n0t_t00_b4d_r1ght}
$ javac EnglishLanguage.java
$ java EnglishLanguage
flag{n0t_t00_b4d_r1ght}
Correct. Your input is the flag.
```

## flag{n0t_t00_b4d_r1ght}