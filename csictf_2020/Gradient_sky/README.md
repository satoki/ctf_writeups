# Gradient sky:Forensics:XXXpts<!--XXX-->
Gradient sky is a begginer level ctf challenge which is aimed towards rookies.  
[sky.jpg](sky.jpg)  

# Solution
sky.jpgが渡される。  
stringsする。  
```bash
$ strings sky.jpg | grep "csictf{"
csictf{j0ker_w4snt_happy}
```
flagが出てくる。  

## csictf{j0ker_w4snt_happy}