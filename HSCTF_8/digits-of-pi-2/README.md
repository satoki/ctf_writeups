# digits-of-pi-2:web:474pts
This [spreadsheet](https://docs.google.com/spreadsheets/d/1NX9nUMrpaxGqChQ7ROzITDtlxaz5McSsN5BMs-o5k-M/edit) is Secure™  

# Solution
スプレッドシートが渡される。  
Digits of pi 2.0  
[site.png](site/site.png)  
数式を確認するとA2に`=QUERY(IMPORTRANGE("1MD4O3pFoQY59_YoW_ZzxRUg-rBgHFlAaYxnNABmqc3A","A:Z"),"SELECT Col1, Col2")`とあった。  
非公開のスプレッドシート`1MD4O3pFoQY59_YoW_ZzxRUg-rBgHFlAaYxnNABmqc3A`があるようで、それを表示しているようだがセルがデータ分しか用意されていない。  
文字列`flag`での検索を行ってもそれらしいものは発見できない。  
データ自体は引っ張ってきているため、通信内容を読めばよさそうだと考える。  
ブラウザの開発者ツールのネットワークからレスポンスの中身を浚う。  
![flag.png](images/flag.png)  
`m4k3_sur3_t0_r3str1ct_y0ur_imp0rtr4ng3s`なる怪しい文字列が見つかった。  
形式どおりに整形するとflagとなった。  

## flag{m4k3_sur3_t0_r3str1ct_y0ur_imp0rtr4ng3s}