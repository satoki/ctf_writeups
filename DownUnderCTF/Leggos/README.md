# Leggos:web:100pts
I <3 Pasta! I won't tell you what my special secret sauce is though!  
[https://chal.duc.tf:30101](https://chal.duc.tf:30101/)  

# Solution
URLにアクセスすると以下のようなサイトだった。  
My Favourite Pasta Sauce  
[site.png](site/site.png)  
ソースを見ると良さそうだ。  
右クリックが禁止されているようだが、頑張って(開発者ツールなどで)ソースを見る。  
```html
~~~
        </style>
        <script src="disableMouseRightClick.js"></script>
    </head>
~~~
        <div class="main-body">
            <h1>My Second Favourite Pasta Sauce</h1>
            <p>This is my second favourite pasta sauce! I have safely hidden my favourite sauce!</p>
            <!-- almost there -->
            <img src="./sauce.JPEG" >
        </div>
~~~
```
disableMouseRightClick.jsなるものがあるようだ。  
開くと以下のようだった。  
```JavaScript:disableMouseRightClick.js
document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    alert('not allowed');
});

  //the source reveals my favourite secret sauce 
  // DUCTF{n0_k37chup_ju57_54uc3_r4w_54uc3_9873984579843} 
```
コメントにflagが書かれている。  

## DUCTF{n0_k37chup_ju57_54uc3_r4w_54uc3_9873984579843}