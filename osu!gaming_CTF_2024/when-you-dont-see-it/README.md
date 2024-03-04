# when-you-dont-see-it:web:111pts
welcome to web! there's a flag somewhere on my osu! profile...  
[https://osu.ppy.sh/users/11118671](https://osu.ppy.sh/users/11118671)  

# Solution
URLが渡される。  
アクセスするとosu!というゲームのプロフィールページのようだ。  
![site.png](site/site.png)  
何もないらしいが、ひとまずソースをgrepしてみる。  
```bash
$ curl -s 'https://osu.ppy.sh/users/11118671' | grep 'osu{' | wc
      0       0       0
$ curl -s 'https://osu.ppy.sh/users/11118671' | grep 'b3N1' | wc
      1    3907  158033
```
base64されたフラグのようなものがヒットする。  
```bash
$ curl -s 'https://osu.ppy.sh/users/11118671' | grep -o 'b3N1.* '
b3N1e29rX3Vfc2VlX21lfQ== encoded with
$ echo -n 'b3N1e29rX3Vfc2VlX21lfQ==' | base64 -d
osu{ok_u_see_me}
```
デコードするとflagであった。  

## osu{ok_u_see_me}