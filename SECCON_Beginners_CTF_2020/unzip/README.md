# unzip:Web:188pts
Unzip Your .zip Archive Like a Pro.  
- [https://unzip.quals.beginners.seccon.jp/](https://unzip.quals.beginners.seccon.jp)  
Hint:  
- [index.php (sha1: 968357c7a82367eb1ad6c3a4e9a52a30eada2a7d)](index.php-968357c7a82367eb1ad6c3a4e9a52a30eada2a7d)  
Hint  
- (updated at 5/23 17:30) [docker-compose.yml](docker-compose.yml-591e0b33b6a4485d7f6518c7efee547fad257ea2)  

# Solution
zipを解凍してくれるサービスのようだ。  
Unzip  
[site.png](site/site.png)  
test.phpファイルを圧縮したtest.zipを解凍させたが動作しない。  
Content-Type: text/plain;charset=UTF-8であった。  
URLを見ると?filename=test.phpとあったので?filename=../../../../etc/passwdなどディレクトリトラバーサルを試すも失敗に終わった。  
docker-compose.ymlを見るとflagは/flag.txtに書かれているようだ。  
index.phpを見ると以下の記述があった。  
```php:index.php
~~~
// prepare the session
$user_dir = "/uploads/" . session_id();
if (!file_exists($user_dir))
    mkdir($user_dir);

if (!isset($_SESSION["files"]))
    $_SESSION["files"] = array();

// return file if filename parameter is passed
if (isset($_GET["filename"]) && is_string(($_GET["filename"]))) {
    if (in_array($_GET["filename"], $_SESSION["files"], TRUE)) {
        $filepath = $user_dir . "/" . $_GET["filename"];
        header("Content-Type: text/plain");
        echo file_get_contents($filepath);
        die();
    } else {
        echo "no such file";
        die();
    }
}
~~~
```
セッションに紐付けられているファイル名でディレクトリトラバーサルができそうだ。  
../../flag.txtをファイル名にすればよいので、..{..{flag.txtを圧縮し、そのzipファイルをバイナリエディタなどで編集する。  
それを解凍させてやればflagが得られる。  

## ctf4b{y0u_c4nn07_7ru57_4ny_1npu75_1nclud1n6_z1p_f1l3n4m35}