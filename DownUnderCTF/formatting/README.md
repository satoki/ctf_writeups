# formatting:reversing:100pts
Its really easy, I promise  
Files: [formatting](https://play.duc.tf/files/235a555e84c8fe3cdbd0bb4c90389583/formatting)  
[formatting](formatting)  

# Solution
ファイルが渡されるので実行するが以下のようになるだけである。  
stringsでも完全なものは出てこないようだ。  
```bash
$ ./formatting
haha its not that easy}
$ strings ./formatting
/lib64/ld-linux-x86-64.so.2
libc.so.6
sprintf
puts
__cxa_finalize
__libc_start_main
GLIBC_2.2.5
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
u/UH
ARAQAPWQA
[]A\A]A^A_
DUCTF{haha its not that easy}
%s%02x%02x%02x%02x%02x%02x%02x%02x}
d1d_You_Just_ltrace_
;*3$"
~~~
```
stringsで得られたダミーの先頭が消えているのが気になる。  
数字も不明である。  
gdbで解析する(一部出力は省略)。  
```bash
$ gdb ./formatting
gdb-peda$ start
gdb-peda$ n 40
```
![gdbpeda.png](images/[gdbpeda.png])  
stackにflagがあった。  

## DUCTF{d1d_You_Just_ltrace_296faa2990acbc36}