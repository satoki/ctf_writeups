# Discord2:FORENSICS:323pts
前に思いついたフラグ送信しようとして止めたんだけど、やっぱりあれが良かったなぁ… でもちゃんと思い出せないなぁ。このフォルダにはキャッシュとかも残ってるし、どこかに編集履歴みたいなの残ってないかなぁ…  
I tried to send to a friend the flag I thought of before and stopped, but I still liked that one... But I can't remember it properly. I'm sure there's a cache or something in this folder, and I'm wondering if there's some kind of edit history somewhere...  

[discord2.zip](discord2.zip)  

# Solution
[Discord 1](../Discord_1)に似ているが、問題名にスペースが入っていない。  
編集履歴みたいなものが残っているそうで、おそらく文字列そのままであろうと予測できる。  
Discord 1では画像を探したが、今回はすべてstringしたのちgrepすれば出てきそうだ。  
```bash
$ unzip discord2.zip
Archive:  discord2.zip
~~~
$ strings discord2/*/*/* | grep UECTF
strings: Warning: 'discord2/Code Cache/js/index-dir' is a directory
strings: Warning: 'discord2/Code Cache/wasm/index-dir' is a directory
{"_state":{"1039033893849944084":{"1039070178207617074":{"0":{"timestamp":1667806462142,"draft":"UECTF{Y0U_C4N_S33_Y0UR_DRAFT}"}}}},"_version":2}
```
flagが見つかった。  

## UECTF{Y0U_C4N_S33_Y0UR_DRAFT}