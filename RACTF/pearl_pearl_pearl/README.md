# pearl pearl pearl:Misc:300pts
Challenge instance ready at 95.216.233.106:49960.  
pearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearlpearl  

# Solution
ncすると以下のように表示される。  
何もできそうにないが、とりあえずファイルにはき出す。  
```bash
nc 95.216.233.106 49960
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
~~~
$ nc 95.216.233.106 49960 > pearlpearlpearl.txt
^C
$ cat pearlpearlpearl.txt
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
ctf{pearlpearlpearl}
~~~
```
odで見ると、改行が混在しているようだ。  
```bash
$ od -An -c pearlpearlpearl.txt
   c   t   f   {   p   e   a   r   l   p   e   a   r   l   p   e
   a   r   l   }  \r   c   t   f   {   p   e   a   r   l   p   e
   a   r   l   p   e   a   r   l   }  \n   c   t   f   {   p   e
   a   r   l   p   e   a   r   l   p   e   a   r   l   }  \n   c
   t   f   {   p   e   a   r   l   p   e   a   r   l   p   e   a
   r   l   }  \n   c   t   f   {   p   e   a   r   l   p   e   a
   r   l   p   e   a   r   l   }  \r   c   t   f   {   p   e   a
   r   l   p   e   a   r   l   p   e   a   r   l   }  \r   c   t
   f   {   p   e   a   r   l   p   e   a   r   l   p   e   a   r
   l   }  \n   c   t   f   {   p   e   a   r   l   p   e   a   r
   l   p   e   a   r   l   }  \r   c   t   f   {   p   e   a   r
   l   p   e   a   r   l   p   e   a   r   l   }  \r   c   t   f
   {   p   e   a   r   l   p   e   a   r   l   p   e   a   r   l
   }  \n   c   t   f   {   p   e   a   r   l   p   e   a   r   l
   p   e   a   r   l   }  \n   c   t   f   {   p   e   a   r   l
   p   e   a   r   l   p   e   a   r   l   }  \r   c   t   f   {
   p   e   a   r   l   p   e   a   r   l   p   e   a   r   l   }
~~~
```
抽出してバイナリにしてみる(0と1を逆にしたものも試す必要がある)。  
```bash
$ cat pearlpearlpearl.txt | tr -d "ractf{pearl} " | tr "\r" "0" | tr "\n" "1"
0111001001100001011000110111010001100110011110110111000000110011001101000111001000110001010111110011000101101110011100110011000101100100001100110101111100110100010111110110001101101100001101000110110101111101
```
これを[バイナリからASCIIに変換](https://www.rapidtables.com/convert/number/binary-to-ascii.html)するとflagが得られる。  
ractf{p34r1_1ns1d3_4_cl4m}

## ractf{p34r1_1ns1d3_4_cl4m}