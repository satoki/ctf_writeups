# AuthEN:Web Exploitation:50pts
Ada is important to the world, she is important for a reason  
Link: [http://104.198.67.251/authen](http://104.198.67.251/authen)  

# Solution
URLを開くと登録フォームのようだが、登録(ログイン？)できない。  
Register  
[site.png](site/site.png)  
ソースを見ると以下の記述があった。  
```html
~~~
                <script>
                $(“.c_submit”).click(function(event) {
 event.preventDefault()
 var email = $(“#cuser”).val();
 var password = $(“#cpass”).val();
 if(username == “admin” && password == String.fromCharCode(115, 104, 97, 107, 116, 105, 99, 116, 102, 123, 98, 51, 121, 48, 110, 100, 95, 112, 117, 114, 51, 95, 99, 52, 108, 99, 117, 108, 97, 116, 105, 48, 110, 115, 125)) {
 if(document.location.href.indexOf(“?password=”) == -1) { 
 document.location = document.location.href + “?password=” + password;
 }
 } else {
 $(“#cresponse”).html(“<div class=’alert alert-danger’>Wrong password sorry.</div>”);
 }
 })
                </script>
~~~
```
passwordが知りたいため、以下のように文字列にする。  
```bash
$ node
> String.fromCharCode(115, 104, 97, 107, 116, 105, 99, 116, 102, 123, 98, 51, 121, 48, 110, 100, 95, 112, 117, 114, 51, 95, 99, 52, 108, 99, 117, 108, 97, 116, 105, 48, 110, 115, 125)
'shaktictf{b3y0nd_pur3_c4lculati0ns}'
```
flagが得られた。  

## shaktictf{b3y0nd_pur3_c4lculati0ns}