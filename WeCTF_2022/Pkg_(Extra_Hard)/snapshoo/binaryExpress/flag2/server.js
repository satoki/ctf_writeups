const fs = require("fs");
//var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\server.js").toString("utf8");
//var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\jwtRS256.key").toString("hex");
var data = fs.readFileSync("C:\\snapshot\\binaryExpress\\flag2\\views\\flag.ejs").toString("utf8");
console.log(data);