import time
import threading
from scapy.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ---------- 設定 ----------
TARGET = "chamber-of-echos.challenges.beginners.seccon.jp"
KEY = bytes.fromhex("546869734973415365637265744b6579")
BLOCK_SIZE = 16
TIMEOUT = 1.0  # 秒
THREADS = 4  # 並列送信数（回線によって調整可）

# ---------- 復号用セットアップ ----------
cipher = AES.new(KEY, AES.MODE_ECB)

# インデックス -> 復号済みデータ
results = {}

# ロックでスレッドセーフ
lock = threading.Lock()


def send_ping(index: int):
    while True:
        try:
            pkt = IP(dst=TARGET) / ICMP(type=8) / Raw(load=b"A" * 1)
            reply = sr1(pkt, timeout=TIMEOUT, verbose=False)
            if reply and Raw in reply:
                encrypted = bytes(reply[Raw].load)
                decrypted = cipher.decrypt(encrypted)

                # パディング除去
                try:
                    plain = unpad(decrypted, BLOCK_SIZE)
                except ValueError:
                    continue  # パディングエラーは無視

                # b"0|xxx" のような形式をパース
                if b"|" not in plain:
                    continue
                idx_str, chunk = plain.split(b"|", 1)
                idx = int(idx_str.decode())

                with lock:
                    if idx not in results:
                        results[idx] = chunk
                        print(f"[+] Got chunk {idx}: {chunk.decode(errors='ignore')}")
                        if len(results) >= 20:  # 十分集まったら止める（調整可）
                            break
        except Exception as e:
            continue


def main():
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=send_ping, args=(i,))
        t.daemon = True
        t.start()
        threads.append(t)

    # すべてのチャンクが揃うまで待機（タイムアウトも検討可）
    while True:
        with lock:
            if len(results) >= 20:  # 必要な分揃ったら終了
                break
        time.sleep(0.1)

    # 結果の整形
    flag = b"".join(results[i] for i in sorted(results))
    print("\n[*] Flag:", flag.decode())


if __name__ == "__main__":
    main()
