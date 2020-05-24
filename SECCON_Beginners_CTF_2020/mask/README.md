# mask:Reversing:62pts
The price of [mask](mask.zip-c9da034834b7b699a7897d408bcb951252ff8f56) goes down. So does the point (it's easy)!  
(SHA-1 hash: c9da034834b7b699a7897d408bcb951252ff8f56)  

# Solution
解凍するとmaskが出てくるので実行してみる。  
```bash
$ ./mask
Usage: ./mask [FLAG]
$ ./mask abcdefghijklmnopqrstuvwxyz
Putting on masks...
a`adede`a`adedepqpqtutupqp
abc`abchijkhijk`abc`abchij
Wrong FLAG. Try again.
```
アルファベットを引数にとりそれを二回置換しているようだ。  
IDAで見てもよいが、stringsで以下が見られる。  
```bash
$ strings mask
~~~
Usage: ./mask [FLAG]
Putting on masks...
atd4`qdedtUpetepqeUdaaeUeaqau
c`b bk`kj`KbababcaKbacaKiacki
Correct! Submit your FLAG.
Wrong FLAG. Try again.
~~~
```
並べてみるとよくわかる。  
U->Kは_だろう。  
```text
a`adede`a`adedepqpqtutupqp
abc`abchijkhijk`abc`abchij

abcdefghijklmnopqrstuvwxyz

atd4`qdedtUpetepqeUdaaeUeaqau
c`b bk`kj`KbababcaKbacaKiacki

ctf4b{dont_reverse_face_mask}
```
アルファベットの先頭文字からflagの単語を推測すると面倒が減る。  

## ctf4b{dont_reverse_face_mask}