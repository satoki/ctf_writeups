# guess:misc:250pts
CTFで一番大事な能力はguessingだって聞きました。  
`nc chall.live.ctf.tsg.ne.jp 21234`  
[guess.tar.gz](guess.tar.gz)  

# Solution
接続先とソースが配布されている。  
繋ぐと以下のようなパスワードを当てるゲームが動いていた。  
```bash
$ nc chall.live.ctf.tsg.ne.jp 21234
guess password:Satoki
guess password:Got:Satoki
Expected:2eu7Itu723akpNlUFe0
```
guessすれば解けるようだ。  
できるわけがない。  
遊んでいると奇妙な点に気づく。  
```bash
$ nc chall.live.ctf.tsg.ne.jp 21234
guess password:AAAAA
guess password:Got:AAAAA
BBBBB
guess password:Got:BBBBB
Expected:7V0nVBi15jjdKrn7HHd
Expected:wY0bbc7fnDLOktij4Ie
CCCCC
guess password:Got:CCCCC
Expected:W9M9MOjLzkSGAleW1po
```
入力と応答の順番がかみ合っていないような結果である。  
/dev/random由来の乱数生成が間に合っていないのかと考え、ひとまず大量の改行や空文字を高速で送り込んでみる方針をとる。  
改行はキーボードのエンターを押し続ければよい。  
```bash
$ nc chall.live.ctf.tsg.ne.jp 21234
guess password:
guess password:Got:
Expected:DwIk4xEvzP5K1RKxbP0



guess password:

Got:



guess password:guess password:Got:
Got:
~~~
guess password:guess password:guess password:Got:
Got:
Got:
Expected:sRDiuzg46zm1ggvY6yQ
Expected:
you win!
TSGLIVE{ThI5_1S_n0T_UMa_MUsUMe_pR3TTy_DerbY_rACe}
```
flagが得られた。  
ソースを読むとraceなので納得である。  
実質guessしたので1st bloodだった。  

## TSGLIVE{ThI5_1S_n0T_UMa_MUsUMe_pR3TTy_DerbY_rACe}