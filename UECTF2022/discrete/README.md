# discrete:REV:400pts
Jumping around in memory  
記憶の中でジャンプする  

[chall](chall)  

# Solution
実行ファイルが配布される。  
```bash
$ ./chall
flag: satoki
invalid input length
$ strings chall
~~~
flag:
invalid input length
Wrong!
Correct!
~~~
```
よくわからないがフラグを入力に取るようであり、`Wrong!`や`Correct!`が見える。  
angrに食わせればよさそうだ。  
以下のsolver.pyで行う(スクリプトは[ここ](https://feneshi.co/TSG_LIVE_8_CTF_writeup)からパク…借りた)。  
```python
import angr
import logging

logging.getLogger("angr").setLevel("CRITICAL")
angr.manager.l.setLevel("CRITICAL")
proj = angr.Project("chall")

simgr = proj.factory.simgr()
simgr.explore(find=lambda s: b"Correct!" in s.posix.dumps(1), avoid=lambda s: b"Wrong!" in s.posix.dumps(1))
if len(simgr.found) > 0:
    print(simgr.found[0].posix.dumps(0).decode("utf-8", "ignore"))
    exit(0)
else:
    print('not found')
```
実行する。  
```bash
$ python solver.py
WARNING | 2022-11-20 00:00:00,000 | cle.loader | The main binary is a position-independent executable. It is being loaded with a base address of 0x400000.
UECTF{dynamic_static_strings_2022}
```
flagが得られた。  

## UECTF{dynamic_static_strings_2022}