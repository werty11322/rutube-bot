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
        print(f"  Запрос к {full_url[:80]}...", flush=True)
        resp = requests.get(full_url, timeout=30)
        print(f"  Статус: {resp.status_code}", flush=True)
        return resp.status_code == 200
    except Exception as e:
        print(f"  Ошибка HTTP: {e}", flush=True)
        return False

def main():
    print("=" * 60, flush=True)
    print("🤖 RUTUBE БОТ (HTTP тест)", flush=True)
    print("=" * 60, flush=True)
    success = 0
    for i in range(TARGET_VIEWS):
        print(f"\n📹 {i+1}/{TARGET_VIEWS}", flush=True)
        proxy = PROXIES[i % len(PROXIES)]
        if watch_video_http(proxy, VIDEO_URL):
            success += 1
        if i < TARGET_VIEWS - 1:
            wait = random.randint(30, 45)
            print(f"  ⏳ Жду {wait} сек...", flush=True)
            time.sleep(wait)
    print(f"\n✅ ИТОГ: {success}/{TARGET_VIEWS}", flush=True)

if __name__ == "__main__":
    main()
