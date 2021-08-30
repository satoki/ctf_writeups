# Mx.Flag:Web:150pts
旗から手紙が届きました。  
```
親愛なる貴方へ

こうして貴方に手紙を送るのは初めてですね。  
実はとてもうまく隠れることができたので、嬉しくなりこのような手紙を送ることにしました。  

どうか私を見つけてくれますか？

旗
```
以下のサイトにアクセスしてフラグを得てください。  
[https://ctf.setodanote.net/web007/](https://ctf.setodanote.net/web007/)  

# Solution
アクセスすると英語版の手紙が表示される。  
Letter of challenge from Flag  
[site.png](site/site.png)  
ソースを見ても何もないため迷うが、読み込まれるファイルを解析するとfavicon.pngが壊れている。  
落としてきて解析を行う。  
```bash
$ wget https://ctf.setodanote.net/web007/images/favicon.png
~~~
$ file favicon.png
favicon.png: ASCII text, with CRLF line terminators
$ cat favicon.png
// flag{Mr_Flag_hiding_in_the_favicon}
console.table({place: "favicon.png", png: "false", flag: "true", Look: "me"});

```
flagが書かれていた。  

## flag{Mr_Flag_hiding_in_the_favicon}