# SQL Challenge 2:Web:pts
問題ページ： [https://sql2.wanictf.org/index.php?year=2011](https://sql2.wanictf.org/index.php?year=2011)  
やっぱり前のページは危ない気がするからページを作り直したよ。これで大丈夫だね。  
(Hint)  
SQL injectionの問題です。  
必要に応じてソースコード(index.php)とデータベースのスキーマ(1_schema.sql)を参考にしてください。  
(注意)  
sql-chall-2.zipは問題を解くために必須の情報ではなく、docker-composeを利用してローカルで問題環境を再現するためのものです。  
興味のある方は利用してみてください。  
[index.php](index.php)　　　　[1_schema.sql](1_schema.sql)　　　　[sql-chall-2.zip](sql-chall-2.zip)  

# Solution
URLにアクセするとアニメのリストが表示される。  
SQL_Challenge_2  
[site.png](site/site.png)  
index.phpを見ると以下の部分でSQLインジェクションが可能であることに気付く。  
```php
~~~
                    //urlの"year="の後に入力した文字列を$yearに入れる。
                    $year = $_GET["year"];

                    //preg_replaceで危険な記号を処理する。
                    $pattern = '/([^a-zA-Z0-9])/';
                    $replace = '\\\$0';
                    $year = preg_replace($pattern, $replace, $year);

                    //クエリを作成する。
                    $query = "SELECT * FROM anime WHERE years = $year";
~~~
```
アルファベットや数字以外は入力できない。  
1_schema.sqlを見ると[SQL Challenge 1](../SQL_Challenge_1)ではINTだったものが変化している。  
```sql
DROP TABLE IF EXISTS anime;

CREATE TABLE anime (
    name VARCHAR(32) NOT NULL,
    years VARCHAR(32) NOT NULL,
    PRIMARY KEY (name)
);
```
`years=0`は暗黙の型変換により、数字として解釈できる文字列以外がTrueになる(実際はクエリを適当に入れて`years=False`を発見した)。  
`https://sql2.wanictf.org/index.php?year=0`でyearsが数字として解釈できないflagが表示された。  
flag  
[flag.png](site/flag.png)  

## FLAG{5ql_ch4r_cf_ca87b27723}