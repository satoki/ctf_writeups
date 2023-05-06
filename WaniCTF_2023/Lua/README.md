# Lua:Reversing:222pts
るあ〜  
Lua~~~  

---

配布ファイル`main.lua`のubuntuにおける実行方法  
How to run `main.lua` on ubuntu  
```bash
$ sudo apt update
$ sudo apt install lua5.1
$ lua main.lua
Input FLAG : FAKE{FAKE_FLAG}
Incorrect
```

[rev-lua.zip](rev-lua.zip)  

# Solution
luaファイルが配られる。  
実行するとただのフラグ当てプログラムのようだ。  
```bash
$ lua main.lua
Input FLAG : Satoki
Incorrect
```
中身はソースコードのようだが、難読化されており読むことが難しい。  
比較時点でメモリにフラグが乗っていることを睨んで、gdbで動的に見てやる(一部省略)。  
```bash
$ gdb --args lua main.lua
gdb-peda$ r
Starting program: /usr/bin/lua main.lua
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Input FLAG : ^C
~~~
gdb-peda$ find FLAG
Searching for 'FLAG' in: None ranges
Found 16 results, display max 16 items:
              [heap] : 0x555555592ff8 ("FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}")
              [heap] : 0x555555593d18 ("FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}")
              [heap] : 0x5555555b23b6 --> 0x203a2047414c46 ('FLAG : ')
              [heap] : 0x55555565526f --> 0x203a2047414c46 ('FLAG : ')
              [heap] : 0x5555556552ac ("FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}")
              [heap] : 0x55555565e56e --> 0x203a2047414c46 ('FLAG : ')
              [heap] : 0x55555565e59e --> 0x203a2047414c46 ('FLAG : ')
           libc.so.6 : 0x7ffff7e25e72 ("FLAG_MULTI) != 0")
ld-linux-x86-64.so.2 : 0x7ffff7fefb70 ("FLAGS:", ' ' <repeats 13 times>, "0x")
ld-linux-x86-64.so.2 : 0x7ffff7ff373a ("FLAGS_1.\n")
ld-linux-x86-64.so.2 : 0x7ffff7ff554b ("FLAGS_1)] == NULL || (info[VERSYMIDX (DT_FLAGS_1)]->d_un.d_val & ~DF_1_NOW) == 0")
ld-linux-x86-64.so.2 : 0x7ffff7ff5574 ("FLAGS_1)]->d_un.d_val & ~DF_1_NOW) == 0")
ld-linux-x86-64.so.2 : 0x7ffff7ff55a8 ("FLAGS] == NULL || (info[DT_FLAGS]->d_un.d_val & ~DF_BIND_NOW) == 0")
ld-linux-x86-64.so.2 : 0x7ffff7ff55c3 ("FLAGS]->d_un.d_val & ~DF_BIND_NOW) == 0")
             [stack] : 0x7fffffffbb3f --> 0x203a2047414c46 ('FLAG : ')
             [stack] : 0x7fffffffbb7c ("FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}")
```
flagがたくさん出てきた。  

## FLAG{1ua_0r_py4h0n_wh4t_d0_y0u_3ay_w4en_43ked_wh1ch_0ne_1s_be44er}