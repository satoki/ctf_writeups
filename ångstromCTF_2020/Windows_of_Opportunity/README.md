# Windows of Opportunity:Rev:50pts
Clam's a windows elitist and he just can't stand seeing all of these linux challenges! So, he decided to step in and create his [own rev challenge](windows_of_opportunity.exe) with the "superior" operating system.  
Hint  
You can probably solve it just by looking at the disassembly.  

# Solution
Windowsの実行ファイルが渡される。  
メインマシンで実行したくないのでstringsを行う。
するとflagが出てくる。  
```bash
$ strings windows_of_opportunity.exe | grep actf
bactf{ok4y_m4yb3_linux_is_s7ill_b3tt3r}
```

## actf{ok4y_m4yb3_linux_is_s7ill_b3tt3r}