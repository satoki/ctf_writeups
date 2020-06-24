# # <!--XXXXXXXXXX-->
I just found a hate group targeting my favorite animal. Can you try and find their secrets? We gotta take them down!  
Site: [panda-facts.2020.redpwnc.tf](https://panda-facts.2020.redpwnc.tf/)  
[index.js](index.js)  

# Solution
サイトに飛ぶとユーザーネームを要求される。  
Panda Facts  
[site1.png](site/site1.png)  
satokiで入ると以下のようなページに移動した。  
Welcome, satoki! Here are some panda facts!  
[site2.png](site/site2.png)  
メンバーであれば"Click to see a member-only fact!"ボタンで進めるようだ。  
ソースから以下のような記述を見つけることができる。  
```JavaScript
~~~
async function generateToken(username) {
    const algorithm = 'aes-192-cbc'; 
    const key = Buffer.from(process.env.KEY, 'hex'); 
    // Predictable IV doesn't matter here
    const iv = Buffer.alloc(16, 0);

    const cipher = crypto.createCipheriv(algorithm, key, iv);

    const token = `{"integrity":"${INTEGRITY}","member":0,"username":"${username}"}`

    let encrypted = '';
    encrypted += cipher.update(token, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    return encrypted;
}
~~~
```
aesを解読しなければならないかと思ったが、ユーザーネームに"や\を入れるとページがうまく動作しない。  
この動作によりtokenのusernameにインジェクションが可能であることがわかる。  
`yamaguchi","member":1,"a":"a`を入力するとメンバーとしてflagが得られた。  
flag  
[flag.png](site/flag.png)  

## flag{1_c4nt_f1nd_4_g00d_p4nd4_pun}