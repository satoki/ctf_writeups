# Look in the shadow:Steganography:300pts
We received a suspicious png file!  
Can you find a hidden message?  
![shadow.jpg](images/shadow.jpg)  
Nous avons reçu un fichier png suspect!  
Pouvez-vous trouver un message caché?  
ZIP PASSWORD: 0FPP7C7F  
Hint  
You need steg tools to extract data.  
Hint  
Use steghide if you don't know which tool to use!  
[LookInTheShadows.zip](LookInTheShadows.zip)  

# Solution
指定されたパスワードでzipを解凍すると以下の画像が得られた。  
![LookInTheShadows.jpg](LookInTheShadows.jpg)  
メッセージが隠されているらしいが、よく使われるのは`steghide`だ。  
```bash
$ steghide extract -sf LookInTheShadows.jpg
Enter passphrase:
wrote extracted data to "secret.txt".
$ cat secret.txt
OFPPT-CTF{3mb3dd3d_H1dd3n_73x7_d4t4}
```
secret.txtが埋め込まれていて、中にflagが書かれていた。  

## OFPPT-CTF{3mb3dd3d_H1dd3n_73x7_d4t4}