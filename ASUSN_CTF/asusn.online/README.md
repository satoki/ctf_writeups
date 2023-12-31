# asusn.online:Misc:pts
[https://asusn.online](https://asusn.online) というドメインを取得したらしい  
今はYouTubeにリダイレクトされるが、リダイレクトされる前のページにFlagが隠されているとかいないとか......？  

# Solution
リダイレクトされる前のページに何かあるようだ。  
curlしてみる。  
```bash
$ curl https://asusn.online
<html>
<head>
<meta http-equiv="refresh" content="0; url=https://www.youtube.com/@full-weak-engineer">
<title>脆弱エンジニアの日常</title>
</head>
<body>
  <p style="color:white">Flagは「鳥取アクエリイーグルス」</p>
</body>
</html>
```
flagが得られた。  

## 鳥取アクエリイーグルス