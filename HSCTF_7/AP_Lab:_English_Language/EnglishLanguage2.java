public class EnglishLanguage2
{
    public static void main(String[] args) {
        String inp = "1dd3|y_3tttb5g`q]^dhn3j";
        if (inp.length()!=23) {
            System.out.println("Your input is incorrect.");
            System.exit(0);
        }
        for (int i = 0; i<3; i++) {
            inp=xor(inp);
            inp=transpose(inp);
        }
        if (inp.equals("1dd3|y_3tttb5g`q]^dhn3j")) {
            System.out.println("Correct. Your input is the flag.");
        }
        else {
            System.out.println(inp);
        }

    }
    public static String transpose(String input) {
        int[] transpose = {11,18,15,19,8,17,5,2,12,6,21,0,22,7,13,14,4,16,20,1,3,10,9};
        char[] chrs = new char[23];
        int j = 0;
        for (int i: transpose) {
            chrs[i] = input.charAt(j);
            j++;
        }//wow
        String ret = String.valueOf(chrs);
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
