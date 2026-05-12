import socket
import socks
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Твой список IP:PORT
PEERS = [
    "95.152.62.133:6658",
    "217.8.92.169:43303",
    "29.73.intal.uz:22570",
    "94.181.183.29:10161",
    "78.139.197.146:35525",
    "178.66.164.221:19289",
    "212.61.1.146:27661",
    "90.188.115.38:58807",
    "91.219.138.96:21157",
    "176.194.108.84:22988",
    "95.181.85.74:20437",
    "92.101.194.220:59093",
    "95.181.85.74:42794",  # ip.newbwc.ru
    "62.165.2.52:31188",
]

def check_http_proxy(ip, port):
    """Проверяет, работает ли HTTP прокси"""
    try:
        proxies = {"http": f"http://{ip}:{port}", "https": f"http://{ip}:{port}"}
        r = requests.get("https://rutube.ru", proxies=proxies, timeout=10)
        if r.status_code == 200:
            return f"http://{ip}:{port}"
    except:
        pass
    return None

def check_socks5_proxy(ip, port):
    """Проверяет, работает ли SOCKS5 прокси"""
    try:
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS5, ip, int(port))
        s.settimeout(10)
        s.connect(("rutube.ru", 80))
        s.close()
        return f"socks5://{ip}:{port}"
    except:
        pass
    return None

def check_socks4_proxy(ip, port):
    """Проверяет, работает ли SOCKS4 прокси"""
    try:
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS4, ip, int(port))
        s.settimeout(10)
        s.connect(("rutube.ru", 80))
        s.close()
        return f"socks4://{ip}:{port}"
    except:
        pass
    return None

def scan_peer(peer):
    """Сканирует один IP:PORT на наличие прокси"""
    ip, port = peer.split(":")
    
    print(f"🔍 Сканирую {ip}:{port}...", flush=True)
    
    results = []
    
    # Проверяем HTTP прокси
    http_result = check_http_proxy(ip, port)
    if http_result:
        results.append(http_result)
        print(f"  ✅ HTTP прокси найден: {http_result}", flush=True)
    
    # Проверяем SOCKS5
    socks5_result = check_socks5_proxy(ip, port)
    if socks5_result:
        results.append(socks5_result)
        print(f"  ✅ SOCKS5 прокси найден: {socks5_result}", flush=True)
    
    # Проверяем SOCKS4
    socks4_result = check_socks4_proxy(ip, port)
    if socks4_result:
        results.append(socks4_result)
        print(f"  ✅ SOCKS4 прокси найден: {socks4_result}", flush=True)
    
    if not results:
        print(f"  ❌ Прокси не найдены", flush=True)
    
    return results

def main():
    print("=" * 60, flush=True)
    print("🔍 СКАНИРОВАНИЕ ТОРРЕНТ-ПИРОВ НА НАЛИЧИЕ ПРОКСИ", flush=True)
    print("=" * 60, flush=True)
    print(f"📊 Всего адресов: {len(PEERS)}", flush=True)
    print("=" * 60, flush=True)
    
    all_proxies = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(scan_peer, peer): peer for peer in PEERS}
        for future in as_completed(futures):
            results = future.result()
            all_proxies.extend(results)
    
    print("\n" + "=" * 60, flush=True)
    print(f"📊 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ", flush=True)
    print("=" * 60, flush=True)
    
    if all_proxies:
        print(f"✅ Найдено прокси: {len(all_proxies)}", flush=True)
        for p in all_proxies:
            print(f"  {p}", flush=True)
    else:
        print("❌ Прокси не найдены. Никто из пиров не открыл прокси-сервер.", flush=True)
        print("   Это нормально — большинство пиров не делятся прокси.", flush=True)

if __name__ == "__main__":
    main()
