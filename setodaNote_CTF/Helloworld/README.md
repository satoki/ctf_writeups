# Helloworld:Rev:50pts
気が付くと椅子に座っていた。簡単なテストから始めよう。ガラスを隔てて真正面に白衣の女が立っている。君が優秀であることを示してくれ。声は天井のスピーカーから聞こえてくるようだ。心配はいらない。そばにある端末が起動する。どちらにしてもすぐに済む。  
添付されたファイルを解析してフラグを得てください。  
**ファイルは「`infected`」というパスワード付き ZIP になっています。**  
[helloworld_dd6b4bbaf0353c9a2d2093ac88135f9b760599db.zip](helloworld_dd6b4bbaf0353c9a2d2093ac88135f9b760599db.zip)  

# Solution
配布されたファイルはexeだが、ウイルス検体に用いられるパスワードなので仮想マシンで実行する。  
```cmd
>helloworld.exe
Nice try, please set some word when you run me.
>helloworld.exe a
Good job, but please set 'flag' when you run me.
>helloworld.exe flag
flag{free_fair_and_secure_cyberspace}
```
flagが表示された。

## flag{free_fair_and_secure_cyberspace}