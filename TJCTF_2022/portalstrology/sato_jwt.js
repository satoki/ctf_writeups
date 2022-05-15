const fs = require("fs")
const jwt = require("jsonwebtoken")

const username = "superigamerbean";
const iat = 1652821200;
const privatekey = fs.readFileSync(`_private.key`, 'utf8')
const token = jwt.sign(
    {
        username,
        iat,
    },
    privatekey,
    {
        algorithm: 'RS256',
        expiresIn: "2h",
        header: {
            alg: 'RS256',
            jku: 'https://satoki.free.beeceptor.com/jwks.json',
            kid: '1',
        }
    }
);

console.log(token);