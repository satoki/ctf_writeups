# Vocaloid Heardle:Misc:325pts
Well, it’s just too usual to hide a flag in stegano, database, cipher, or server. What if we decide to sing it out instead?  

[flag.mp3](flag.mp3)　[vocaloid_heardle.py](vocaloid_heardle.py)  

# Solution
フラグを示すであろうmp3とソースが配布される。  
まずはmp3を聞くと、ボカロの曲が複数個結合されていた。  
ソースを見ると以下のようであった。  
```python
import requests
import random
import subprocess

resources = requests.get("https://sekai-world.github.io/sekai-master-db-diff/musicVocals.json").json()

def get_resource(mid):
    return random.choice([i for i in resources if i["musicId"] == mid])["assetbundleName"]

def download(mid):
    resource = get_resource(mid)
    r = requests.get(f"https://storage.sekai.best/sekai-assets/music/short/{resource}_rip/{resource}_short.mp3")
    filename = f"tracks/{mid}.mp3"
    with open(filename, "wb") as f:
        f.write(r.content)
    return mid

with open("flag.txt") as f:
    flag = f.read().strip()

assert flag.startswith("SEKAI{") and flag.endswith("}")
flag = flag[6:-1]
tracks = [download(ord(i)) for i in flag]

inputs = sum([["-i", f"tracks/{i}.mp3"] for i in tracks], [])
filters = "".join(f"[{i}:a]atrim=end=3,asetpts=PTS-STARTPTS[a{i}];" for i in range(len(tracks))) + \
          "".join(f"[a{i}]" for i in range(len(tracks))) + \
          f"concat=n={len(tracks)}:v=0:a=1[a]"

subprocess.run(["ffmpeg"] + inputs + ["-filter_complex", filters, "-map", "[a]", "flag.mp3"])
```
読み解くと、どうやらフラグの中身を一文字ずつ曲に置き換え、最後に結合しているようだ。  
`get_resource`をprintすると、どうやら曲にも複数のバージョンがあるようで、歌唱者？が変わっている。  
ただし曲は同じである。  
ここで、すべてのASCII文字を曲に置き換え、それを聴き比べ同一の曲であった場合に文字を決定することでフラグが再構成できることに気づく。  
以下のdl.pyですべてのASCII文字を置き換えた曲を`tracks`へ保存する。  
```python
import random
import string
import requests

resources = requests.get("https://sekai-world.github.io/sekai-master-db-diff/musicVocals.json").json()

def get_resource(mid):
    return random.choice([i for i in resources if i["musicId"] == mid])["assetbundleName"]

def download(mid):
    resource = get_resource(mid)
    r = requests.get(f"https://storage.sekai.best/sekai-assets/music/short/{resource}_rip/{resource}_short.mp3")
    filename = f"tracks/{mid}.mp3"
    with open(filename, "wb") as f:
        f.write(r.content)
    return mid

for c in string.printable:
    try:
        print(f"OK: {download(ord(c))}")
    except Exception as e:
        print(f"ERROR: {ord(c)}")
        print(e)
```
実行した後に、聞き比べる。  
```bash
$ python dl.py
OK: 48
OK: 49
OK: 50
OK: 51
OK: 52
ERROR: 53
Cannot choose from an empty sequence
OK: 54
OK: 55
ERROR: 56
Cannot choose from an empty sequence
OK: 57
~~~
```
どうやらフラグは次の曲であるようだ(歌詞を聞き取り「ボカロ 歌詞」などで検索すると曲名が出る)。  
```
■tracks/118.mp3
＊ハロー、プラネット。
■tracks/48.mp3
ワールドイズマイン
■tracks/67.mp3
自傷無色
■tracks/97.mp3
霽れを待つ
■tracks/108.mp3
愛されなくても君がいる
■tracks/111.mp3
カトラリー
■tracks/73.mp3
ニア
■tracks/100.mp3
ECHO
■tracks/60.mp3
悔やむと書いてミライ
■tracks/51.mp3
セカイはまだ始まってすらいない
■tracks/117.mp3
ODDS&ENDS
```
これらを文字へ直せばよい。  
```bash
$ python3 -c 'print("".join([chr(i) for i in [118,48,67,97,108,111,73,100,60,51,117]]))'
v0CaloId<3u
```
これを形式に合わせるとflagとなった。  

## SEKAI{v0CaloId<3u}