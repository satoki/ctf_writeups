# web_meta:Web:100pts
フラグが書いてあるHTMLのはずなのに、ブラウザで開いても見当たりません！開発者の気持ちになって探しましょう！  
[web_meta.zip](web_meta.zip)  

# Solution
ファイルが配布される。  
解凍するとhtmlファイルのようだ。  
stringsしてみる。  
```bash
$ strings super_cite.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="flag is nitic_ctf{You_can_see_dev_too1!}">
    <title>nitic_ctf_2</title>
</head>
<body>
    nitic ctf 2
</body>
</html>
```
問題名の通りmetaタグにフラグが書かれていた。  

## nitic_ctf{You_can_see_dev_too1!}