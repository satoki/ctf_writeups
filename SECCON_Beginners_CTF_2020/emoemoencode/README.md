# emoemoencode:Misc:53pts
Do you know emo-emo-encode?  
[emoemoencode.txt](emoemoencode.txt-2586093c6d0bf61e0babf4d142c2418fb243b188)  

# Solution
txtファイルの中には🍣🍴🍦🌴🍢🍻🍳🍴🍥🍧🍡🍮🌰🍧🍲🍡🍰🍨🍹🍟🍢🍹🍟🍥🍭🌰🌰🌰🌰🌰🌰🍪🍩🍽と書かれていた。  
絵文字でエンコードされているようだが、ctf4bから始まることがわかっているので最初の二文字の差をとって確認する。  
U+1F363とU+1F374の差はcとtの差と一致していることでフラグをシフトしたものに間違いない。  
以下のコードでデコードする。  
```python:emoemodecode.py
emoemo = "🍣🍴🍦🌴🍢🍻🍳🍴🍥🍧🍡🍮🌰🍧🍲🍡🍰🍨🍹🍟🍢🍹🍟🍥🍭🌰🌰🌰🌰🌰🌰🍪🍩🍽"

for c in emoemo:
    print(chr(ord(c)-0x1f300), end="")
print()
```

## ctf4b{stegan0graphy_by_em000000ji}