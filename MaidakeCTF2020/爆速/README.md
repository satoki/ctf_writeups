# 爆速:Web:200pts
この速さについてこれますか？[https://aokakes.work/MaidakeCTF2020/fast/](https://aokakes.work/MaidakeCTF2020/fast/)  
Hint  
勝手に飛ばされないように抗いましょう。  

# Solution
URLにアクセスすると以下のようなサイトだった。  
爆速  
[site.png](site/site.png)  
Get Flag!!ボタンをクリックすると、一瞬どこかに遷移するがまた戻ってしまう。  
Burp Suiteなどで詳細を見てもよい。  
FirefoxではEscキーを押すことで、読み込みを中止できる。  
タイミングよく中止すると、4f1d4bda3.htmlにアクセスしていることがわかる。  
curlで覗いてみる。  
```bash
$ curl https://aokakes.work/MaidakeCTF2020/fast/4f1d4bda3.html
<meta http-equiv="refresh" content="0;URL='./'" flag="MaidakeCTF{Kirito_is_said_to_be_able_to_go_720km/h_when_he_uses_his_sword_skill}">
```
リダイレクトのタグとともにflagが書かれていた。  

## MaidakeCTF{Kirito_is_said_to_be_able_to_go_720km/h_when_he_uses_his_sword_skill}