# Mirage:Misc:100pts
"Your eyes can deceive you; don't trust them."  
-- Obi-Wan Kenobi  
[https://mirage.hexionteam.com](https://mirage.hexionteam.com)  

# Solution
URLにアクセスすると次のようなページが開く。  
[site.png](site/site.png)  
画像がflagの換字式暗号文であることは容易に想像ができるが、総当たりするのは骨が折れる。  
入力欄に文字を入力してみると以下のように変換された。  
```text
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}
dBFS4f}jZE5gRsAKOplm20xt8hwcevoyGz1TJ{VDMQ39iquC7WXN_HLYUaPkr6Ibn
```
dec.pyで復号してやる。  
```python:dec.py
inp = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"
outp = "dBFS4f}jZE5gRsAKOplm20xt8hwcevoyGz1TJ{VDMQ39iquC7WXN_HLYUaPkr6Ibn"
text = "j4teqybvAskIE2S}4IdIc_M5IB8IHmlIF_0Ypn"

flag = []
for i in range(len(text)):
	for j in range(len(outp)):
		if text[i] == outp[j]:
			flag.append(inp[j])

print("".join(flag))
```

## hexCTF{Don7_judge_a_B0Ok_by_1ts_c0v3r}