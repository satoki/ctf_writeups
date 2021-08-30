# Header:Web:50pts
作成中のサイトを管理しているサーバに問題があり、機密情報が漏洩しているようです。サイトにアクセスして機密情報を特定してください。  
以下のサイトにアクセスして隠されたフラグを見つけてください。  
[https://ctf.setodanote.net/web002/](https://ctf.setodanote.net/web002/)  

# Solution
問題の通りヘッダーを見る。  
```bash
$ curl --head https://ctf.setodanote.net/web002/
HTTP/2 200
date: Mon, 23 Aug 2021 10:33:49 GMT
content-type: text/html
last-modified: Tue, 17 Aug 2021 03:42:18 GMT
x-setodanotectf-flag: flag{Just_a_whisper}
permissions-policy: interest-cohort=()
x-nginx-cache: MISS
accept-ranges: bytes
cf-cache-status: DYNAMIC
expect-ct: max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"
report-to: {"endpoints":[{"url":"https:\/\/a.nel.cloudflare.com\/report\/v3?s=V2cX3X4bMULAAxZQJoqrpGYTC%2BqRQbbryhrJ3VEGjxMU%2FY25jwOPUcLDEpTXzlwcHhPkbcctX2RtJH6rvGRAtEwTVDHOOoJHdC6%2B78tYB2dp6UnuDX9DWsUt30HsbGiQyRovjh8%3D"}],"group":"cf-nel","max_age":604800}
nel: {"success_fraction":0,"report_to":"cf-nel","max_age":604800}
server: cloudflare
cf-ray: 6833af570c720a7a-KIX

```
flagが得られた。  

## flag{Just_a_whisper}