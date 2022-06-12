const NodeRSA = require("node-rsa");

const key = new NodeRSA(`
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAJhmdrx/D3RFG6M0zah4mviLAjxoOx+LbdbgJm7bfh3S8rvDnk0b
DULPxcuy9FOMLLdlS4YHZ1bo8QGD+0BU0vUCAwEAAQJBAITBVRNUV6EABlhAShpE
nTJ+3P7ECSSsb40riy8scosE9vED0oogPsNnlRdSCXJDGSptCtb57vMXzqD9w2IC
ye0CIQDq53DzLHcTVGGqfVraPRSyZwR1mExTVLfv8GYC7YBpCwIhAKYWOD2NGfqt
ZNFOyZprpYmwI1MHjU2ysRDiNdZ+3TP/AiAEHkynpsbrqtYPhCUcoGeFfTLh0Oq9
p0WWSlOvh3Rx4wIhAIpaHhVf8hE42a/mAtio7WeqG3Lx6oqb3RYkaha47Yl/AiBJ
vrGHYAkQzrubzGupvpTVTex2q6D/27XuaWWVrO11OQ==
-----END RSA PRIVATE KEY-----
`);

const encrypted = "V44FTEScskUnyxOlSRtWiWqrY6tGOPYtxvNOZxx6rxQD7BAJJncc86enn5FYp53hJDdbCcJDsudy39grhL7DAlUe+NPOgV+j7BN1igZRE9C+y5kORoyKF7AP0H5oErn6HdvdUK9f3ANfWJk9EzcB3M7MhcyC/zmL/xZ4Bf4VmVVicZCVDEteYCNVPA8vr0olphXJIEkBmhXG3wy9OrKTkh4VonqSjMvlBvqWELJlsWUdgvKVht2yHVErwF1K27xf";

const decrypted = key.decrypt(encrypted, "utf8");
console.log("flag: ", decrypted);