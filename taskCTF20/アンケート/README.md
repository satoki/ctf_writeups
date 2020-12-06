# アンケート:Misc:0pts
お疲れ様でした！  
振り返りのために, 今回のCTFに関する簡単なアンケートにご協力ください。  
なお, この問題は0点問題なので, 回答は必須ではありません。  
[https://forms.gle/SsC9qpdy61JSUJHQ7](https://forms.gle/SsC9qpdy61JSUJHQ7)  

# Solution
アンケートには後に回答する。  
フォームから以下のようにflagを奪取する。  
```bash
$ wget -q -O - https://forms.gle/SsC9qpdy61JSUJHQ7 | grep taskctf
,["taskctf{Th4nk_u_f0r_pl4ying!}",1,0,0,0]
```
flagが得られた。  

## taskctf{Th4nk_u_f0r_pl4ying!}