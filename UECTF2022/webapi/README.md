# webapi:WEB:100pts
サーバーからフラグを取ってきて表示する web ページを作ったけど、上手く動かないのはなんでだろう？  
I created a web page that fetches flags from the server and displays them, but why doesn't it work?  

[http://uectf.uec.tokyo:4447](http://uectf.uec.tokyo:4447/)  

# Solution
URLが渡される。  
![site.png](site/site.png)  
`Flag is here: server error`と表示されている。  
問題文からSSRF系かと思っていたが、ソースを見ると以下のようであった。  
```bash
$ curl http://uectf.uec.tokyo:4447/
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <h1>Hello world!</h1>
  <div class="flag">
    <span class="flag-label">Flag is here:</span>
    <span class="flag-data"></span>
  </div>
</body>

<script>
  const FLAG_URL = 'https://i5omltk3rg2vbwbymc73hnpey40eowfq.lambda-url.ap-northeast-1.on.aws/';
  fetch(FLAG_URL)
    .then(data => {
      document.getElementsByClassName('flag-data')[0].innerText = data;
    })
    .catch(err => {
      document.getElementsByClassName('flag-data')[0].innerText = 'server error';
    })
</script>
</html>
```
直接`FLAG_URL`を叩けばよさそうだ。  
```bash
$ curl https://i5omltk3rg2vbwbymc73hnpey40eowfq.lambda-url.ap-northeast-1.on.aws/
UECTF{cors_is_browser_feature}
```
flagが得られた。  

## UECTF{cors_is_browser_feature}