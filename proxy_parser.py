import requests
import re
import random
import time

print("🚀 СБОР И ПРОВЕРКА ПРОКСИ", flush=True)
print("=" * 60, flush=True)

all_proxies = []

# Источник 1: Free-Proxy-List
try:
    url = "https://free-proxy-list.net/ru-proxy.html"
    print("🔍 Парсинг free-proxy-list.net...", flush=True)
    resp = requests.get(url, timeout=15)
    rows = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+)</td>', resp.text)
    for ip, port in rows:
        all_proxies.append(f"{ip}:{port}")
    print(f"  ✅ Найдено: {len(rows)}", flush=True)
except Exception as e:
    print(f"  ❌ Ошибка: {e}", flush=True)

# Источник 2: ProxyScrape
try:
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=text"
    print("🔍 Парсинг proxyscrape.com...", flush=True)
    resp = requests.get(url, timeout=15)
    lines = resp.text.strip().split('\r\n')
    for line in lines:
        if line.strip():
            all_proxies.append(line.strip())
    print(f"  ✅ Найдено: {len(lines)}", flush=True)
except Exception as e:
    print(f"  ❌ Ошибка: {e}", flush=True)

# Убираем дубликаты
all_proxies = list(set(all_proxies))
print(f"\n📊 ВСЕГО УНИКАЛЬНЫХ ПРОКСИ: {len(all_proxies)}", flush=True)

if len(all_proxies) == 0:
    print("❌ Нет прокси для проверки", flush=True)
    exit(0)

# Выбираем 100 случайных прокси для проверки
sample = random.sample(all_proxies, min(100, len(all_proxies)))
print(f"🔍 Проверяем {len(sample)} случайных прокси на доступ к Rutube...", flush=True)
print("=" * 60, flush=True)

working = []
for i, proxy in enumerate(sample, 1):
    try:
        r = requests.get(
            "https://rutube.ru",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=10
        )
        if r.status_code == 200:
            print(f"  ✅ [{i}/{len(sample)}] {proxy} → {r.status_code}", flush=True)
            working.append(proxy)
        else:
            print(f"  ❌ [{i}/{len(sample)}] {proxy} → {r.status_code}", flush=True)
    except Exception as e:
        print(f"  ⚠️ [{i}/{len(sample)}] {proxy} → Ошибка", flush=True)
    time.sleep(0.5)

print("=" * 60, flush=True)
print(f"📊 РЕЗУЛЬТАТ: {len(working)}/{len(sample)} прокси работают", flush=True)

if working:
    print("\n✅ РАБОЧИЕ ПРОКСИ (можно использовать в боте):", flush=True)
    for p in working[:10]:
        print(f"  http://{p}", flush=True)
else:
    print("\n❌ Нет рабочих прокси. Бесплатные прокси не подходят для Rutube.", flush=True)
