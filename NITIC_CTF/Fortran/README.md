# Fortran:Reversing:200pts
[https://www.dropbox.com/s/jc1gqk0rvmv94d3/fortran.zip?dl=0](fortran.zip)  

# Solution
ジャンルはstrings。  
```bash
$ ls
problem  problem.exe
$ strings * | grep "nitic_ctf{"
nitic_ctf{No_FORTRAN_Yes_Fortran}
```
ちなみにこれはexeからのもので、problemを見てると時間が溶ける。  

## nitic_ctf{No_FORTRAN_Yes_Fortran}