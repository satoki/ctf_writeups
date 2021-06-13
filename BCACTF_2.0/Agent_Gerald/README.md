# Agent Gerald:webex:125pts
Agent Gerald is a spy in SI-6 (Stegosaurus Intelligence-6). We need you to infiltrate this top-secret SI-6 webpage, but it looks like it can only be accessed by Agent Gerald's special browser...  
[http://web.bcactf.com:49156/](http://web.bcactf.com:49156/)  
  
Hint 1 of 1  
What is a way webpages know what kind of browser you're using?  

# Solution
サイトにアクセスすると謎のページが出てくる。  
Welcome to the Stegosaurus Intelligence-6 Homepage  
[site.png](site/site.png)  
問題名からもUser-Agentが怪しそうだ。  
以下のようにUser-Agentを`Gerald`にしてGETしてみる。
```bash
$ curl -H "User-Agent: Gerald" http://web.bcactf.com:49156/
<!DOCTYPE html>
        <html>
            <head>
            </head>
            <body>
                <h1>Welcome to the Stegosaurus Intelligence-6 Homepage</h1>
                <h2>Are you Agent Gerald?</h2>
                <img src="gerald.PNG" alt="agent gerald" style="width: 50%"></img>
                   <h4> Welcome, Agent Gerald! Your flag is: bcactf{y0u_h@ck3d_5tegos@urus_1nt3lligence} </h4>
            </body>
        </html>
```
flagが得られた。  

## bcactf{y0u_h@ck3d_5tegos@urus_1nt3lligence}