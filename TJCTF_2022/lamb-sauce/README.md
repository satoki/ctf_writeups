# lamb-sauce:web:116pts
where's the lamb sauce  
[lamb-sauce.tjc.tf](https://lamb-sauce.tjc.tf/)  

# Solution
アクセスすると謎のサイトであった。  
where's the lamb sauce  
[site.png](site/site.png)  
ソースを見ると以下のようであった。  
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>where's the lamb sauce</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
      }

      body {
        font-family: Arial, Helvetica, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
      }
    </style>
  </head>

  <body>
    <main>
      <h1>where's the lamb sauce</h1>
      <iframe width="560" height="315" src="https://www.youtube.com/embed/-wlDVf-qwyU?controls=0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
      <!-- <a href="/flag-9291f0c1-0feb-40aa-af3c-d61031fd9896.txt"> is it here? </a> -->
    </main>
  </body>
</html>
```
謎のコメントがあるので取得する。  
```bash
$ curl https://lamb-sauce.tjc.tf/flag-9291f0c1-0feb-40aa-af3c-d61031fd9896.txt
tjctf{idk_man_but_here's_a_flag_462c964f0a177541}
```
flagが得られた。  

## tjctf{idk_man_but_here's_a_flag_462c964f0a177541}