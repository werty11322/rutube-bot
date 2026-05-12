import requests
import re
import random
import time
from bs4 import BeautifulSoup

def fetch_proxies():
    """Собирает прокси с бесплатных сайтов"""
    proxies = []
    
    # Источник 1: Free-Proxy-List (Россия)
    try:
        url = "https://free-proxy-list.net/ru-proxy.html"
        resp = requests.get(url, timeout=15)
        rows = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+)</td>', resp.text)
        for ip, port in rows:
            proxies.append(f"http://{ip}:{port}")
        print(f"✅ Free-Proxy-List: {len(rows)} прокси")
    except Exception as e:
        print(f"⚠️ Ошибка Free-Proxy-List: {e}")
    
    # Источник 2: HideMy.Name (Россия)
    try:
        url = "https://hidemy.name/ru/proxy-list/?country=RU#list"
        resp = requests.get(url, timeout=15)
        rows = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+)</td>', resp.text)
        for ip, port in rows:
            proxies.append(f"http://{ip}:{port}")
        print(f"✅ HideMy.Name: {len(rows)} прокси")
    except Exception as e:
        print(f"⚠️ Ошибка HideMy.Name: {e}")
    
    # Источник 3: ProxyScrape (все страны, потом отфильтруем РФ)
    try:
        url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=ipport&format=text"
        resp = requests.get(url, timeout=15)
        raw = resp.text.split('\r\n')
        for line in raw:
            if line.strip():
                proxies.append(f"http://{line.strip()}")
        print(f"✅ ProxyScrape: {len(raw)} прокси")
    except Exception as e:
        print(f"⚠️ Ошибка ProxyScrape: {e}")
    
    # Убираем дубликаты
    proxies = list(set(proxies))
    print(f"📊 Всего собрано: {len(proxies)} прокси")
    return proxies

def check_proxy(proxy, test_url="https://rutube.ru", timeout=10):
    """Проверяет, работает ли прокси"""
    try:
        r = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=timeout)
        return r.status_code == 200
    except:
        return False

def get_working_proxies(proxy_list, limit=10):
    """Проверяет список прокси и возвращает рабочие"""
    working = []
    for proxy in proxy_list:
        if check_proxy(proxy):
            working.append(proxy)
            print(f"  ✅ {proxy}")
            if len(working) >= limit:
                break
        else:
            print(f"  ❌ {proxy}")
        time.sleep(0.5)
    return working

# ========== ИСПОЛЬЗОВАНИЕ ==========
if __name__ == "__main__":
    print("🚀 Сбор свежих прокси...")
    all_proxies = fetch_proxies()
    print(f"\n🔍 Проверка {len(all_proxies)} прокси (может занять время)...")
    good = get_working_proxies(all_proxies, limit=10)
    print(f"\n✅ Рабочих прокси найдено: {len(good)}")
    print("\nСписок для вставки в PROXIES:")
    print(good)
