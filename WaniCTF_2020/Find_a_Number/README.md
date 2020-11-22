# Find a Number:Misc:pts
隠された数字を当てるとフラグが表示されます.  
数字は0以上500000以下であることが保証されています．  
nc number.wanictf.org 60000  
[number.py](number.py)  

# Solution
20回の試行で数字を当てれば良い。  
二分探索すれば500000*((1/2)^20)=0.476くらいなので一つに定まる。  
最初の時点で5分の1ほどの個数に落としておくと入力ミスにも対応できる。  
以下のように行う。  
```bash
$ nc number.wanictf.org 60000
find a number
challenge 0
input:100000
too small
try again!
challenge 1
input:^C
$ nc number.wanictf.org 60000
find a number
challenge 0
input:100000
too small
try again!
challenge 1
input:^C
$ nc number.wanictf.org 60000
find a number
challenge 0
input:100000
too big
try again!
challenge 1
input:50000
too big
try again!
challenge 2
input:25000
too big
try again!
challenge 3
input:12500
too small
try again!
challenge 4
input:18750
too small
try again!
challenge 5
input:21875
too big
try again!
challenge 6
input:20312
too big
try again!
challenge 7
input:19531
too small
try again!
challenge 8
input:19921
too big
try again!
challenge 9
input:19726
too small
try again!
challenge 10
input:19823
too big
try again!
challenge 11
input:19774
too small
try again!
challenge 12
input:19798
too small
try again!
challenge 13
input:19810
too big
try again!
challenge 14
input:19804
too big
try again!
challenge 15
input:19801
too big
try again!
challenge 16
input:19799
too small
try again!
challenge 17
input:19800
correct!!!
FLAG{b1n@ry_5e@rch_1s_v3ry_f@5t}
```
flagが得られた。  

## FLAG{b1n@ry_5e@rch_1s_v3ry_f@5t}