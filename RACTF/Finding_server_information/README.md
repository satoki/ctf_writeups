# Finding server information:Web:350pts
Challenge instance ready at 95.216.233.106:10175.  
See if you can find the source, we think it's called app.py  

# Solution
アクセスするとSign inとSign upがあるが、Sign upは現在停止しているようだ。  
RAQE  
[site.png](../Quarantine_-_Hidden_information/site/site.png)  
SQLインジェクション`t' OR LENGTH(username) = 5 --`でログインすると動画が見られるようだ。  
Three videos avaliable  
[site1.png](../Quarantine/site/flag.png)  
/watch/HMHT.mp4  
[site2.png](site/site2.png)  
/watch/TIOK.mp4  
[site3.png](site/site3.png)  
watch/TCYI.mp4  
[site4.png](site/site4.png)  
どこもおかしな点は見られないが、data:video/mp4;が埋め込まれている。  
ファイル名を問題の通りapp.pyにしてみる。  
/watch/app.py  
[site5.png](site/site5.png)  
読み込めていないように見えるが、ソースにしっかりと埋め込まれている。  
```html
~~~
    <center>
        <h1>Watch video</h1>
        
        <div class="video">
            <video controls src="data:video/mp4;base64,ractf{qu3ry5tr1ng_m4n1pul4ti0n}"></video>
        </div>
    </center>
~~~
```

## ractf{qu3ry5tr1ng_m4n1pul4ti0n}