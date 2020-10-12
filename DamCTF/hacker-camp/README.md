# hacker-camp:web:371pts
Sponsored challenge provided by [HackerOne](https://www.hackerone.com/). Questions/issues go to captainGeech.  
Natasha Drew wants to go to Hacker Camp but doesn't have the grades she needs. Hack into the student portal and change her grades so she can attend.  
[hacker-camp.chals.damctf.xyz](https://hacker-camp.chals.damctf.xyz/)  

# Solution
リンクに飛ぶと以下のようなサイトだった。  
OSUSEC - Student Management Portal  
[site1.png](site/site1.png)  
Natasha Drewの成績を書き換えたいようだ。  
まずはSQLインジェクションを試す。  
```text
t' OR 't' = 't
```
脆弱性がありログインに成功した。  
OSUSEC - Dashboard  
[site2.png](site/site2.png)  
データベースをあさるが何もなかった。  
ソースを見てみると以下のような記述があった。  
```html
~~~
<script>
    var staff = {
        admin   :   false,
        name    :   'rhonda.daniels'
    }
</script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
<script src="/assets/js/app.min.js"></script>
</body>
</html>
```
adminであると何かできるようだ。  
app.min.jsを見てみる。  
```JavaScript:app.min.js
(function(s,objectName){setupLinks = function(){if( s.admin ){var sl = document.getElementsByClassName("student-link");for (i = 0; i < sl.length; i++) {let name = sl[i].innerHTML;sl[i].style.cursor='pointer';sl[i].addEventListener("click", function(){window.location = '/update-' + objectName + '/' + this.dataset.id;});}}};updateForm = function(){ var submitButton = document.getElementsByClassName("update-record"); if( submitButton.length === 1 ){ submitButton[0].addEventListener("click", function(){var english = document.getElementById("english");english = english.options[english.selectedIndex].value;var science = document.getElementById("science");science = science.options[science.selectedIndex].value;var maths = document.getElementById("maths");maths = maths.options[maths.selectedIndex].value;var grades = new Set(["A","B","C","D","E","F"]);if (grades.has(english) && grades.has(science) && grades.has(maths) ) {document.getElementById('student-form').submit();}else{ alert('Grades should only be between A - F');}});}};setupLinks();updateForm();})(staff,'student');
```
[整形する](https://lab.syncer.jp/Tool/JavaScript-PrettyPrint/)と以下になる。  
```JavaScript
(function (s, objectName) {
  setupLinks = function () {
    if (s.admin) {
      var sl = document.getElementsByClassName("student-link");
      for (i = 0; i < sl.length; i++) {
        let name = sl[i].innerHTML;
        sl[i].style.cursor = 'pointer';
        sl[i].addEventListener("click", function () {
          window.location = '/update-' + objectName + '/' + this.dataset.id;
        });
      }
    }
  };
  updateForm = function () {
    var submitButton = document.getElementsByClassName("update-record");
    if (submitButton.length === 1) {
      submitButton[0].addEventListener("click", function () {
        var english = document.getElementById("english");
        english = english.options[english.selectedIndex].value;
        var science = document.getElementById("science");
        science = science.options[science.selectedIndex].value;
        var maths = document.getElementById("maths");
        maths = maths.options[maths.selectedIndex].value;
        var grades = new Set(["A", "B", "C", "D", "E", "F"]);
        if (grades.has(english) && grades.has(science) && grades.has(maths)) {
          document.getElementById('student-form').submit();
        } else {
          alert('Grades should only be between A - F');
        }
      });
    }
  };
  setupLinks();
  updateForm();
})(staff, 'student');
```
`'/update-' + objectName + '/' + this.dataset.id`に飛んでいるようだ。  
ソースの以下からthis.dataset.idがbase64された名前(アンダーバー区切り)であることがわかる。  
```html
~~~
<td data-id="TmFuY2llX0JyZXR0" class="student-link">Brett, Nancie</td>
~~~
```
`https://hacker-camp.chals.damctf.xyz/update-student/TmFuY2llX0JyZXR0`にアクセスすると以下のようであった。  
Brett, Nancie  
[site3.png](site/site3.png)  
成績を書き換えられるようである。  
Natasha_Drewをbase64したTmF0YXNoYV9EcmV3にアクセスし、成績をすべてAに書き換える。  
flag  
[flag.png](site/flag.png)  
flagが得られた。  

## dam{n0w_w3_c4n_h4ck_th3_pl4n3t}