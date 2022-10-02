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