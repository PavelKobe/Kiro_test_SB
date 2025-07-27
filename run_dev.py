#!/usr/bin/env python3
"""
Скрипт для запуска Flask приложения в режиме разработки
"""

import os
import sys
from pathlib import Path

def main():
    """Запуск Flask приложения"""
    
    # Устанавливаем переменные окружения
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # Проверяем наличие .env файла
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  Файл .env не найден. Создайте его на основе .env.example")
        return False
    
    # Проверяем подключение к БД
    try:
        import psycopg2
        from dotenv import load_dotenv
        load_dotenv()
        
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '1234'),
            database=os.getenv('DB_NAME', 'stockmann_incidents')
        )
        conn.close()
        print("✅ База данных доступна")
        
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        print("Запустите: python database/load_basic_data.py")
        return False
    
    # Запускаем приложение
    print("🚀 Запуск Flask приложения...")
    print("📍 Адрес: http://127.0.0.1:5000")
    print("🔐 Логин: admin / Пароль: 12345")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено")
    except Exception as e:
        print(f"❌ Ошибка запуска: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)