# Compare:FORENSICS:100pts
新しくUECTFのロゴを作ったよ。え？元々あったロゴと同じじゃないかって？君はまだまだ甘いなぁ。  
I made a new logo for UECTF. What, do you think it's the same as the original logo? You are still a bit naive.  

[UECTF_org.bmp](UECTF_org.bmp)　[UECTF_new.bmp](UECTF_new.bmp)  

# Solution
bmpが二つ渡される。  
問題名より比較すればよさそうなので、以下のcompare.pyで行う。  
```python
org = open("UECTF_org.bmp", "rb").read()
new = open("UECTF_new.bmp", "rb").read()

for i in range(len(org)):
    if org[i] != new[i]:
        print(chr(new[i]), end="")
```
実行する。  
```bash
$ python compare.py
UECTF{compare_two_files_byte_by_byte}
```
flagが得られた。  

## UECTF{compare_two_files_byte_by_byte}