# Quarantine - Hidden information:Web:150pts
Challenge instance ready at 95.216.233.106:57153.  
We think there's a file they don't want people to see hidden somewhere! See if you can find it, it's gotta be on their webapp somewhere...  

# Solution
アクセスするとSign inとSign upがあるが、Sign upは現在停止しているようだ。  
RAQE  
[site.png](site/site.png)  
隠したいファイルがあるとのことなので、クローラーをブロックしていると考えられる。  
robots.txtを見に行くと以下のようであった。  
```text:robots.txt
User-Agent: *
Disallow: /admin-stash
```
http://95.216.233.106:57153/admin-stash にアクセスするとflagが表示された。  
flag  
[flag.png](site/flag.png)  

## ractf{1m_n0t_4_r0b0T}