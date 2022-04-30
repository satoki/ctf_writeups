# Prisoner:Warmups:50pts
Have you ever broken out of jail? Maybe it is easier than you think!  

**Connect with:**  
```
# Password is "userpass"
ssh -p 32174 user@challenge.nahamcon.com
```

# Solution
sshでの接続先のみが渡されるため指定された通り接続する。  
```bash
$ ssh -p 32174 user@challenge.nahamcon.com
user@challenge.nahamcon.com's password:

  _________________________
     ||   ||     ||   ||
     ||   ||, , ,||   ||
     ||  (||/|/(\||/  ||
     ||  ||| _'_`|||  ||
     ||   || o o ||   ||
     ||  (||  - `||)  ||
     ||   ||  =  ||   ||
     ||   ||\___/||   ||
     ||___||) , (||___||
    /||---||-\_/-||---||\
   / ||--_||_____||_--|| \
  (_(||)-| SP1337 |-(||)_)
          --------

Hello prisoner, welcome to jail.
Don't get any ideas, there is no easy way out!
: ls
: pwd
:
```
jailが組まれており、何のコマンドも実行できない。  
`exit`で終了もできず、Ctrl+Cでの強制終了もできない。  
ここで、ひとまず入力を終わらせたいため、EOFをCtrl+Dで入力してみる。  
```bash
: ls
: pwd
: Traceback (most recent call last):
  File "/home/user/jail.py", line 27, in <module>
    input(": ")
EOFError
>>>
```
pythonのエラーが発生したようだ。  
これでpythonが実行できるようになったため、osコマンドを実行する。  
```bash
>>> import os
>>> os.system("ls")
flag.txt  jail.py
0
>>> os.system("cat flag.txt")
flag{c31e05a24493a202fad0d1a827103642}
0
```
flagが得られた。  

## flag{c31e05a24493a202fad0d1a827103642}