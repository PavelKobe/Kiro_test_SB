#!/usr/bin/env python3
"""
Проверка связей между магазинами и отделами
"""

import sys
import os
from pathlib import Path

# Добавляем путь к моделям
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from flask import Flask
from stockmann_models import db, Store, Department, StoreDepartment

def check_relations():
    """Проверяет связи между магазинами и отделами"""
    
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
            print("🔗 Проверка связей магазинов и отделов:")
            print("-" * 50)
            
            # Проверяем связи
            relations = StoreDepartment.query.all()
            print(f"📊 Всего связей: {len(relations)}")
            
            # Проверяем каждый магазин
            stores = Store.query.all()
            for store in stores[:5]:  # Первые 5 магазинов
                departments = store.departments.all()
                print(f"\n🏪 {store.code} ({store.name[:30]}...):")
                print(f"   Отделов: {len(departments)}")
                
                if len(departments) == 0:
                    print("   ❌ Нет связанных отделов!")
                else:
                    for dept in departments[:3]:  # Первые 3 отдела
                        print(f"   - {dept.name}")
                    if len(departments) > 3:
                        print(f"   ... и еще {len(departments) - 3}")
            
            # Если связей нет, создаем базовые
            if len(relations) == 0:
                print("\n❌ Связи не найдены! Создаем базовые связи...")
                
                # Получаем первые несколько магазинов и отделов
                stores = Store.query.limit(5).all()
                departments = Department.query.limit(10).all()
                
                # Создаем связи для каждого магазина
                for store in stores:
                    # Для больших магазинов - все отделы
                    if store.area_sqm and store.area_sqm > 8000:
                        store_departments = departments
                    # Для средних - основные отделы
                    elif store.area_sqm and store.area_sqm > 5000:
                        store_departments = departments[:7]
                    # Для маленьких - базовые отделы
                    else:
                        store_departments = departments[:4]
                    
                    for dept in store_departments:
                        relation = StoreDepartment(store_id=store.id, department_id=dept.id)
                        db.session.add(relation)
                
                db.session.commit()
                print("✅ Базовые связи созданы!")
                
                # Проверяем снова
                for store in stores:
                    departments = store.departments.all()
                    print(f"   {store.code}: {len(departments)} отделов")
            
            return True
                
        except Exception as e:
            print(f"❌ Ошибка при проверке связей: {e}")
            return False

if __name__ == '__main__':
    success = check_relations()
    sys.exit(0 if success else 1)