# striped table:Web:pts
テーブルの行の背景色をストライプにする作業をしてもらったら、こんなことになってしまいました!  
ページにjavascript`alert(19640503)`を埋め込み実行させるとフラグが得られます。  
[https://striped.wanictf.org/?source](https://striped.wanictf.org/?source)にアクセスするとソースが閲覧できます。  
[https://striped.wanictf.org](https://striped.wanictf.org/)  

# Solution
URLにアクセスするとメモが投稿できるサイトがある。  
メモアプリ  
[site.png](site/site.png)  
ソースも見られるようだ。  
以下に注目する。  
```html
~~~
      <?php foreach ($results as $index => $result) : ?>
        <?php if ($index % 2 === 0) : ?>
          <tr>
            <td><?= $result['id'] ?></td>
            <td><?= htmlspecialchars($result['title'], ENT_QUOTES) ?></td>
            <td><?= nl2br(htmlspecialchars($result['memo'], ENT_QUOTES)) ?></td>
            <td><a href="/?delete=<?= $result['id'] ?>"><button type="button" class="btn btn-danger">削除</button></a></td>
          </tr>
        <?php else: ?>
          <tr style="background-color: #f0f0f0">
            <td><?= $result['id'] ?></td>
            <td><?= htmlspecialchars($result['title'], ENT_QUOTES) ?></td>
            <td><?= nl2br($result['memo']) ?></td>
            <td><a href="/?delete=<?= $result['id'] ?>"><button type="button" class="btn btn-danger">削除</button></a></td>
          </tr>
        <?php endif; ?>
      <?php endforeach; ?>
~~~
```
htmlspecialcharsを忘れている箇所がある。  
`<script>alert(19640503)</script>`を偶数回目に投稿すればよい。  
flagがalertされた。  
flag  
[flag.png](site/flag.png)  
ちなみに`<img src=1 onerror=alert(19640503)>`ではNGだった(謎)。  

## FLAG{simple_cross_site_scripting}