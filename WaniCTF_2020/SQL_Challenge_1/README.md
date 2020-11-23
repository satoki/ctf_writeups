# SQL Challenge 1:Web:102pts
問題ページ： [https://sql1.wanictf.org/index.php?year=2011](https://sql1.wanictf.org/index.php?year=2011)  
今まで見たアニメのリストをデータベースに登録したよ。間違えて秘密の情報（FLAG）もデータベースに登録しちゃったけど、たぶん誰にも見られないし大丈夫だよね。  
(Hint)  
SQL injectionの問題です。  
URLの「year=」の後に続く数字(年号)をSQL injectionを起こすような文字列に変更するとFLAGが表示されます。  
一部使えない文字もあるのでソースコード(index.php)を参考に考えてみてください。  
必要に応じてデータベースのスキーマ(1_schema.sql)も参考にしてください。  
(注意)  
sql-chall-1.zipは問題を解くために必須の情報ではなく、docker-composeを利用してローカルで問題環境を再現するためのものです。  
興味のある方は利用してみてください。  
[index.php](index.php)　　　　[1_schema.sql](1_schema.sql)　　　　[sql-chall-1.zip](sql-chall-1.zip)  

# Solution
URLにアクセするとアニメのリストが表示される。  
SQL_Challenge_1  
[site.png](site/site.png)  
index.phpを見ると以下の部分でSQLインジェクションが可能であることに気付く。  
```php
~~~
                    //urlの"year="の後に入力した文字列を$yearに入れる。
                    $year = $_GET["year"];

                    //一部の文字は利用出来ません。以下の文字を使わずにFLAGを手に入れてください。
                    if (preg_match('/\s/', $year))
                        exit('危険を感知'); //スペース禁止
                    if (preg_match('/[\']/', $year))
                        exit('危険を感知'); //シングルクォート禁止
                    if (preg_match('/[\/\\\\]/', $year))
                        exit('危険を感知'); //スラッシュとバックスラッシュ禁止
                    if (preg_match('/[\|]/', $year))
                        exit('危険を感知'); //バーティカルバー禁止                    

                    //クエリを作成する。
                    $query = "SELECT * FROM anime WHERE years =$year";
~~~
```
禁止文字以外を使ってTrueにしてやればよい。  
`1!=1`により常にTrueとすることができる。  
`https://sql1.wanictf.org/index.php?year=1!=1`で全データが列挙され、その中にflagがあった。  
flag  
[flag.png](site/flag.png)  

## FLAG{53cur3_5ql_a283b4dffe}