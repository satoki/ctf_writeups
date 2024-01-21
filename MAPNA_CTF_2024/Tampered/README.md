# Tampered:Forensics:pts
Our MAPNA **[flags](tampered_6fb083f974d05371cef19c0e585ba5c59da23aa8.txz)** repository was compromised, with attackers introducing one invalid flag. Can you identify the counterfeit flag?  
**Note:** Forgot the flag format in the rules pages, just find the tampered one.  
**You are not allowed to brute-force the flag in scoreboard, this will result in your team being blocked.**  

# Solution
ファイルが配布される。  
中には大量のフラグが含まれている。  
```
$ head flags.txt
MAPNA{X9JMN#CO4W1YrE%8%!ULanDXl$Yy=H>PLe5pJ*pk}
MAPNA{m+0ORa'p2TIqjBH3On+SbjjG1w*?p&hWMlW8D[cU}
MAPNA{6;,//u%ED<<K)Vlq</NCcsgM?nwdKwE8O4p?/>wq}
MAPNA{H9q(/3oNRmp4I(UZ9GIf'4*=Nz&60dkUJ?ymR7M@}
MAPNA{EprAuVKi\v<'.ACK>ier"Fgs(5o3)ZdUTdI7K66@}
MAPNA{lQE?RV0s7tuz6s3IQCx=E"i,YCxo;/N%uS=WpQ.L}
MAPNA{AfHAr6L++57S3;8hQTfO9,ppVoNn*VRxh(8Y3QM\}
MAPNA{.Rb3,:d2JJ4Sii%C9>lmGWA8O+Oni%zl3bS6I):v}
MAPNA{Ps?u1UgN+[d-d.V(pgXOiP6Z%gX(tq)2m=4K,e/t}
MAPNA{pB($5JY\jhj'1G??DtxsAAxQeg!y7&llu&[O2wqg}
```
攻撃者が導入した偽フラグを探せとのことらしい。  
チームメンバーが改行の文字などが違うのではないかと言っていた。  
試してみる。  
```bash
$ xxd flags.txt | head
00000000: 4d41 504e 417b 5839 4a4d 4e23 434f 3457  MAPNA{X9JMN#CO4W
00000010: 3159 7245 2538 2521 554c 616e 4458 6c24  1YrE%8%!ULanDXl$
00000020: 5979 3d48 3e50 4c65 3570 4a2a 706b 7d0d  Yy=H>PLe5pJ*pk}.
00000030: 0d0a 4d41 504e 417b 6d2b 304f 5261 2770  ..MAPNA{m+0ORa'p
00000040: 3254 4971 6a42 4833 4f6e 2b53 626a 6a47  2TIqjBH3On+SbjjG
00000050: 3177 2a3f 7026 6857 4d6c 5738 445b 6355  1w*?p&hWMlW8D[cU
00000060: 7d0d 0d0a 4d41 504e 417b 363b 2c2f 2f75  }...MAPNA{6;,//u
00000070: 2545 443c 3c4b 2956 6c71 3c2f 4e43 6373  %ED<<K)Vlq</NCcs
00000080: 674d 3f6e 7764 4b77 4538 4f34 703f 2f3e  gM?nwdKwE8O4p?/>
00000090: 7771 7d0d 0d0a 4d41 504e 417b 4839 7128  wq}...MAPNA{H9q(
$ xxd flags.txt | grep '0a0d'
0000a0d0: 3475 346d 2f73 4d4e 2e21 6a69 3270 6e72  4u4m/sMN.!ji2pnr
00077840: 4948 4823 3654 4c2b 7576 7d0d 0a0d 4d41  IHH#6TL+uv}...MA
000a0d00: 4855 2428 6747 4c4a 7d0d 0d0a 4d41 504e  HU$(gGLJ}...MAPN
000a0d10: 417b 5855 3b39 472e 6963 6c59 7a58 673d  A{XU;9G.iclYzXg=
000a0d20: 556c 3630 3a69 4675 4970 4947 2b6b 793c  Ul60:iFuIpIG+ky<
000a0d30: 5275 4f4c 222a 247a 4d28 7d0d 0d0a 4d41  RuOL"*$zM(}...MA
000a0d40: 504e 417b 5232 6954 7446 513d 6d44 4f4d  PNA{R2iTtFQ=mDOM
000a0d50: 5828 556c 6676 264a 2676 7836 4e30 2172  X(Ulfv&J&vx6N0!r
000a0d60: 5c42 2d31 3456 3c33 4752 632e 7d0d 0d0a  \B-14V<3GRc.}...
000a0d70: 4d41 504e 417b 4c21 6e32 352b 5c3f 5466  MAPNA{L!n25+\?Tf
000a0d80: 7931 4e62 3f3d 6a37 373d 4664 2477 365a  y1Nb?=j77=Fd$w6Z
000a0d90: 4749 5b2d 4036 6a2e 426d 5a56 3040 7d0d  GI[-@6j.BmZV0@}.
000a0da0: 0d0a 4d41 504e 417b 2228 2b29 276e 445a  ..MAPNA{"(+)'nDZ
000a0db0: 6a44 213c 236f 6a77 565c 5778 2635 5024  jD!<#ojwV\Wx&5P$
000a0dc0: 2933 273a 583b 2333 6653 385b 2f28 4e66  )3':X;#3fS8[/(Nf
000a0dd0: 7d0d 0d0a 4d41 504e 417b 2d6f 2859 3f26  }...MAPNA{-o(Y?&
000a0de0: 6144 4e73 3a5b 6a26 2c3f 3837 6c4d 406a  aDNs:[j&,?87lM@j
000a0df0: 315c 5427 2459 4326 492e 4c6a 7470 5c37  1\T'$YC&I.Ljtp\7
000ac890: 417b 4b77 3f46 424e 5530 6130 644b 592c  A{Kw?FBNU0a0dKY,
0010a0d0: 4570 7d0d 0d0a 4d41 504e 417b 3057 2724  Ep}...MAPNA{0W'$
$ grep 'IHH#6TL+uv}' flags.txt
MAPNA{Tx,D51otN\eUf7qQ7>ToSYQ\;5P6jTIHH#6TL+uv}
```
`0d0d0a`ではなく`0d0a0d`な箇所が一つだけあり、それがflagであった。  

## MAPNA{Tx,D51otN\eUf7qQ7>ToSYQ\;5P6jTIHH#6TL+uv}