# Spentalkux:Misc:300pts
Spentalkux 🐍📦

# Solution
とんでもない面白問題文だ。  
Spentalkuxでググると以下がヒットする。  
[site.png](image.png)  
[https://pypi.org/project/spentalkux/](https://pypi.org/project/spentalkux/)  
最新版を実行すると以下のようであった。  
```bash
$ python __init__13.37.py
Hello.
Can I help you?
Oh, you're looking for something to do with *that*.
My creator left this behind but, I wonder what the key is? I don't know, but if I did I would say it's about 10 characters.
Enjoy this.
Ztpyh, Iq iir'jt vrtdtxa qzxw lhu'go gxfpkrw tz pckv bc ybtevy... *ffiieyano*. New cikm sekab gu xux cskfiwckr bs zfyo si lgmpd://zupltfvg.czw/lxo/QGvM0sa6
Goodbye now.
That's your cue to leave, bro
Exit stage left, pal
OFF YOU POP.
You know what I haven't got time for this
Forking and executing rm -rf.
```
暗号文がある。  
ヴィジュネル暗号だとメンバーから教えてもらった。  
[ヴィジュネル（Vigenere）暗号](https://linesegment.web.fc2.com/application/cipher/Vigenere.html)で暗号鍵Spentalkuxで復号する。  
```text
暗号文：
Ztpyh, Iq iir'jt vrtdtxa qzxw lhu'go gxfpkrw tz pckv bc ybtevy... *ffiieyano*. New cikm sekab gu xux cskfiwckr bs zfyo si lgmpd://zupltfvg.czw/lxo/QGvM0sa6
復号化：
Hello, If you're reading this you've managed to find my little... *interface*. The next stage of the challenge is over at https://pastebin.com/raw/BCiT0sp6
```
[https://pastebin.com/raw/BCiT0sp6](https://pastebin.com/raw/BCiT0sp6)にアクセスすると謎のHexが手に入るのでファイルに書き出すとpngであることがわかる。  
[Hexadecimal -> file (binary)](https://tomeko.net/online_tools/hex_to_file.php)が便利。  
画像にバイナリ(01011111 01101000 01100101 01110010 01110010 01101001 01101110 01100111)が書いてあるのでASCIIにして読むと、_herringである。  
red herringで注意をそらすといった意味があるのでハズレらしい。  
しかしSpentalkuxには前のバージョンがあるようだ。  
実行すると以下になる。  
```bash
$ python __init__0.9.py
Urgh. Not you again.
Fine. I'll tell you more.
...
But, being the chaotic evil I am, I'm not giving it to you in plaintext.
Enjoy this.
JA2HGSKBJI4DSZ2WGRAS6KZRLJKVEYKFJFAWSOCTNNTFCKZRF5HTGZRXJV2EKQTGJVTXUOLSIMXWI2KYNVEUCNLIKN5HK3RTJBHGIQTCM5RHIVSQGJ3C6MRLJRXXOTJYGM3XORSIJN4FUYTNIU4XAULGONGE6YLJJRAUYODLOZEWWNCNIJWWCMJXOVTEQULCJFFEGWDPK5HFUWSLI5IFOQRVKFWGU5SYJF2VQT3NNUYFGZ2MNF4EU5ZYJBJEGOCUMJWXUN3YGVSUS43QPFYGCWSIKNLWE2RYMNAWQZDKNRUTEV2VNNJDC43WGJSFU3LXLBUFU3CENZEWGQ3MGBDXS4SGLA3GMS3LIJCUEVCCONYSWOLVLEZEKY3VM4ZFEZRQPB2GCSTMJZSFSSTVPBVFAOLLMNSDCTCPK4XWMUKYORRDC43EGNTFGVCHLBDFI6BTKVVGMR2GPA3HKSSHNJSUSQKBIE
This is the part where you *leave*, bro.
Look, if you don't get outta here soon ima run rm -rf on ya
I don't want you here. GO AWAY.
Leave me alone now.
GOODBYE!
I used to want you dead but...
now I only want you gone.
```
ちなみにここまで、すでにチームメンバーがやっていた。  
マジかしこい。  
Base系の暗号化であるように見える。  
Base32を試すと、Base64が出てくる。  
```text
Base32 Decode
H4sIAJ89gV4A/+1ZURaEIAi8SkfQ+1/O3f7MtEBfMgz9rC/diXmIA5hSzun3HNdBbgbtVP2v/2+LowM837wFHKxZbmE9pQfsLOaiLAL8kvIk4MBma17ufHQbIJCXoWNZZKGPWB5QljvXIuXOmm0SgLixJw8HRC8Tbmz7x5eIspypaZHSWbj8cAhdjli2WUkR1sv2dZmwXhZlDnIcCl0GyrFX6fKkBEBTBsq+9uY2Ecug2Rf0xtaJlNdYJuxjP9kcd1LOW/fQXtb1sd3fSTGXFTx3UjfGFx6uJGjeIAAA
```
[Base64をデコードする](https://base64.guru/converter/decode/file)とgzipファイルのようだ(Base64_Decode.gz)。  
展開するとASCIIでバイナリ(Base64_Decode.txt)が記述されている。  
バイナリをさらにASCIIにするとまたASCIIで記述されたバイナリが出てくる(Base64_Decode2.txt)のでもう一度ASCIIにすると以下のHexが出てくる。  
```text
45 61 60 49 22 41 70 5b 36 74 32 30 3a 57 70 30 65 64 60 2d 3f 53 51 47 3f 31 4e 49 28 61 40 6c 24 3e 74
```
HexをさらにASCIIにすると以下になる。  
```text
Ea`I"Ap[6t20:Wp0ed`-?SQG?1NI(a@l$>t
```
Base85をデコードするとflagが得られた。  

## ractf{My5t3r10u5_1nt3rf4c3?}