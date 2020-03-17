# Keysar:Crypto:40pts
Hey! My friend sent me a message... He said encrypted it with the key ANGSTROMCTF.  
He mumbled what cipher he used, but I think I have a clue.  
Gotta go though, I have history homework!!  
agqr{yue_stdcgciup_padas}  
Hint  
Keyed caesar, does that even exist??  

# Solution
問題名からシーザー暗号であることが分かるが、actfがagqrと置き換わっていることからアルファベットの並びをずらすだけでは不十分である。  
ANGSTROMCTFがキーであるが、Tが二つ存在するため一つ消去する(fがrに変わっている事より後ろのTが不要)。  
ANGSTROMCTFより後ろは、重複しないようアルファベットを並べる。  
```text
ANGSTROMCFBDEHIJKLPQUVWXYZ
ABCDEFGHIJKLMNOPQRSTUVWXYZ

agqr{yue_stdcgciup_padas}
actf{yum_delicious_salad}
```

## actf{yum_delicious_salad}