# out-of-click:forensics:149pts
I love playing this map but recently I noticed that some of the circles seem off. Can you help me find the **locations** of the *weird circles*?  

[beatmaps.zip](beatmaps.zip)  

# Solution
zipが配布されるので展開すると、osuファイルなどビートマップデータが出てくる。  
```bash
$ ls -al
total 5164
drwxrwxrwx 1 satoki satoki    4096 Mar  4 11:07  .
drwxrwxrwx 1 satoki satoki    4096 Mar  4 11:07  ..
-rwxrwxrwx 1 satoki satoki   66304 Feb 15 17:01  1.jpg
-rwxrwxrwx 1 satoki satoki 4745925 Feb 15 17:01 '12 - Everything will freeze.mp3'
-rwxrwxrwx 1 satoki satoki   12770 Feb 20 10:15 'UNDEAD CORPORATION - Everything will freeze (BrokenAppendix) [Out Of Click].osu'
-rwxrwxrwx 1 satoki satoki   12597 Feb 15 17:01 'UNDEAD CORPORATION - Everything will freeze (Ekoro) [Normal].osu'
-rwxrwxrwx 1 satoki satoki   56494 Feb 15 17:01 'UNDEAD CORPORATION - Everything will freeze (Ekoro) [Time Freeze].osu'
-rwxrwxrwx 1 satoki satoki  291161 Feb 15 17:01  bg.jpg
-rwxrwxrwx 1 satoki satoki   83612 Feb 15 17:01  normal-hitclap.wav
```
日時やファイル名からも`UNDEAD CORPORATION - Everything will freeze (BrokenAppendix) [Out Of Click].osu`にフラグが含まれていそうである。  
ひとまず[egg-pain-∞](../egg-pain-∞)で利用した、osuファイルのマウスの軌跡をpngにするスクリプトを一部修正して用いる。  
```bash
$ python osu2img3.py
Traceback (most recent call last):
  File "/beatmaps/osu2img3.py", line 32, in <module>
    hit_objects = parse_osu_file(file_path)
  File "/beatmaps/osu2img3.py", line 16, in parse_osu_file
    x, y = int(parts[0]), int(parts[1])
ValueError: invalid literal for int() with base 10: '111 115'
```
intへのキャスト時にエラーが出ている。  
数値が一つだけ入っているべき場所に、スペースで区切られ二つ入っているようだ。  
以下のように変更し、エラーが出る数値のみtryでキャッチして出力する。  
```python
~~~
                if len(parts) >= 3:
                    try:
                        x, y = int(parts[0]), int(parts[1])
                    except:
                        print(parts[0], parts[1])
                        continue
                    hit_objects.append((x, y))
    return hit_objects
~~~
file_path = "UNDEAD CORPORATION - Everything will freeze (BrokenAppendix) [Out Of Click].osu"
~~~
```
実行する。  
```bash
$ python osu2img3.py
111 115 117 123
66 84 77 67
95 49 53 95
109 89 95 71
48 97 84 125
```
数値がASCIIを10進数にしたものに見える。  
以下のように変換する。  
```bash
$ python
~~~
>>> text = "111 115 117 123 66 84 77 67 95 49 53 95 109 89 95 71 48 97 84 125".split(" ")
>>> "".join([chr(int(c)) for c in text])
'osu{BTMC_15_mY_G0aT}'
```
flagとなった。  

## osu{BTMC_15_mY_G0aT}