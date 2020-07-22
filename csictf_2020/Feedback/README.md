# Feedback:Feedback:10pts
Thanks a lot for taking part in csictf 2020!  
[https://forms.gle/a1y8SVwNcpJrjS2T7](https://forms.gle/a1y8SVwNcpJrjS2T7)  

# Solution
アンケートには別途答えるとして、flagのみの奪取を図る。
```bash
$ wget https://forms.gle/a1y8SVwNcpJrjS2T7
$ ls
a1y8SVwNcpJrjS2T7
$ grep csictf{ a1y8SVwNcpJrjS2T7
,["csictf{th4nk5_f0r_pl4y1ng}\n\nHere's a Voiceflow license for you!\n\nPlease sign up using the link given below to retrieve your subscription.\nhttps://creator.voiceflow.com/signup/promo?coupon\u003dcsictf2020",1,0,0,0]
```

## csictf{th4nk5_f0r_pl4y1ng}