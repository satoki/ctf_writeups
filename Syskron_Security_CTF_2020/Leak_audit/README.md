# Leak audit:Tuesday:200pts
We found an old dump of our employee database on the dark net! Please check the database and send us the requested information:  
    1. How many employee records are in the file?  
    2. Are there any employees that use the same password? (If true, send us the password for further investigation.)  
    3. In 2017, we switched to bcrypt to securely store the passwords. How many records are protected with bcrypt?  
Flag format: answer1_answer2_answer3 (e.g., 1000_passw0rd_987).  
View Hint  
Knowing SQL doesn't hurt.  
[BB-inDu57rY-P0W3R-L34k3r2.tar.gz](BB-inDu57rY-P0W3R-L34k3r2.tar.gz)  

# Solution
渡されたファイルを解凍するとdbファイルが出てくる。  
```bash
$ tar -zxvf BB-inDu57rY-P0W3R-L34k3r2.tar.gz
BB-inDu57rY-P0W3R-L34k3r2.db
$ file *
BB-inDu57rY-P0W3R-L34k3r2.db:     SQLite 3.x database, last written using SQLite version 3033000
BB-inDu57rY-P0W3R-L34k3r2.tar.gz: gzip compressed data, from Unix
```
データベースファイルのようだ。  
調査するものは、データベースのレコード数、重複しているパスワード、ハッシュ化されているパスワード数の3つだ。  
[SQLite Viewer](http://inloop.github.io/sqlite-viewer/)なる神ウェブアプリに投げる。  
SQLite Viewer  
[SQLiteViewer.png](images/SQLiteViewer.png)  
personalテーブルがあるようだ。  
以下のように調査を行う。  
```SQL
SELECT count(number) FROM 'personal'
SELECT password FROM personal GROUP BY password HAVING COUNT(password) > 1
SELECT count(password) FROM personal WHERE password LIKE '%$%$%'
```
結果は以下になった。  
```text
376
mah6geiVoo
21
```
整形するとflagになる。  
ちなみにbcryptの形式は以下になっているらしい。  
$2b$10$H7bpJOSIguADfqQ/QJWEn.mXgOhmpKU83ycvyIENiChHarlPn0oa2  
暗号化のバージョン：$2b$  
ストレッチング回数：$10$  
ソルトとハッシュ：H7bpJOSIguADfqQ/QJWEn.mXgOhmpKU83ycvyIENiChHarlPn0oa2  

## 376_mah6geiVoo_21