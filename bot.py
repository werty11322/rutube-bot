import sys
import time
import random
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("🚀 БОТ ЗАПУЩЕН (Webshare Proxy Test)", flush=True)

# ========== АВТОРИЗОВАННЫЕ ПРОКСИ (твои) ==========
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

# Цель
VIDEO_URL = "https://rutube.ru/video/cf89b1de7a3db4d79069629e96116ebb/"

def watch_video_with_auth(proxy_string, url):
    """
    Запускает Chrome через указанный прокси (с авторизацией)
    и пытается открыть Rutube.
    """
    proxy_parts = proxy_string.split('@')
    proxy_auth = proxy_parts[0].replace('http://', '')
    proxy_addr = proxy_parts[1]
    proxy_login, proxy_pass = proxy_auth.split(':')

    options = Options()
    # --- Ключевые опции для GitHub Actions ---
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Задаём прокси (без логина/пароля)
    options.add_argument(f'--proxy-server={proxy_addr}')

    try:
        driver = webdriver.Chrome(options=options)

        # --- АВТОРИЗАЦИЯ НА ПРОКСИ через alert (самый частый случай) ---
        driver.get("http://httpbin.org/ip")
        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.send_keys(f"{proxy_login}\t{proxy_pass}")
            alert.accept()
            print(f"  [OK] Авторизация на прокси {proxy_addr} прошла", flush=True)
        except Exception as auth_err:
            print(f"  [!] Нет окна авторизации (возможно, не требуется) — {auth_err}", flush=True)

        # --- ОСНОВНОЙ АДРЕС ---
        full_url = f"{proxy_addr}?url={url}"  # обрати внимание: используем только адрес, без логина
        # (Worker у нас отдельный, но здесь мы пробуем без Cloudflare Worker)
        # Правильнее: driver.get(url)
        driver.get(url)

        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        driver.execute_script("""
            var v = document.querySelector('video');
            if(v) { v.muted = true; v.play(); }
        """)
        print(f"  Просмотр {duration} сек...", flush=True)
        time.sleep(90)  # фиксированное время для теста

        driver.quit()
        return True
    except Exception as e:
        print(f"  ❌ Ошибка: {str(e)[:100]}", flush=True)
        traceback.print_exc()
        try:
            driver.quit()
        except:
            pass
        return False

def main():
    print("=" * 60, flush=True)
    print("🤖 RUTUBE БОТ (Webshare Proxy Test)", flush=True)
    print(f"📹 Видео: {VIDEO_URL}", flush=True)
    print(f"🔄 Прокси: {len(PROXIES)} шт", flush=True)
    print("=" * 60, flush=True)

    success = 0
    for i, proxy in enumerate(PROXIES):
        print(f"\n📹 Просмотр {i+1}/{len(PROXIES)}")
        if watch_video_with_auth(proxy, VIDEO_URL):
            success += 1

        if i < len(PROXIES) - 1:
            wait = random.randint(45, 90)
            print(f"⏳ Жду {wait} сек...")
            time.sleep(wait)

    print(f"\n✅ ИТОГ: {success}/{len(PROXIES)}")

if __name__ == "__main__":
    main()
