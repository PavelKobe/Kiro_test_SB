#!/usr/bin/env python3
"""
Скрипт загрузки дополнительных данных для системы Stockmann
"""

import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def load_additional_data():
    """Загружает дополнительные данные в базу"""
    try:
        print("Подключение к базе данных...")
        
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '1234'),
            database=os.getenv('DB_NAME', 'stockmann_incidents')
        )
        
        cursor = conn.cursor()
        
        # Читаем SQL файл
        sql_file = Path(__file__).parent / 'additional_data.sql'
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("Загрузка дополнительных данных...")
        cursor.execute(sql_content)
        conn.commit()
        
        print("✅ Дополнительные данные загружены успешно!")
        
        # Показываем статистику
        cursor.execute("SELECT COUNT(*) FROM stores")
        stores_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incident_categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incident_subcategories")
        subcategories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        print(f"\n📊 Статистика данных:")
        print(f"Магазины: {stores_count}")
        print(f"Категории: {categories_count}")
        print(f"Подкатегории: {subcategories_count}")
        print(f"Пользователи: {users_count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке данных: {e}")
        return False

if __name__ == '__main__':
    success = load_additional_data()
    sys.exit(0 if success else 1)