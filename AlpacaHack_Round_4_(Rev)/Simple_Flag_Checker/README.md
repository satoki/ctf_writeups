# Simple Flag Checker:Rev:146pts
A simple flag checker :)  

[checker](checker)  

# Solution
謎のバイナリが渡される。  
実行すると、問題名の通りフラグチェッカーのようだ。  
```bash
$ ./checker
flag? Satoki
Wrong...
```
IDAでデコンパイルすると`main`は以下であった。  
```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rbx
  int v4; // r12d
  int result; // eax
  __int64 v6[4]; // [rsp+0h] [rbp-98h] BYREF
  int v7; // [rsp+20h] [rbp-78h]
  char s[56]; // [rsp+30h] [rbp-68h] BYREF
  unsigned __int64 v9; // [rsp+68h] [rbp-30h]

  v9 = __readfsqword(0x28u);
  __printf_chk(1LL, "flag? ", envp);
  fgets(s, 50, _bss_start);
  memset(v6, 0, sizeof(v6));
  v7 = 0;
  v3 = 0LL;
  LOBYTE(v4) = 1;
  do
  {
    update(v6, (unsigned __int8)s[v3]);
    v4 = (memcmp(v6, (char *)&table + 16 * v3++, 0x10uLL) == 0) & (unsigned __int8)v4;
  }
  while ( v3 != 49 );
  if ( v4 )
  {
    __printf_chk(1LL, "Correct! Your flag is: %s\n", s);
    result = 0;
  }
  else
  {
    puts("Wrong...");
    result = 1;
  }
  if ( v9 != __readfsqword(0x28u) )
    return term_proc();
  return result;
}
```
フラグは49文字で、正解であれば`Correct! Your flag is: %s\n`が出力されるようだ。  
以下のように文字数分ループしている個所に注目する。  
```c
  do
  {
    update(v6, (unsigned __int8)s[v3]);
    v4 = (memcmp(v6, (char *)&table + 16 * v3++, 0x10uLL) == 0) & (unsigned __int8)v4;
  }
  while ( v3 != 49 );
```
`update`に一文字ずつ渡しているようで、あらかじめ`memset`した領域に何らかの更新処理を行っている。  
その後に`memcmp`で比較処理を行い、結果をフラグの正誤判定に利用する変数にANDしている。  
つまり一文字でも間違えると、この変数が偽になり不正解と判定される。  
`update`はとてつもなく複雑な処理をしているので読みたくない。  
`memcmp`にブレークポイントを設置し挙動を見る。  
```bash
$ gdb ./checker
~~~
pwndbg> start
~~~
pwndbg> disass main
Dump of assembler code for function main:
=> 0x0000555555555980 <+0>:     endbr64
~~~
   0x0000555555555a27 <+167>:   mov    rdi,rbp
   0x0000555555555a2a <+170>:   call   0x5555555550b0 <memcmp@plt>
   0x0000555555555a2f <+175>:   test   eax,eax
~~~
pwndbg> b *0x0000555555555a2a
Breakpoint 2 at 0x555555555a2a
pwndbg> c
Continuing.
flag? xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

~~~
──────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────────────────────────
 ► 0x555555555a2a <main+170>    call   memcmp@plt                  <memcmp@plt>
        s1: 0x7fffffffdb90 ◂— 0x77aefc95befb0983
        s2: 0x555555558020 (table) ◂— 0xac050fa321f13c42
        n: 0x10

   0x555555555a2f <main+175>    test   eax, eax
   0x555555555a31 <main+177>    sete   al
   0x555555555a34 <main+180>    movzx  eax, al
   0x555555555a37 <main+183>    and    r12d, eax
   0x555555555a3a <main+186>    add    rbx, 1
   0x555555555a3e <main+190>    cmp    rbx, 0x31
   0x555555555a42 <main+194>    jne    main+136                    <main+136>

   0x555555555a44 <main+196>    test   r12d, r12d
   0x555555555a47 <main+199>    je     main+260                    <main+260>

   0x555555555a49 <main+201>    lea    rdx, [rsp + 0x30]
~~~
```
`s1`と`s2`が異なっていることがわかる。  
このことから、一文字目の判定が失敗していることがわかる。  
次に、入力フラグの先頭を`A`にし、判定を成功させてみる。  
```bash
pwndbg> c
Continuing.
flag? Axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

~~~
──────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────────────────────────
 ► 0x555555555a2a <main+170>    call   memcmp@plt                  <memcmp@plt>
        s1: 0x7fffffffdb90 ◂— 0xac050fa321f13c42
        s2: 0x555555558020 (table) ◂— 0xac050fa321f13c42
        n: 0x10

```
`s1`と`s2`が一致していることがわかる。  
これは二文字目を`l`、三文字目を`p`にした場合でも同様であった。  
こうして先頭からフラグを導出できる。  
以下のplzflag.pyようにpwndbg導入済みgdbを直で実行し、ptrlibで自動化してやる。  
```python
import re
import string
from ptrlib import *

logger.level = 0

flag = ["x"] * 49

for i in range(49):
    for c in string.printable:
        sock = Process("gdb ./checker")
        sock.sendlineafter("pwndbg> ", "start")
        sock.sendlineafter("pwndbg> ", "b *0x0000555555555a2a")
        sock.sendlineafter("pwndbg> ", "c")
        flag[i] = c
        sock.sendline("".join(flag))
        for j in range(i):
            sock.sendlineafter("pwndbg> ", "c")
        sock.recvuntil("s1")
        result = sock.recvuntil("pwndbg> ").decode()
        sock.close()
        result = re.sub(r"\x1b\[[0-9;]*m", "", result)
        s1_s2 = re.findall(r"◂—\s*(0x[0-9a-fA-F]+)", result)
        if s1_s2[0] == s1_s2[1]:
            print(f"flag[{i}] = {c}")
            break

print(f"flag = {''.join(flag)}")
```
実行する。  
```bash
flag[0] = A
flag[1] = l
flag[2] = p
~~~
flag[45] = c
flag[46] = a
flag[47] = k
flag[48] = }
flag = Alpaca{h4sh_4lgor1thm_1s_b4s3d_0n_MD5_4nd_keccak}
```
flagが得られた。  

## Alpaca{h4sh_4lgor1thm_1s_b4s3d_0n_MD5_4nd_keccak}