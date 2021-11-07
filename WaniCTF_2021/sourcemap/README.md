# sourcemap:Web:158pts
へっへっへ...JavaScriptは難読化したから、誰もパスワードはわからないだろう...  
え? ブラウザの開発者ツールのxxx機能から見れちゃうって!?  
[https://sourcemap.web.wanictf.org](https://sourcemap.web.wanictf.org/)  

# Solution
アクセスするとパスワードをチェックするサイトのようだ。  
sourcemap  
[site.png](site/site.png)  
チェック機構が動いていそうなファイルは`/js/app.bcff35da.js`だったが、見ると以下のように難読化されていた。  
一部フラグのようなものが見える。  
```JavaScript
~~~
e(426,438,431,439)+e(440,447,438,437)+t(622,614,627,628)+t(626,634,618,617)+"_50urc3m4p}"
~~~
//# sourceMappingURL=app.bcff35da.js.map
```
ファイル末尾にあるコメントがソースマップなのでそちらをgrepすればよい。  
```bash
$ wget https://sourcemap.web.wanictf.org/js/app.bcff35da.js.map
~~~
$ grep -oP FLAG{.*?} app.bcff35da.js.map
FLAG{d3v700l_c4n_r3v34l_50urc3_c0d3_fr0m_50urc3m4p}
```

## FLAG{d3v700l_c4n_r3v34l_50urc3_c0d3_fr0m_50urc3m4p}