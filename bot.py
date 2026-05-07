from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
import os

def main():
    print("🤖 RUTUBE БОТ ЗАПУЩЕН")
    print("=" * 50)
    
    # Настройки (можно через переменные окружения)
    url = os.environ.get("RUTUBE_URL", "https://rutube.ru/video/test/")
    target = int(os.environ.get("TARGET_VIEWS", "5"))
    
    success = 0
    for i in range(target):
        print(f"\n📹 Просмотр {i+1}/{target}")
        
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        driver = None
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            watch_time = random.randint(60, 120)
            print(f"⏱ Смотрю {watch_time} сек...")
            time.sleep(watch_time)
            
            success += 1
            print("✅ Успешно")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        finally:
            if driver:
                driver.quit()
        
        if i < target - 1:
            wait = random.randint(30, 60)
            print(f"⏳ Жду {wait} сек...")
            time.sleep(wait)
    
    print(f"\n📊 Итог: {success}/{target}")

if __name__ == "__main__":
    main()
