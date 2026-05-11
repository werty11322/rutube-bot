import sys
import time
import random
import traceback

print("🚀 БОТ ЗАПУЩЕН", flush=True)

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    print("✅ Библиотеки импортированы", flush=True)
except Exception as e:
    print(f"❌ Ошибка импорта: {e}", flush=True)
    sys.exit(1)

# ========== КОНФИГУРАЦИЯ ==========
VIDEO_URL = "https://rutube.ru/video/cf89b1de7a3db4d79069629e96116ebb/"
TARGET_VIEWS = 20
MIN_TIME = 90
MAX_TIME = 180

PROXIES = [
    "https://proxy-2.alinakozlova1745.workers.dev",
    "https://proxy-3.alinakozlova1745.workers.dev",
    "https://proxy-4.alinakozlova1745.workers.dev",
    "https://proxy-5.alinakozlova1745.workers.dev",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/147.0.0.0 Safari/537.36",
]

def watch_video(proxy, url, duration):
    print(f"  Прокси: {proxy.split('/')[2]}", flush=True)
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    selected_ua = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={selected_ua}")
    
    try:
        print("  Создаю драйвер...", flush=True)
        driver = webdriver.Chrome(options=options)
        
        full_url = f"{proxy}?url={url}"
        print(f"  Открываю: {full_url[:80]}...", flush=True)
        driver.get(full_url)
        
        print("  Жду загрузки страницы...", flush=True)
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("  Жду видео...", flush=True)
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        
        print("  Запускаю видео...", flush=True)
        driver.execute_script("""
            var v = document.querySelector('video');
            if(v) {
                v.muted = true;
                v.play();
            }
        """)
        
        print(f"  Смотрю {duration} сек...", flush=True)
        start_time = time.time()
        while time.time() - start_time < duration:
            driver.execute_script(f"window.scrollBy(0, {random.randint(50, 200)})")
            time.sleep(random.uniform(5, 10))
        
        driver.quit()
        print("  ✅ Успешно", flush=True)
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
    print("🤖 RUTUBE БОТ (GitHub Actions)", flush=True)
    print("=" * 60, flush=True)
    print(f"📹 Видео: {VIDEO_URL}", flush=True)
    print(f"🎯 Цель: {TARGET_VIEWS} просмотров", flush=True)
    print(f"🔄 Прокси: {len(PROXIES)} шт", flush=True)
    print("=" * 60, flush=True)
    
    success = 0
    for i in range(TARGET_VIEWS):
        print(f"\n📹 Просмотр {i+1}/{TARGET_VIEWS}", flush=True)
        proxy = PROXIES[i % len(PROXIES)]
        duration = random.randint(MIN_TIME, MAX_TIME)
        
        if watch_video(proxy, VIDEO_URL, duration):
            success += 1
        
        if i < TARGET_VIEWS - 1:
            wait = random.randint(45, 90)
            print(f"⏳ Жду {wait} сек...", flush=True)
            time.sleep(wait)
    
    print("\n" + "=" * 60, flush=True)
    print(f"📊 ИТОГ: {success}/{TARGET_VIEWS}", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    main()


