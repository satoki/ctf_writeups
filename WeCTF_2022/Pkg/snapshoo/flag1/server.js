const fs = require("fs");
//var data = fs.readFileSync("C:\\snapshot\\flag1\\server.js").toString("utf8");
var data = fs.readFileSync("C:\\snapshot\\flag1\\private_key.der").toString("hex");
console.log(data);