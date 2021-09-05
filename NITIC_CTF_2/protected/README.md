# protected:Rev:200pts
パスワードでフラグを保護すれば安全！  
[protected.zip](protected.zip)  

# Solution
protected.zipを解凍するとELFが出てきた。  
パスワードがチェックされるようだ。  
```bash
$ ./chall
PASSWORD: Satoki
Invalid password.
```
stringsしてみる。  
```bash
$ strings chall
~~~
PASSWORD:
sUp3r_s3Cr37_P4s5w0Rd
Invalid password.
:*3$"
GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0
~~~
```
`sUp3r_s3Cr37_P4s5w0Rd`といういかにもなものがある。  
入力してみる。  
```bash
$ ./chall
PASSWORD: sUp3r_s3Cr37_P4s5w0Rd
nitic_ctf{hardcode_secret}
```
flagが表示された。  

## nitic_ctf{hardcode_secret}