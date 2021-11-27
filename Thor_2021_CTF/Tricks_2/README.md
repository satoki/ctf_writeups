# Tricks 2:Web:pts
Another round of PHP Tricks, good luck.  
[Click here](https://ch6.sbug.se/)  

# Solution
アクセスすると第二のPHP問であることがわかる。  
[site.png](site/site.png)  
```php
 <?php error_reporting(0);if(isset($_GET[base64_decode('YQ==')])&&isset($_GET[base64_decode('Yg==')])){if(strlen($_GET[base64_decode('YQ==')])>mb_strlen($_GET[base64_decode('Yg==')],base64_decode('dXRmOA=='))){if(strlen($_GET[base64_decode('Yg==')])>mb_strlen($_GET[base64_decode('YQ==')],base64_decode('dXRmOA=='))){$u327a6c4304ad5938=file_get_contents(base64_decode('Li4vLi4vZmxhZw=='));echo $u327a6c4304ad5938;}else{echo base64_decode('QWxyaWdodC4=');}}else{echo base64_decode('VHJ5IGhhcmRlci4=');}}else{highlight_file(__FILE__);die();}?> 
```
邪魔なbase64などを取っ払うと以下になる。  
```php
<?php
error_reporting(0);
if(isset($_GET['a'])&&isset($_GET['b'])){
    if(strlen($_GET['a'])>mb_strlen($_GET['b'],'utf8')){
        if(strlen($_GET['b'])>mb_strlen($_GET['a'],'utf8')){
            $u327a6c4304ad5938=file_get_contents('../../flag');
            echo $u327a6c4304ad5938;
        }else{
            echo 'Alright.';
        }
    }else{
        echo 'Try harder.';
    }
}else{
    highlight_file(__FILE__);
    die();
}
?>
```
strlenがmb_strlenより長くなるものを二つ与えてやればよい。  
strlenはバイト数を返すのでマルチバイト文字を利用すればよいことがわかる。  
```bash
$ curl "https://ch6.sbug.se/?a=あ&b=あ"
SBCTF{d1d_y0u_kn0w_abou7_7h47?}
```
日本語でおｋ

## SBCTF{d1d_y0u_kn0w_abou7_7h47?}