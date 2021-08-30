# identify_the_source:OSINT:250pts
組織はある攻撃者グループの動向を調査しています。あなたは旧知の情報提供者からその攻撃者グループが攻撃に利用しようとしているというファイルを入手することに成功しました。情報提供者はファイルの配布元URLの情報も持っているようですが、そちらの情報を入手するためには高額な対価が必要となりそうです。あなたが自由にできる予算は限られています。巧みな話術でどうやらあるマルウェア解析サイトから取得した情報であるようだというところまでは聞き出せました。組織はあなたに配布元URLを特定し、攻撃を未然に防ぐとともに攻撃者グループに関する重要な情報が含まれていないか調査するよう指示を出しました。  
添付されたファイルを解析して関連する配布URLを特定、調査し、フラグを入手してください。  
[identify_the_source_318ddc101a919d78eeea3551455bc7e26455d73c.zip](identify_the_source_318ddc101a919d78eeea3551455bc7e26455d73c.zip)  

# Solution
謎のtsuruというファイルが渡される。  
どうやら攻撃に利用されるファイルのようで、配布元を調査すればよいらしい。  
[ANY.RUN](https://any.run/)にて検索をかけるとヒットする。  
![ar.png](images/ar.png)  
15 July 2021, 00:23の実行が`https://yrsuccessesareunheraldedyrfailuresaretrumpeted.setodanote.net/tsuru`からのようで怪しい。  
curlするがもう何もないようだ。  
```bash
$ curl https://yrsuccessesareunheraldedyrfailuresaretrumpeted.setodanote.net
<!DOCTYPE HTML>
<html>
        <head>
                <title>Good job</title>
                <meta charset="utf-8" />
                <link rel="stylesheet" href="main.css" />
        </head>
        <body>
        <p>NO DATA</p>
        <br />
        <br />
        <br />
~~~
        <br />
        <br />
        <br />
        <p deleteTime="1626307200">The flag is no longer here.</p>
        </body>
</html>
```
Wayback Machineでみると複数のアーカイブがある。  
2021/07/15 00:23周辺のものを見ればよい。  
[2021/07/14 16:21:01のアーカイブ](https://web.archive.org/web/20210714162101/https://yrsuccessesareunheraldedyrfailuresaretrumpeted.setodanote.net/)にコメントでflagが書かれていた。  
```bash
$ curl https://web.archive.org/web/20210714162101/https://yrsuccessesareunheraldedyrfailuresaretrumpeted.setodanote.net/
~~~
                <title>Now loading</title>
                <meta charset="utf-8"/>
                <link rel="stylesheet" href="/web/20210714162101cs_/https://yrsuccessesareunheraldedyrfailuresaretrumpeted.setodanote.net/main.css"/>
        </head>
        <body>
        <p>Now laoding...</p>
        <br/>
        <br/>
        <br/>
~~~
        <br/>
        <br/>
        <br/>
        <p><!-- flag{No_one_cares_the_bomb_that_didn't_go_off} --></p>
        </body>
</html>
~~~
```

## flag{No_one_cares_the_bomb_that_didn't_go_off}