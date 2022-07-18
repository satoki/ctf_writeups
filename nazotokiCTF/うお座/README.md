# うお座:Misc - Water elements:34pts
みずがめ座からてんびん座に向かうとき、ひみつの鍵が手に入るだろう。水の中に浮かぶ真実を見定めよ。  
[password.enc](password.enc)　[encrypt-pisces-new.zip](encrypt-pisces-new.zip)  

Hint  
みずがめ座からてんびん座に向かうとき…ヘッダー情報に記録されるものはなんでしょうか？  
Hint  
どうやらリファラーの情報にaquariusが含まれた状態でてんびん座のサイトにアクセスすると鍵が手に入りそうです。書き換えられないでしょうか？  
やり方がわからない人は「リファラー　書き換え」とかでぐぐると良いかもしれません。  
Hint  
ひみつの鍵は手に入りましたか？その鍵を使ってpassword.encを復号してみましょう。うまくいけばzipのパスワードが手に入るはずです。  
やり方がわからなければ「openssl　復号　秘密鍵」とかでぐぐってね。  
Hint  
そろそろ目が疲れてきたころかと思って涼し気な画像をご用意しました。ちょっと休憩してぼんやり眺めてみてはいかがでしょうか。  
もしあなたが若者なら、年上の人に見せてみるとピンとくる人がいるかもしれません。  

# Solution
password.encとencrypt-pisces-new.zipの二つが配られる。  
encrypt-pisces-new.zipはパスワードがかけられており、password.encも暗号化されている。  
問題文に`みずがめ座からてんびん座に向かうとき、ひみつの鍵が手に入るだろう。`とあるが、ともにWeb問である。  
つまりみずがめ座のサイトからてんびん座のサイトへ移動(Refererをうまく設定する)すれば良いようだ。  
以下のとおり行う。  
```bash
$ curl -H "Referer: https://aquarius.ctf.nazotoki.tech" https://libra.ctf.nazotoki.tech
~~~
            <h2 class="heading--title">Libra</h2>
            <h6>リクエストヘッダー情報</h6>
            <p>
                フラグは<code>stardustChrome</code>という特殊なブラウザでしか閲覧できません。
            </p>
            <p>
                X-Forwarded-For:■■■.■■■.■■■.■■■<br>X-Forwarded-Proto:https<br>X-Forwarded-Port:443<br>Host:libra.ctf.nazotoki.tech<br>X-Amzn-Trace-Id:Root=1-62d40da2-3906d1d60aece3a202851eb7<br>user-agent:curl/7.81.0<br>accept:*/*<br><br />遠いところをよくおいでくださいました。ひみつの鍵を差し上げます。
<pre>-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAunVG5a8SbXgsayNWhd4f9FYsWb8z57P2Ql8Yq+fQgq0Y2xcH
/HgHO0vZrgSbjFLxnpx4D9arOtvGdn06GLZcL3eU32jPvqVh8QhqmaQ8bdUDlEp8
yt45DMoleYflw8c9q2dDsRjLUoE2qhtMm2xR8B9U+mRq+vVgEJdvNMgmn+XtsmRx
A41n3nHTfTcOznZaNRxyAqZjooDOuUoVBStJVUqbd4a3EzMCBbdAzyQ2VdQEigT0
PVstPiMI0draaO9oKlZkfuGkJJ3Ftn8+A4cjIG8ycihsGqfEMSVUpLmUI+Etb0+C
3iD+B7P25v0CDNdD2odWIRipjdE8TmuTA+AsuQIDAQABAoIBAQCBCSw5Q4EzNNk4
g8oa9m+SvhgPO90F2mrv37PJM7H+3R+4byXduIr4pDNO1G15HOWNaKdF/r+dCf88
fMk51OnTB6SFP5mVTAqNrc9n6FrRf3rsoufd1RASI8rvYfbGGBo7hkk4Q/phbH6S
FjZb0QibbnN2nQvUBP+oO8R/+IuSV3NgxvtQ3CggRnqTiwx99kHO3gEXJVHozq09
mceaWIQeT6jAf5nMsNKl2YlBxomMkeXZ8jEcCJQcAPuHJjZ2SJmLpbADIffg/c95
oaLejnoEWUflnN/QPw7shHE2F50uKyEYAh5uNCjVHRQE15jUOQZBr5aLMtpyCkfJ
3bPrzFcBAoGBAOyEMyBBwAh2Kuk+QS9OCsFcxjTQPV/jkHnk2nU8I7xrO0MqONOL
/ily+GcbTrY4bx8zkIKuYwEAp/5Mybd+C/kRsjeSGZVrNxNDNG32JYTn49Z1miKv
jNMGUJsfOoKI6G1gKnI3j5WlP2E+xXtQkJUMwqj5vdafCTVJhWrucFyxAoGBAMnR
ave7rOChNxVEoS7YmwMUSEk/PlM4MLkv7WkOPdNATxZ2u5fj8RrHfI4pGt//QXUX
pI0dE6Y8ndM24YhynvqGYr8cyygBj+BpMZFXSFmf2ozRTawFbo2IgqqsZ6AszQVb
EUuq5k5mx5Mg+ilMMzTmxjL4AD5GRy/2ofYK5DKJAoGACdhW6HjULYX9s0fMHtP4
zqO1/GzOoTcvxGMqVMb0FdvA08LmKqghJEiM3n3cgOlIdtwGn+nyZRBJ7eP0YZb1
mKCL8pQ6TGXyHPMnM4yTczzT1xF+IQN9sSsKH+rk3JomUqc2HRsC9w+x27JpNgDc
g9fMIoyCwnRMRdORoinas4ECgYAausnYFdtHxRJulrBia/3b4ovQZ7fxfbe2T0q6
Z1B48kOHTiJ6c44zZchxa7BLips4zvDUX82CbvTYTKSCVewIclQRy9Z8bfiIWGZg
QZcrh6iCjhYjenSx+iqUQFFZPZXJ583an7/xElvMeMmpPpZpo0cM6RvfI5+6EohQ
9hBTQQKBgQCBiu+qiElJXJUTrwr3XESHUEsCPz27VWViYlj/n6GsY80QSf4Y1F0d
ynDDCJ4zE0FL1WfFFGMqaE86wvQZwvv9NCqSkpxhfbYhf/lKUmyNIyqoQYkV7kAK
NjQ0gdNlw4NLioSXny6/0k5G4OIzwh8QNf38sZGKhm7FMVQ4G8r1Yw==
-----END RSA PRIVATE KEY-----</pre>
                                    </p>
            <a href="/" onclick="window.location.reload();">再読み込み</a>
~~~
```
秘密鍵が手に入ったので、[CyberChef](https://gchq.github.io/CyberChef/)でpassword.encを復号する。  
![cyberchef.png](images/cyberchef.png)  
`The password for the zip is "fomalhaut".`が得られる。  
zipのパスワードは`fomalhaut`のようなので解凍する(当初は配布されたzipのパスワードが間違っており時間を溶かした)。  
```bash
$ unzip -P fomalhaut encrypt-pisces-new.zip
Archive:  encrypt-pisces-new.zip
  inflating: pisces.jpg
```
すると画像が現れる。  
![pisces.jpg](pisces.jpg)  
一見すると何もないので、[Stegsolve](http://www.caesum.com/handbook/Stegsolve.jar)を用いる。  
![stegsolve.png](images/stegsolve.png)  
Stereogram Solver機能を使うと、`ケッパク`との文字が浮かび上がった。  
これがflagであった。  

## ケッパク