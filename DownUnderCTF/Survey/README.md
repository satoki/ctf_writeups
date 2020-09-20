# Survey:survey:10pts
The organising team have put a lot of effort and love into making DUCTF. We would really appreciate your honest feedback!  
[https://duc.tf/feedback](https://duc.tf/feedback)  

# Solution
アンケートには別途答えるとして、flagのみの奪取を図る。  
```bash
$ wget https://duc.tf/feedback
~~~
$ ls
feedback
$ grep DUCTF{ feedback
,["Thank you for playing DownUnderCTF. Your feedback is appreciated!\n\nHere is your flag: DUCTF{th4nk_y0u_f0r_p4rt1c1pating_in_DUCTF!1!1}",0,0,0,0]
```

## DUCTF{th4nk_y0u_f0r_p4rt1c1pating_in_DUCTF!1!1}