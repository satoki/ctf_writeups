# Autorev, Assemble!:Rev:125pts
Clam was trying to make a neural network to automatically do reverse engineering for him, but he made a typo and the neural net ended up making a reverse engineering challenge instead of solving one! Can you [get the flag?](autorev_assemble)  
Find it on the shell server at /problems/2020/autorev_assemble/ or over tcp at nc shell.actf.co 20203.  
Hint  
Don't do this by hand.  

# Solution
はじめにobjdumpを行う(autorev_assemble.txt)。  
main内の入力後の部分に注目すると以下のようになっている。  
```asm
~~~
  4079c7:	e8 b4 8a ff ff       	callq  400480 <fgets@plt>
  4079cc:	48 8d 3d 8d b6 20 00 	lea    0x20b68d(%rip),%rdi        # 613060 <z>
  4079d3:	e8 5c b8 ff ff       	callq  403234 <f992>
  4079d8:	85 c0                	test   %eax,%eax
  4079da:	0f 84 7a 0f 00 00    	je     40895a <main+0xfe9>
  4079e0:	48 8d 3d 79 b6 20 00 	lea    0x20b679(%rip),%rdi        # 613060 <z>
  4079e7:	e8 85 c9 ff ff       	callq  404371 <f268>
  4079ec:	85 c0                	test   %eax,%eax
  4079ee:	0f 84 66 0f 00 00    	je     40895a <main+0xfe9>
  4079f4:	48 8d 3d 65 b6 20 00 	lea    0x20b665(%rip),%rdi        # 613060 <z>
  4079fb:	e8 f4 97 ff ff       	callq  4011f4 <f723>
~~~
```
複数のfXXXの結果により、終了しているようだ。  
最初のf992は以下のようになっている。  
```asm
~~~
0000000000403234 <f992>:
  403234:	55                   	push   %rbp
  403235:	48 89 e5             	mov    %rsp,%rbp
  403238:	48 89 7d f8          	mov    %rdi,-0x8(%rbp)
  40323c:	48 8b 45 f8          	mov    -0x8(%rbp),%rax
  403240:	48 83 c0 62          	add    $0x62,%rax
  403244:	0f b6 00             	movzbl (%rax),%eax
  403247:	3c 30                	cmp    $0x30,%al
  403249:	0f 94 c0             	sete   %al
  40324c:	0f b6 c0             	movzbl %al,%eax
  40324f:	5d                   	pop    %rbp
  403250:	c3                   	retq   
~~~
```
受け付けた入力値の0x62文字目が0x30であるかチェックしている。  
この入力がflagだと推測できる。  
fXXXは大量に存在するため、自動化が必須である。  
以下のコードでmainから呼ばれているfXXXを順番に集め、その文字を正しい順番に配置する。  
```python:main_f.py
import re

f = open("autorev_assemble.txt")
text = f.read()

fxxx = []
for s in re.finditer("callq.*?<(?P<fn>f[0-9]*?)>", text):
    fxxx.append(s.group("fn"))
#print(len(fxxx))
table = []
for t in re.finditer("<f[0-9](.|\s)*?retq", text):
    u = t.group()
    fn = re.match("<(?P<fn>f[0-9]*?)>", u)
    fi = fn.group("fn")
    pos = re.search("add(.|\s)*?0x(?P<pos>.*?),", u)
    if pos != None:
        se = pos.group("pos")
    else:
        se = "0"
    cha = re.search("cmp(.|\s)*?0x(?P<cha>.*?),", u)
    if cha != None:
        th = cha.group("cha")
    else:
        th = "0"
    table.append([fi, int(se, 16), int(th, 16)])
flag = ['@'] * len(fxxx)
for i in range(len(fxxx)):
    for j in range(len(table)):
        if fxxx[i] == table[j][0]:
            flag[table[j][1]] = chr(table[j][2])
print("".join(flag))

f.close()
```
結果は次のようになる。  
```text:出力
_lockchain big data solutions now with added machine learning. Enjoy! I sincerely hope you actf{wr0t3_4_pr0gr4m_t0_h3lp_y0u_w1th@th1s_df93171eb49e21a3a436e186bc68a5b2d8ed} instead of doing it by hand.
```
@が表示されている部分がうまく配置できていないのでgdbで解析するとflagが得られる(総当たりでもよいし、見た目で_とわかる)。

## actf{wr0t3_4_pr0gr4m_t0_h3lp_y0u_w1th_th1s_df93171eb49e21a3a436e186bc68a5b2d8ed}