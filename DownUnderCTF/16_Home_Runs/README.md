# 16 Home Runs:misc:100pts
How does this string relate to baseball in anyway? What even is baseball? And how does this relate to Cyber Security? ¯(ツ)/¯  
RFVDVEZ7MTZfaDBtM19ydW41X20zNG41X3J1bm4xbjZfcDQ1N182NF9iNDUzNX0=  

# Solution
何を言っているかわからんが、base64するとフラグが出てきた。  
```bash
$ python
>>> import base64
>>> text = "RFVDVEZ7MTZfaDBtM19ydW41X20zNG41X3J1bm4xbjZfcDQ1N182NF9iNDUzNX0="
>>> print(base64.b64decode(text))
b'DUCTF{16_h0m3_run5_m34n5_runn1n6_p457_64_b4535}'
```
なんじゃこりゃ。  

## DUCTF{16_h0m3_run5_m34n5_runn1n6_p457_64_b4535}