# Typing game:Web:10.00pts
面白そうなタイピングゲームを見つけたぞ！早速やってみよう♪  
...なんかムズくない？？？？？  
問題サイト：[https://typing-game.web.cpctf.space/](https://typing-game.web.cpctf.space/)  

**Hint**  
ほとんどのWebブラウザには開発者ツールがあり、Webページの裏側を覗いてみることができる。  
ゲームのプログラムのコードを読み取ったり、隠された画面の要素を調べることも思いのままだ。  

# Solution
アクセスすると**わくわく**タイピングゲームのようだ。  
![site1.png](site/site1.png)  
恐ろしいことに、10sで以下の量の文字を打ち込む必要がある。  
![site2.png](site/site2.png)  
現実で行うと手が爆発するので、jsのソースを見る。  
```bash
$ curl -sL 'https://typing-game.web.cpctf.space/main.js' | grep -Po CPCTF{.*?}
CPCTF{y0u_4r3_4_typ1ng_m45t3r}
```
flagが書かれていた。  

## CPCTF{y0u_4r3_4_typ1ng_m45t3r}