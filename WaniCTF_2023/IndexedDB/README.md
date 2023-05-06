# IndexedDB:Web:119pts
このページのどこかにフラグが隠されているようです。ブラウザの開発者ツールを使って探してみましょう。  
It appears that the flag has been hidden somewhere on this page. Let's use the browser's developer tools to find it.  
[https://indexeddb-web.wanictf.org](https://indexeddb-web.wanictf.org/)  

# Solution
ページのどこかにフラグが隠されているとある。  
ひとまずcurlしてみる。  
```bash
$ curl https://indexeddb-web.wanictf.org/
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
  </head>

  <body>
  </body>
  <script>
    var connection;

    window.onload = function () {
      var openRequest = indexedDB.open("testDB");

      openRequest.onupgradeneeded = function () {
        connection = openRequest.result;
        var objectStore = connection.createObjectStore("testObjectStore", {
          keyPath: "name",
        });
        objectStore.put({ name: "FLAG{y0u_c4n_u3e_db_1n_br0wser}" });
      };

      openRequest.onsuccess = function () {
        connection = openRequest.result;
      };
      window.location = "1ndex.html";
    };
  </script>
</html>
```
flagが隠されて？いた。  

## FLAG{y0u_c4n_u3e_db_1n_br0wser}