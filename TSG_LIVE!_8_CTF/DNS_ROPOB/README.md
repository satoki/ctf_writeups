# DNS ROPOB:rev:400pts
ランダム化される前でよかった。  
**注意!** この問題のFlagのフォーマットは`TSGCTF{hogehoge}` です  
[dns_ropob](dns_ropob)  

# Solution
Revは専門外なのでひとまずstringsにかけてみる。  
```bash
$ strings dns_ropob
~~~
FLAG >
%32s
correct!
wrong!
;*3$"
7(&h
GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0
crtstuff.c
~~~
```
`correct!`なる文字が見えるため、入力の検証を行っていそうだ。  
angrにおいてテキストでゴールを指定する方法があったはずである。  
「CTF angr correct」などでググると[SECCON Beginners CTF 2021 作問者Writeup](https://feneshi.co/ctf4b2021writeup/#be_angry)へのリンク出てくる(俺も作問側じゃん…)。  
このスクリプトをキディする。  
```python
#!/usr/bin/env python3
import angr
import logging

logging.getLogger("angr").setLevel("CRITICAL")
angr.manager.l.setLevel("CRITICAL")
proj = angr.Project("./dns_ropob")

simgr = proj.factory.simgr()
simgr.explore(find=lambda s: b"correct!" in s.posix.dumps(1))
if len(simgr.found) > 0:
    found = simgr.found[0].posix.dumps(0).decode("utf-8", "ignore")
    print(found)

# ref. https://feneshi.co/ctf4b2021writeup/#be_angry
```
実行する。  
```bash
$ python torisan.py
WARNING | 2022-05-14 00:00:00,000 | cle.loader | The main binary is a position-independent executable. It is being loaded with a base address of 0x400000.
TSGCTF{I_am_inspired_from_ROPOB}
```
flagが得られた。  

## TSGCTF{I_am_inspired_from_ROPOB}