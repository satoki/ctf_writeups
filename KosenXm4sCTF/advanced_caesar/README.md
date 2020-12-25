# advanced_caesar:Crypto:94pts
超すごい暗号作った！ｗ  
[encrypted_flag.txt](encrypted_flag.txt)  

# Solution
配布されたファイルには、以下の記述があった。  
```text:encrypted_flag.txt
xn4u{fejyhzwyjazwzqkszurwhyqaop}
```
rotのようだが、`xm4s`が`xn4u`になっていることから、一文字ずつズレているようである。  
以下のrotn.pyで復号する。  
```python:rotn.py
text = "xn4u{fejyhzwyjazwzqkszurwhyqaop}"
n = 26

for i in text:
    if n <= 0:
        n = 26
    if not i in "4{}":
        i = chr((ord(i) - ord('a') + n) % 26 + ord('a'))
        n -= 1
    print(i, end="")
print()
```
実行する。  
```bash
$ python rotn.py
xm4s{caesarnoyomikatagawakarann}
```
flagが得られた。  

## xm4s{caesarnoyomikatagawakarann}