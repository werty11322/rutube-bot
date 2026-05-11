import sys
import time
import random
import requests

print("🚀 БОТ ЗАПУЩЕН (тест HTTP)", flush=True)

VIDEO_URL = "https://rutube.ru/video/cf89b1de7a3db4d79069629e96116ebb/"
TARGET_VIEWS = 20
PROXIES = [
    "https://proxy-2.alinakozlova1745.workers.dev",
    "https://proxy-3.alinakozlova1745.workers.dev",
    "https://proxy-4.alinakozlova1745.workers.dev",
    "https://proxy-5.alinakozlova1745.workers.dev",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
]

def watch_video_http(proxy, url):
    full_url = f"{proxy}?url={url}"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        resp = requests.get(full_url, timeout=30)
        return resp.status_code == 200
    except Exception as e:
        print(f"  Ошибка HTTP: {e}")
        return False

def main():
    print("=" * 60)
    print("🤖 RUTUBE БОТ (HTTP тест)")
    print("=" * 60)
    success = 0
    for i in range(TARGET_VIEWS):
        print(f"\n📹 {i+1}/{TARGET_VIEWS}")
        proxy = PROXIES[i % len(PROXIES)]
        if watch_video_http(proxy, VIDEO_URL):
            success += 1
        if i < TARGET_VIEWS - 1:
            wait = random.randint(30, 45)
            print(f"  ⏳ Жду {wait} сек...")
            time.sleep(wait)
    print(f"\n✅ ИТОГ: {success}/{TARGET_VIEWS}")

if __name__ == "__main__":
    main()


