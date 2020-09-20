# Twitter:misc:10pts
Check out our Twitter! Find the post with the flag! You can give us a follow if you like <3  

# Solution
公式の[Twitter](https://twitter.com/DownUnderCTF)を見てみる。  
それらしきツイートがあるがbase64エンコードされているようだ。  
![twitter.png](image/twitter.png)  
デコードする。  
```bash
$ python
>>> import base64
>>> text = "RFVDVEZ7aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1YZlI5aVk1eTk0c30="
>>> print(base64.b64decode(text))
b'DUCTF{https://www.youtube.com/watch?v=XfR9iY5y94s}'
```

## DUCTF{https://www.youtube.com/watch?v=XfR9iY5y94s}