# Feedback:Misc:1pts
Thank you for playing bi0sCTF 2024. We would highly appreciate any feedback you have regarding this edition of the CTF.  
[https://docs.google.com/forms/d/e/1FAIpQLSeD65HB4DPvSTo_GkpWDLGam7hHN4v0a7CFFz2mvtTDJgDAVA/viewform?usp=sharing](https://docs.google.com/forms/d/e/1FAIpQLSeD65HB4DPvSTo_GkpWDLGam7hHN4v0a7CFFz2mvtTDJgDAVA/viewform?usp=sharing)  

# Solution
アンケートのようだ。  
いつもの通りcurlでフラグを奪う。  
```bash
$ curl -s 'https://docs.google.com/forms/d/e/1FAIpQLSeD65HB4DPvSTo_GkpWDLGam7hHN4v0a7CFFz2mvtTDJgDAVA/viewform?usp=sharing' | grep -o 'bi0sctf{.*}'
bi0sctf{th4nk5_f0r_pl4y1ng_bi0sctf2024}
```
フォレンジックだけ無意味なISTへの時間変換をさせられ、フラグをいくつか試す必要があるなど最悪な体験だった。  

## bi0sctf{th4nk5_f0r_pl4y1ng_bi0sctf2024}