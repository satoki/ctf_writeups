# Missing Image:Web:75pts
Max has been trying to add a picture to his first website. He uploaded the image to the server, but unfortunately, the image doesn't seem to be loading. I think he might be looking in the wrong subdomain...  
[https://hidden.challenges.nactf.com/](https://hidden.challenges.nactf.com/)  

# Solution
URLにアクセスするが、以下のような緑のページだった。  
Where's the flag?  
[site.png](site/site.png)  
ソースを見ると、以下のようにflag.pngの場所がおかしいようだ。  
```html:index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>Where's the flag?</title> <!-- (It's not here) -->
</head>
<body>
<h1>Where's the flag?</h1>
<img src="http://challenges.nactf.com/flag.png" alt="">
</body>
</html>
```
正しい場所`https://hidden.challenges.nactf.com/flag.png`に以下の画像があった。  
![flag.png](flag.png)  
flagが書かれている。  

## nactf{h1dd3n_1mag3s}