import sys
import requests
import time

print("🚀 Тест прокси (HTTP only)", flush=True)

PROXIES = [
    "http://izvsdzck:vteq8avwcr0h@31.58.9.4:6077",
    "http://izvsdzck:vteq8avwcr0h@31.59.20.176:6754",
    "http://izvsdzck:vteq8avwcr0h@45.38.107.97:6014",
    "http://izvsdzck:vteq8avwcr0h@216.10.27.159:6837",
    "http://izvsdzck:vteq8avwcr0h@107.172.163.27:6543",
    "http://izvsdzck:vteq8avwcr0h@191.96.254.138:6185",
    "http://izvsdzck:vteq8avwcr0h@23.229.19.94:8689",
    "http://izvsdzck:vteq8avwcr0h@31.56.127.193:7684",
    "http://izvsdzck:vteq8avwcr0h@198.23.243.226:6361",
]

VIDEO_URL = "https://rutube.ru/video/cf89b1de7a3db4d79069629e96116ebb/"

def test_proxy(proxy):
    try:
        r = requests.get(VIDEO_URL, proxies={"http": proxy, "https": proxy}, timeout=15)
        print(f"  {proxy.split('@')[1][:20]}... → {r.status_code}", flush=True)
        return r.status_code == 200
    except Exception as e:
        print(f"  ❌ {proxy.split('@')[1][:20]}... → {str(e)[:50]}", flush=True)
        return False

def main():
    print("=" * 60, flush=True)
    print("Проверка доступа к Rutube через Webshare прокси", flush=True)
    print("=" * 60, flush=True)
    success = 0
    for idx, proxy in enumerate(PROXIES, 1):
        print(f"\n🔎 Прокси {idx}/{len(PROXIES)}", flush=True)
        if test_proxy(proxy):
            success += 1
        time.sleep(2)
    print(f"\n✅ Работает: {success}/{len(PROXIES)}", flush=True)

if __name__ == "__main__":
    main()
