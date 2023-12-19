# German shell:rev:277pts
Do you have an Albert Einstein in you? If not you better find one cuz you gonna need em else you gunna faint rottin  
`/var/quantumLava/flag.txt`  
`nc 35.244.43.8 1337`  

# Solution
接続先が渡される。  
```bash
$ nc 35.244.43.8 1337
$ ls
/bin/sh: 1: tl: not found

$ pwd
/bin/sh: 1: fxp: not found
```
シェルが動いているようだが、謎の文字変換がかかっている。  
入力文字列を反転して、文字の番目に応じて変換しているようだ。  
記号を確認する。  
```bash
$ nc 35.244.43.8 1337
$ //////////
/bin/sh: 1: %%%%%%%%%%: not found

$ //////////
/bin/sh: 1: Syntax error: "&&" unexpected

$ //////////
/bin/sh: 1: 0000000000: not found

$ //////////
/bin/sh: 1: !!!!!!!!!!: not found

$ //////////

$ **********
/bin/sh: 1: **********: not found

$ **********
/bin/sh: 1: //////////: Permission denied

$ **********
/bin/sh: 1: : Permission denied

$ **********
/bin/sh: 1: !!!!!!!!!!: not found

$ **********
/bin/sh: 1: 1212121212: not found
```
ランダムに変わるようだ。  
問題文から`cat /v*/q*/f*`すればよさそうだ。  
アルファベットは一文字ずつ確認し決めてやると、`*e/*m/*o/ jpq`のようになる。  
あとは記号がうまくマッチするまで試せばよい。  
```bash
$ nc 35.244.43.8 1337
$ *e/*m/*o/ jpq
/bin/sh: 1: Syntax error: word unexpected (expecting ")")

$ *e/*m/*o/ jpq
nite{tr7n517t10n_u51ng_t1m3_n0t_c001_00000yx}
```
flagが得られた。  

## nite{tr7n517t10n_u51ng_t1m3_n0t_c001_00000yx}