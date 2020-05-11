# Logs In ! Part 1:Web:155pts
Data printed on one of our dev application has been altered, after questioning the team responsible of its development, it doesn't seem to be their doing. The H4XX0R that changed the front seems to be a meme fan and enjoyed setting the front.  
We've already closed the RCE he used, there is a sensitive database running behind it. If anyone could access it we'll be in trouble. Can you please audit this version of the application and tell us if you find anything compromising, you shouldn't be able to find the admin session.  
The application is hosted at [logs_in](http://logs_in.sharkyctf.xyz/)  

# Solution
RCEされてフロントを変更されたようだ。  
Home  
[site1.png](site/site1.png)  
サイトにアクセスするとSymfonyの設定が開けることがわかる。  
http://logs_in.sharkyctf.xyz/_profiler/empty/search/results?limit=10 でログが見えるようだ。  
Profile Search  
[site2.png](site/site2.png)  
limitの値を大きくしログの表示数を増やすと、CTF開始前である2020/05/08にhttp://logs_in-nginx/e48e13207341b6bffb7fb1622282247b/debug なるGETがある。  
http://logs_in.sharkyctf.xyz/e48e13207341b6bffb7fb1622282247b/debug にアクセスしてみるとflagが手に入る。
[flag.png](site/flag.png)  

## shkCTF{0h_N0_Y0U_H4V3_4N_0P3N_SYNF0NY_D3V_M0D3_1787a60ce7970e2273f7df8d11618475}