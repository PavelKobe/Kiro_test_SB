#!/usr/bin/env python3
"""
Тестирование API endpoints
"""

import requests
import sys

def test_api():
    """Тестирует API endpoints"""
    
    base_url = "http://127.0.0.1:5000"
    
    # Сначала нужно войти в систему
    session = requests.Session()
    
    print("🔐 Авторизация...")
    login_data = {
        'username': 'admin',
        'password': '12345'
    }
    
    response = session.post(f"{base_url}/login", data=login_data)
    if response.status_code != 200:
        print(f"❌ Ошибка авторизации: {response.status_code}")
        return False
    
    print("✅ Авторизация успешна")
    
    # Тестируем API подкатегорий
    print("\n📋 Тестирование API подкатегорий...")
    for category_id in [1, 2, 3]:  # Тестируем первые 3 категории
        response = session.get(f"{base_url}/api/subcategories/{category_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Категория {category_id}: {len(data)} подкатегорий")
            if data:
                print(f"      Пример: {data[0]['name']} (SLA: {data[0]['sla_hours']}ч)")
        else:
            print(f"   ❌ Ошибка для категории {category_id}: {response.status_code}")
    
    # Тестируем API отделов
    print("\n🏬 Тестирование API отделов...")
    for store_id in [1, 2, 3]:  # Тестируем первые 3 магазина
        response = session.get(f"{base_url}/api/departments/{store_id}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Магазин {store_id}: {len(data)} отделов")
            if data:
                print(f"      Пример: {data[0]['name']}")
        else:
            print(f"   ❌ Ошибка для магазина {store_id}: {response.status_code}")
    
    print("\n✅ Тестирование API завершено")
    return True

if __name__ == '__main__':
    print("🧪 Тестирование API endpoints...")
    print("Убедитесь, что приложение запущено на http://127.0.0.1:5000")
    print("-" * 50)
    
    try:
        success = test_api()
        sys.exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("❌ Не удается подключиться к приложению")
        print("Запустите приложение: python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка тестирования: {e}")
        sys.exit(1)