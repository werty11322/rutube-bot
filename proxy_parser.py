import requests
import re

print("🚀 СБОР ПРОКСИ (без проверки)", flush=True)
print("=" * 50, flush=True)

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

print("=" * 50, flush=True)
print(f"📊 ВСЕГО УНИКАЛЬНЫХ ПРОКСИ: {len(all_proxies)}", flush=True)
print("=" * 50, flush=True)
print("\nПервые 20 прокси для примера:", flush=True)
for p in all_proxies[:20]:
    print(f"  {p}", flush=True)
    # Проверка одного случайного прокси
if all_proxies:
    test_proxy = all_proxies[0]
    print(f"\n🧪 Проверка прокси {test_proxy}:", flush=True)
    try:
        r = requests.get("https://rutube.ru", proxies={"http": f"http://{test_proxy}", "https": f"http://{test_proxy}"}, timeout=10)
        print(f"  Статус: {r.status_code}", flush=True)
    except Exception as e:
        print(f"  Ошибка: {str(e)[:50]}", flush=True)
