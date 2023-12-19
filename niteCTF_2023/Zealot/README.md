# Zealot:rev:50pts
Follow the commandments and you shall be worthy enough to lift the sword of Zealot  
`nc 34.93.183.186 1337`  

[zealot.zip](zealot.zip)  

# Solution
接続先とバイナリが渡される。  
IDAで見るとよくあるパスワードチェックのようだ。  
![ida.png](images/ida.png)  
angrで簡単に解けそうなので、以下のようにsolve.pyを実行する。  
```python
import angr
import logging

logging.getLogger("angr").setLevel("CRITICAL")
angr.manager.l.setLevel("CRITICAL")
proj = angr.Project("Zealot")
simgr = proj.factory.simgr()
simgr.explore(
    find=lambda s: b"Entered Here" in s.posix.dumps(1),
    avoid=lambda s: b"Leave At Once" in s.posix.dumps(1)
)

if len(simgr.found) > 0:
    print(simgr.found[0].posix.dumps(0))
    exit(0)
else:
    print("Not Found")
```
実行する。  
```bash
$ python solve.py
b'niteCTF{good_for_health_bad_for_ed\x00cation}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```
フラグのようなものが出たが、形式が異なる。  
ローカルで入力を試す。  
```bash
$ echo -e "niteCTF{good_for_health_bad_for_ed\x00cation}" | ./Zealot
ZZZZZZZZZZZ       EEEEEEEEEEEE      AAAAA       LL               OOOOOOOOO      TTTTTTTTTTTT
      ZZ          EE               A     A      LL             OO         OO         TT
    ZZ            EEEEEE          AAAAAAAAA     LL             OO         OO         TT
 ZZ               EE              A       A     LL             OO         OO         TT
ZZZZZZZZZZZ       EEEEEEEEEEEE    A       A     LLLLLLLLLL       OOOOOOOO            TT

Speak Heretic!!
Password entered is niteCTF{good_for_health_bad_for_ed
Entered Here
You Heretics Sure Do Get On My Nerve
nite{FAKE_FAKE_FAKEFLAG}
```
意図的であるかは不明だが、NULLバイトが含まれていることにも注意が必要であった。  
リモートへ送信する。  
```bash
$ echo -e "niteCTF{good_for_health_bad_for_ed\x00cation}" | nc 34.93.183.186 1337
ZZZZZZZZZZZ       EEEEEEEEEEEE      AAAAA       LL               OOOOOOOOO      TTTTTTTTTTTT
      ZZ          EE               A     A      LL             OO         OO         TT
    ZZ            EEEEEE          AAAAAAAAA     LL             OO         OO         TT
 ZZ               EE              A       A     LL             OO         OO         TT
ZZZZZZZZZZZ       EEEEEEEEEEEE    A       A     LLLLLLLLLL       OOOOOOOO            TT

Speak Heretic!!
Password entered is niteCTF{good_for_health_bad_for_ed
Entered Here
You Heretics Sure Do Get On My Nerve
nite{Teri_yaki_maaki_chu_chicken}
```
flagが得られた。  

## nite{Teri_yaki_maaki_chu_chicken}