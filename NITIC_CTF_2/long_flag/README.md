# long flag:Web:200pts
[https://quizzical-mcnulty-e4cdbf.netlify.app/](https://quizzical-mcnulty-e4cdbf.netlify.app/)

# Solution
アドレスのみが渡される。  
long flag  
[site.png](site/site.png)  
flagが書かれているのだろうが見えない。  
ソースを見ると`<span>n</span><span>i</span>`のようにflagが一文字ずつspanタグに囲まれている。  
curlして邪魔なタグを消してやればいい。  
```bash
$ curl https://quizzical-mcnulty-e4cdbf.netlify.app/ |\
> tr -d "\n" |\
> python -c 'print(input().replace("<span>","").replace("</span>",""))' |\
> grep -oP nitic_ctf{.*?}
~~~
nitic_ctf{Jy!Hxj$RdB$uA,b$uM.bN7AidL6qe4gkrB9dMU-jY8KU828ByP9E#YDi9byaF4sQ-p/835r26MT!QwWWM|c!ia(ynt48hBs&-,|3}
```
だいぶ無理やりだがflagが表示された。  

## nitic_ctf{Jy!Hxj$RdB$uA,b$uM.bN7AidL6qe4gkrB9dMU-jY8KU828ByP9E#YDi9byaF4sQ-p/835r26MT!QwWWM|c!ia(ynt48hBs&-,|3}