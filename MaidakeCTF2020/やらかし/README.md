# やらかし:Web:300pts
会員限定サイトを作りました。新規登録は出来ません。 [https://aokakes.work/MaidakeCTF2020/yarakashi/](https://aokakes.work/MaidakeCTF2020/yarakashi/)  
Hint  
URLの末尾に「?source」をくっつけると...  
ゲットしたそいつはsqliteです。  

# Solution
URLにアクセスすると、ただのログインフォームだ。  
やらかし  
[site.png](site/site.png)  
SQLインジェクションなど試してみるがエラーが発生しない。  
ソースを見ると`<!-- ?source -->`なるコメントがあった。  
アクセスすると以下のソースが表示された。  
```php
<?php
if (isset($_GET['source'])) {
    show_source(__FILE__);
    exit();
}
$error = '';
if (isset($_POST['name']) && isset($_POST['password'])) {
    $name = $_POST['name'];
    $pw = $_POST['password'];

    $pdo = new PDO('sqlite:./KazutoKirigaya.db');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

    $sql = $pdo->prepare('SELECT * FROM users');
    $sql->execute();
    $result = $sql->fetchAll(PDO::FETCH_ASSOC);

    if ($name == $result[0]['name'] && base64_encode($pw) == $result[0]['pw']) {
        session_start();
        session_regenerate_id(true);
        $_SESSION['user'] = $result[0]['name'];
        header("Location: ./flag.php");
    } else {
        $error = 'くぅ～！残念っ！！';
    }
}
?>
~~~
```
nameとbase64したpasswordでログインするようだ。  
`KazutoKirigaya.db`が気になるが、どうやら取得できるようなのでwgetしてみる。  
```bash
$ wget https://aokakes.work/MaidakeCTF2020/yarakashi/KazutoKirigaya.db
~~~
$ file KazutoKirigaya.db
KazutoKirigaya.db: SQLite 3.x database, last written using SQLite version 3026000
$ strings KazutoKirigaya.db
SQLite format 3
tableusersusers
CREATE TABLE users (
name VARCHAR(256) PRIMARY KEY,
pw VARCHAR(256)))
indexsqlite_autoindex_users_1users
5EugeoU3RhcmJ1cnN0U3RyZWFt
        Eugeo
```
stringsでnameとpassword(base64)が取得できた。  
デコードすると以下になる。  
```text
Eugeo
U3RhcmJ1cnN0U3RyZWFt

Eugeo
StarburstStream
```
ログインするとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## MaidakeCTF{The_motorcycle_Kirito_is_riding_is_said_to_be_a_DT125R}