#!/usr/bin/env python3
"""
Скрипт проверки данных в базе
"""

import sys
import os
from pathlib import Path

# Добавляем путь к моделям
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from flask import Flask
from stockmann_models import db, Store, IncidentCategory, IncidentSubcategory, Department, User

def check_data():
    """Проверяет наличие данных в базе"""
    
    app = Flask(__name__)
    
    # Настройка подключения к базе данных
    from dotenv import load_dotenv
    load_dotenv()
    
    db_name = os.getenv('DB_NAME', 'stockmann_incidents')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '1234')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            print("📊 Проверка данных в базе:")
            print("-" * 40)
            
            # Проверяем магазины
            stores = Store.query.all()
            print(f"🏪 Магазины: {len(stores)}")
            for store in stores[:5]:  # Показываем первые 5
                print(f"   - {store.code}: {store.name}")
            if len(stores) > 5:
                print(f"   ... и еще {len(stores) - 5}")
            
            # Проверяем категории
            categories = IncidentCategory.query.all()
            print(f"\n📂 Категории: {len(categories)}")
            for cat in categories[:5]:
                print(f"   - {cat.code}: {cat.name}")
            if len(categories) > 5:
                print(f"   ... и еще {len(categories) - 5}")
            
            # Проверяем подкатегории
            subcategories = IncidentSubcategory.query.all()
            print(f"\n📋 Подкатегории: {len(subcategories)}")
            for subcat in subcategories[:5]:
                print(f"   - {subcat.code}: {subcat.name} (SLA: {subcat.sla_hours}ч)")
            if len(subcategories) > 5:
                print(f"   ... и еще {len(subcategories) - 5}")
            
            # Проверяем отделы
            departments = Department.query.all()
            print(f"\n🏬 Отделы: {len(departments)}")
            for dept in departments[:5]:
                print(f"   - {dept.code}: {dept.name}")
            if len(departments) > 5:
                print(f"   ... и еще {len(departments) - 5}")
            
            # Проверяем пользователей
            users = User.query.all()
            print(f"\n👥 Пользователи: {len(users)}")
            for user in users[:5]:
                print(f"   - {user.username}: {user.full_name} ({user.role})")
            if len(users) > 5:
                print(f"   ... и еще {len(users) - 5}")
            
            print("\n" + "=" * 40)
            
            if len(stores) == 0 or len(categories) == 0:
                print("❌ Данные не загружены! Запустите:")
                print("   python database/load_basic_data.py")
                return False
            else:
                print("✅ Данные загружены корректно!")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка при проверке данных: {e}")
            return False

if __name__ == '__main__':
    success = check_data()
    sys.exit(0 if success else 1)