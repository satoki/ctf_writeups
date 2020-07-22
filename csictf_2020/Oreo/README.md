# Oreo:Web:100pts
My nephew is a fussy eater and is only willing to eat chocolate oreo. Any other flavour and he throws a tantrum.  
[http://chall.csivit.com:30243](http://chall.csivit.com:30243/)  

# Solution
アクセスすると以下のように問題文と同じ文が表示された。  
```text
My nephew is a fussy eater and is only willing to eat chocolate oreo. Any other flavour and he throws a tantrum.
```
[site.png](site/site.png)  
クッキーを見てみると以下が入っていた。  
```text
c3RyYXdiZXJyeQ==
```
base64でデコードすると、`strawberry`となる。  
これを`chocolate`に変えてやればいい。  
クッキーに以下をセットする。  
```text
Y2hvY29sYXRl
```
サイトにアクセスするとflagが表示された。  
[flag.png](site/flag.png)  

## csictf{1ick_twi5t_dunk}