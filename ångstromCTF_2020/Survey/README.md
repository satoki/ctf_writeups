# Survey:Misc:5pts
Thanks for playing this CTF! Please fill out [our survey](https://forms.gle/kNXSjDzzf2jmcrrXA) so that we can improve ångstromCTF next year. This challenge does not affect time-based tiebreakers.  


# Solution
アンケートには別途答えるとして、flagのみの奪取を図る。  
```bash
$ wget https://forms.gle/kNXSjDzzf2jmcrrXA
$ ls
kNXSjDzzf2jmcrrXA
$ grep actf kNXSjDzzf2jmcrrXA
,["Thank you for filling out the survey! Your flag is actf{never_gonna_run_around_and_desert_you}.",0,0,0,0]
```

## actf{never_gonna_run_around_and_desert_you}