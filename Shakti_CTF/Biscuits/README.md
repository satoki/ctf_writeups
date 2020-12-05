# Biscuits:Web Exploitation:50pts
Ada Lovelace used to love eating french biscuits during her work  
Link: [http://34.72.245.53/Web/Biscuits/](http://34.72.245.53/Web/Biscuits/)  

# Solution
問題名から容易に想像がつく。  
URLにアクセスするまでもない。  
```bash
$ curl -s --dump-header - http://34.72.245.53/Web/Biscuits/ | grep shaktictf
Set-Cookie: THE_FLAG_IS=shaktictf%7Bc00k13s_m4k3_phr3n0l0gy%26m3sm3r15m_3asy%7D
$ curl -s --dump-header - http://34.72.245.53/Web/Biscuits/ | grep shaktictf | nkf -w --url-input
Set-Cookie: THE_FLAG_IS=shaktictf{c00k13s_m4k3_phr3n0l0gy&m3sm3r15m_3asy}
```
flagがクッキーに入っていた。  

## shaktictf{c00k13s_m4k3_phr3n0l0gy&m3sm3r15m_3asy}