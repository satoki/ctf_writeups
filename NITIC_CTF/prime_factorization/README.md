# prime_factorization:PPC:200pts
合成数Cが与えられる。素因数分解してa_0^b_0 * a_1^b_1 * … * a_n^b_nの形にして、nitic_ctf{a_0_b_0_a_1_b_1…a_n_b_n}のがフラグとなる。この時a_iは素数、b_iは1以上の整数、aは昇順に並んでいる。  
例えばC=48の時、48=2^4*3^1より、フラグはnitic_ctf{2_4_3_1}である。  
[https://www.dropbox.com/s/ry54l4dp15g17v8/prime_factorization_1.zip?dl=0](prime_factorization_1.zip)  

# Solution
prime_factorization_1.zipを解凍すると408410100000と書かれたファイルが出てくる。  
ファイルにした理由は謎だが、問題文通り[素因数分解を試みる](http://factordb.com/index.php?query=408410100000)と以下のようになる。  
408410100000 = (2 * 3 * 5 * 7)^5 = 2^5 * 3^5 * 5^5 * 7^5  
よって、2_5_3_5_5_5_7_5になる。  

## nitic_ctf{2_5_3_5_5_5_7_5}