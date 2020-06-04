# Comments:Forensics:100pts
I found this file on my Keith's computer... what could be inside?  
Hint  
Look through the comments :eyes:  
Hint  
http://kb.winzip.com/help/winzip/help_comment.htm  
[Comments.zip](Comments.zip)  

# Solution
Comments.zipが渡されるので中身を見てみると、1.zipから8.zipまで何度も圧縮されている。  
8.zipの中にflag.txtがあるがflagではないようだ。  
zipにコメントがなさそうだが、バイナリエディタでComments.zipにfの文字を見つけることができる。  
一つずつ見ていくとflagが得られる。  
stringsしてもよい。  
```bash
$ ls
1.zip  2.zip  3.zip  4.zip  5.zip  6.zip  7.zip  8.zip  Comments.zip  flag.txt
$ strings -n 3 * | grep PK
~~~
No flag here. :(PK
}PK
6PK
nPK
4PK
{PK
gPK
aPK
lPK
fPK
```

## flag{4n6}