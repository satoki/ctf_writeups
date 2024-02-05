# zshfuck:misc:127pts
may your code be under par. execute the `getflag` binary somewhere in the filesystem to win  
`nc mc.ax 31774`  

[jail.zsh](jail.zsh)  

# Solution
接続先とソースが渡される。  
ソースは以下のようであった。  
```zsh
#!/bin/zsh
print -n -P "%F{green}Specify your charset: %f"
read -r charset
# get uniq characters in charset
charset=("${(us..)charset}")
banned=('*' '?' '`')

if [[ ${#charset} -gt 6 || ${#charset:|banned} -ne ${#charset} ]]; then
    print -P "\n%F{red}That's too easy. Sorry.%f\n"
    exit 1
fi
print -P "\n%F{green}OK! Got $charset.%f"
charset+=($'\n')

# start jail via coproc
coproc zsh -s
exec 3>&p 4<&p

# read chars from fd 4 (jail stdout), print to stdout
while IFS= read -u4 -r -k1 char; do
    print -u1 -n -- "$char"
done &
# read chars from stdin, send to jail stdin if valid
while IFS= read -u0 -r -k1 char; do
    if [[ ! ${#char:|charset} -eq 0 ]]; then
        print -P "\n%F{red}Nope.%f\n"
        exit 1
    fi
    # send to fd 3 (jail stdin)
    print -u3 -n -- "$char"
done
```
一回目に`*`、`?`、`` ` ``を除く6種類以下の文字を入力し、それらの文字だけで構成されたスクリプトを二回目に入力するとzshで実行してくれる。  
フラグはどこかにある`getflag`を実行する必要があるようだ。  
まずは`getflag`の場所だが、チームメンバが`find .`でディレクトリ一覧が表示されることを発見していた。  
```bash
$ nc mc.ax 31774
Specify your charset: find .

OK! Got f i n d   ..
find .
.
./y0u
./y0u/w1ll
./y0u/w1ll/n3v3r_g3t
./y0u/w1ll/n3v3r_g3t/th1s
./y0u/w1ll/n3v3r_g3t/th1s/getflag
./run
~~~
$ nc mc.ax 31774
Specify your charset: find .

OK! Got f i n d   ..
find ..
..
../app
../app/y0u
../app/y0u/w1ll
../app/y0u/w1ll/n3v3r_g3t
../app/y0u/w1ll/n3v3r_g3t/th1s
../app/y0u/w1ll/n3v3r_g3t/th1s/getflag
../app/run
../boot
../tmp
../libx32
../lib32
../etc
~~~
```
`find ..`で一つ上がルートであり、`/app/y0u/w1ll/n3v3r_g3t/th1s/getflag`を実行すればよいことがわかる。  
文字種を削減するため`/a**/***/****/*********/****/g******`のようにワイルドカードを利用したいが、禁止されている。  
ここでzshのワイルドカードを調べると`[a-z]`のようにアルファベット小文字を指定できることがわかる。  
`[a-z]`と`/`で6種類だがパスに数字や記号があるためマッチしない。  
試行錯誤すると`[0-z]`で良いことがわかる。  
以下のように行う。  
```bash
$ nc mc.ax 31774
Specify your charset: [0-z]/

OK! Got [ 0 - z ] /.
/[0-z][0-z][0-z]/[0-z][0-z][0-z]/[0-z][0-z][0-z][0-z]/[0-z][0-z][0-z][0-z][0-z][0-z][0-z][0-z][0-z]/[0-z][0-z][0-z][0-z]/[0-z][0-z][0-z][0-z][0-z][0-z][0-z]
dice{d0nt_u_jU5T_l00oo0ve_c0d3_g0lf?}
```
flagが得られた。  

## dice{d0nt_u_jU5T_l00oo0ve_c0d3_g0lf?}