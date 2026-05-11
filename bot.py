import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ========== КОНФИГУРАЦИЯ ==========
VIDEO_URL = "https://rutube.ru/video/cf89b1de7a3db4d79069629e96116ebb/"
TARGET_VIEWS = 20
MIN_TIME = 90
MAX_TIME = 180

# Cloudflare прокси
PROXIES = [
    "https://proxy-2.alinakozlova1745.workers.dev",
    "https://proxy-3.alinakozlova1745.workers.dev",
    "https://proxy-4.alinakozlova1745.workers.dev",
    "https://proxy-5.alinakozlova1745.workers.dev",
]

# User-Agent ротация
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/147.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
]

def get_chrome_options():
    """Настройки Chrome для GitHub Actions"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    return options

def watch_video(proxy, url, duration):
    options = get_chrome_options()
    selected_ua = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={selected_ua}")
    
    try:
        driver = webdriver.Chrome(options=options)
        
        full_url = f"{proxy}?url={url}"
        print(f"  Прокси: {proxy.split('/')[2]}")
        driver.get(full_url)
        
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        
        driver.execute_script("""
            var v = document.querySelector('video');
            if(v) {
                v.muted = true;
                v.play();
            }
        """)
        
        print(f"  Смотрю {duration} сек...")
        
        start_time = time.time()
        while time.time() - start_time < duration:
            scroll_y = random.randint(50, 200)
            driver.execute_script(f"window.scrollBy(0, {scroll_y})")
            time.sleep(random.uniform(5, 10))
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"  Ошибка: {str(e)[:100]}")
        try:
            driver.quit()
        except:
            pass
        return False

def main():
    print("=" * 60)
    print("🤖 RUTUBE БОТ (GitHub Actions)")
    print("=" * 60)
    print(f"📹 Видео: {VIDEO_URL}")
    print(f"🎯 Цель: {TARGET_VIEWS} просмотров")
    print(f"🔄 Прокси: {len(PROXIES)} шт")
    print("=" * 60)
    
    success = 0
    for i in range(TARGET_VIEWS):
        print(f"\n📹 Просмотр {i+1}/{TARGET_VIEWS}")
        proxy = PROXIES[i % len(PROXIES)]
        duration = random.randint(MIN_TIME, MAX_TIME)
        
        if watch_video(proxy, VIDEO_URL, duration):
            success += 1
        
        if i < TARGET_VIEWS - 1:
            wait = random.randint(45, 90)
            print(f"⏳ Жду {wait} сек...")
            time.sleep(wait)
    
    print(f"\n📊 ИТОГ: {success}/{TARGET_VIEWS}")

if __name__ == "__main__":
    main()
