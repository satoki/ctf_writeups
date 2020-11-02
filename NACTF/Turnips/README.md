# Turnips:Forensics:100pts
Dr. J loves his ch0nky turnips, can you find his ch0nky flag?  
[turnip-for-what.jpg](turnip-for-what.jpg)  

# Solution
turnip-for-what.jpgが渡される。  
```bash
$ strings turnip-for-what.jpg | grep nactf
nactf{turn1p_f0r_h3x_f3j52}
```
気がついたらターミナルにflagが出ていた。  

## nactf{turn1p_f0r_h3x_f3j52}