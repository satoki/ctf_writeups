# js:Misc:30pts
`(`, `)`, `[`, `]`, `+`, `!`の6種類の文字のみで, "yes" という文字列を作れますか？  
※このエンドポイントは、当該エンドポイントへのPOSTリクエスト以外のリクエストを全て拒否します。 POSTリクエストが送信できる媒体をご利用ください。  
**Curlコマンドを利用する場合**  
```
$ curl 34.145.29.222:30009 -X POST -d '{"want_flag": "XXXX(ここに文字列が入る)"}'
```
[dist.zip](dist.zip)  

# Solution
JSFuck問のようだ。  
文字列"yes"を作ってPOSTしてやる。  
[Wikipedia](https://ja.wikipedia.org/wiki/JSFuck)にアルファベット一覧がある。  
`y`、`e`、`s`を使用する。  
```
y
(+[![]]+[+(+!+[]+(!+[]+[])[!+[]+!+[]+!+[]]+(+!+[])+(+[])+(+[])+(+[]))])[+!+[]+[+[]]]
e
(!![]+[])[!+[]+!+[]+!+[]]
s
(![]+[])[!+[]+!+[]+!+[]]
```
`+`で連結すればよい。  
```bash
$ curl 34.145.29.222:30009 -X POST -d '{"want_flag": "(+[![]]+[+(+!+[]+(!+[]+[])[!+[]+!+[]+!+[]]+(+!+[])+(+[])+(+[])+(+[]))])[+!+[]+[+[]]]+(!![]+[])[!+[]+!+[]+!+[]]+(![]+[])[!+[]+!+[]+!+[]]"}'
Bad Request
```
Bad Requestになるが、配布されたソースセットにsolve.shがある。  
```bash
$ curl 34.145.29.222:30009 -X POST -d '{"want_flag": "(+[![]]+[+(+!+[]+(!+[]+[])[!+[]+!+[]+!+[]]+(+!+[])+(+[])+(+[])+(+[]))])[+!+[]+[+[]]]+(!![]+[])[!+[]+!+[]+!+[]]+(![]+[])[!+[]+!+[]+!+[]]"}' -H 'Content-Type: application/json'
taskctf{js_1s_4_tr1cky_l4ngu4ge}
```
Content-Typeを指定してやるとflagが得られた。  

## taskctf{js_1s_4_tr1cky_l4ngu4ge}