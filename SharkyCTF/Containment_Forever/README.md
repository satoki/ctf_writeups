# Containment Forever:Web:266pts
Hello, welcome on "Containment Forever"! There are 2 categories of posts, only the first is available, get access to the posts on the flag category to retrieve the flag.  
[containment-forever.sharkyctf.xyz](http://containment-forever.sharkyctf.xyz)  

# Solution
アクセスすると以下のようなサイトとなっている。  
Home  
[site1.png](site/site1.png)  
Confinement  
[site2.png](site/site2.png)  
Flag  
[site3.png](site/site3.png)  
Confinementページのソースは以下のようになっている。  
```html
<tr>
    <td> 5e70da94d7b1600013655bb5 </td>
    <td> <a href="/item/5e70da94d7b1600013655bb5">Confinement basics</a> </td>
    <td>Thotonox</td>
    <td>Confinement basics</td>
    <td>Tue Mar 17 2020 14:11:32 GMT+0000 (Coordinated Universal Time)</td>
</tr>

<tr>
    <td> 5e7e4f48d7b1600013655bb9 </td>
    <td> <a href="/item/5e7e4f48d7b1600013655bb9">Confined together</a> </td>
    <td>enstro</td>
    <td>Confined together</td>
    <td>Fri Mar 27 2020 19:08:56 GMT+0000 (Coordinated Universal Time)</td>
</tr>

<tr>
    <td> 5e83642bd7b1600013655bba </td>
    <td> <a href="/item/5e83642bd7b1600013655bba">Eating anything</a> </td>
    <td>DarkClown</td>
    <td>Eating anything</td>
    <td>Tue Mar 31 2020 15:39:23 GMT+0000 (Coordinated Universal Time)</td>
</tr>

<tr>
    <td> 5e8ee635d7b1600013655bbd </td>
    <td> <a href="/item/5e8ee635d7b1600013655bbd">Toilet Paper Fever</a> </td>
    <td>EverySingleOne</td>
    <td>Toilet Paper Fever</td>
    <td>Thu Apr 09 2020 09:09:09 GMT+0000 (Coordinated Universal Time)</td>
</tr>
```
/item/ObjectIdに各コンテンツのページが生成されているようである。  
[/item/~~~](site/item)  
FlagページのコンテンツにはObjectIdが存在しないためそれを推測する必要がある。  
ObjectIdに共通部分(????????d7b1600013655bb?)が存在するため、何らかの法則に基づいていると考えられる。  
Dateが怪しい。  
```text
Confinement
5e70da94d7b1600013655bb5 Tue Mar 17 2020 14:11:32 GMT+0000 (Coordinated Universal Time)
5e7e4f48d7b1600013655bb9 Fri Mar 27 2020 19:08:56 GMT+0000 (Coordinated Universal Time)
5e83642bd7b1600013655bba Tue Mar 31 2020 15:39:23 GMT+0000 (Coordinated Universal Time)
5e8ee635d7b1600013655bbd Thu Apr 09 2020 09:09:09 GMT+0000 (Coordinated Universal Time)

Flag
????????d7b1600013655bb? Sat Mar 21 2020 09:13:22 GMT+0000 (Coordinated Universal Time)
????????d7b1600013655bb? Mon Apr 13 2020 15:50:18 GMT+0000 (Coordinated Universal Time)
```
5e7e4f48 - 5e70da94を行って10進数に直してみる。  
5e7e4f48 - 5e70da94 = d74b4(881844)  
881844はMar 17 2020 14:11:32からMar 27 2020 19:08:56までの経過秒数であることがわかる。  
つまりFlagまでの時間を計算し、わかっているObjectIdの先頭8桁へ足せばよい。  
Mar 17 2020 14:11:32からMar 21 2020 09:13:22は327710秒  
5e70da94 + 5001e(327710) = 5e75dab2  
Apr 09 2020 09:09:09からApr 13 2020 15:50:18は369669秒  
5e8ee635 + 5a405(369669) = 5e948a3a  
最後の1桁は総当たりすると以下のURLが存在することがわかる。  
http://containment-forever.sharkyctf.xyz/item/5e75dab2d7b1600013655bb8  
http://containment-forever.sharkyctf.xyz/item/5e948a3ad7b1600013655bbf  
flagはそのページに分割して書かれている  
[5e75dab2d7b1600013655bb8.png](site/flag/5e75dab2d7b1600013655bb8.png)  
[5e948a3ad7b1600013655bbf.png](site/flag/5e948a3ad7b1600013655bbf.png)  

## shkCTF{IDOR_IS_ALS0_P0SSIBLE_W1TH_CUST0M_ID!_f878b1c38e20617a8fbd20d97524a515}