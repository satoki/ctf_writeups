# puni_puni:Web:80pts
近所の子供から「ぷにぷにこーどあげるね」と1枚の紙を手渡されました。見ると子供の字とは思えない正確な書体で英数字がびっしりと書き込まれています。これはいったい。そう聞こうとしましたが、紙に意識を取られた一瞬のうちにその子供はいなくなっていました。  
紙に書かれた文字列を解析し、フラグを入手してください。フラグは得られた文字列を `flag{}` で囲んで答えてください。例えば `flag` が得られた場合は `flag{flag}` と入力します。  
```
xn--q6jaaaaaa08db0x8nc9t1b8fsviei84atb4i0lc
xn--q6jaaaaa03dpd4mb3jc5rpa0g9jpk07acadc.
xn--q6jylla3va3j6c8138a8eptvb303cxv4ft3o4ue63a
xn--v8ja6aj2a3cri3ag4a2r6cx2a1rkk1272c7j4ajd4bmf0kjhg6rb.
xn--q6j6gav1a0b2e1bh1ac2cl29ad7728kdjen6cz80dju6bqexchl9gel8b.
```

# Solution
どう見てもIDNのAラベルなので[Punycode converter](https://www.punycoder.com/)で変換すると以下のようであった。  
```text
フラグは、さん、さん、ピー、ユー、エヌ、ワイ、
シー、オー、ディー、イー、よん、よん、です.
カタカナ表記は半角英小文字に、
ひらがな表記は半角数字にしたものがフラグです.
なお、読点は区切り文字なので取り除いてください.
```

## flag{33punycode44}