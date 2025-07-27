#!/usr/bin/env python3
"""
Тест создания инцидента
"""

import sys
import os
from pathlib import Path

# Добавляем путь к моделям
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from flask import Flask
from stockmann_models import db, Store, IncidentCategory, IncidentSubcategory, Incident, IncidentHistory
from datetime import datetime

def test_incident_creation():
    """Тестирует создание инцидента"""
    
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
            print("🧪 Тестирование создания инцидента...")
            
            # Получаем тестовые данные
            store = Store.query.first()
            category = IncidentCategory.query.first()
            subcategory = IncidentSubcategory.query.first()
            
            if not store or not category:
                print("❌ Нет тестовых данных в базе")
                return False
            
            print(f"📍 Магазин: {store.code} - {store.name}")
            print(f"📂 Категория: {category.name}")
            if subcategory:
                print(f"📋 Подкатегория: {subcategory.name} (SLA: {subcategory.sla_hours}ч)")
            
            # Генерируем номер инцидента
            current_year = datetime.now().year
            
            # Ищем последний номер для данного магазина и года
            last_incident = db.session.query(Incident).filter(
                Incident.incident_number.like(f"{store.code}-{current_year}-%")
            ).order_by(Incident.incident_number.desc()).first()
            
            if last_incident and last_incident.incident_number:
                parts = last_incident.incident_number.split('-')
                if len(parts) >= 3:
                    try:
                        last_num = int(parts[-1])
                        next_num = last_num + 1
                    except ValueError:
                        next_num = 1
                else:
                    next_num = 1
            else:
                next_num = 1
            
            incident_number = f"{store.code}-{current_year}-{next_num:04d}"
            print(f"🔢 Сгенерированный номер: {incident_number}")
            
            # Создаем инцидент
            incident = Incident(
                incident_number=incident_number,
                title="Тестовый инцидент",
                description="Это тестовый инцидент для проверки работы системы",
                category_id=category.id,
                subcategory_id=subcategory.id if subcategory else None,
                priority='medium',
                severity='minor',
                store_id=store.id,
                reporter_id=1,
                customer_affected=False,
                source='manual'
            )
            
            # Устанавливаем время создания явно
            incident.created_at = datetime.utcnow()
            incident.updated_at = datetime.utcnow()
            
            # Рассчитываем SLA
            if subcategory:
                from datetime import timedelta
                incident.sla_deadline = incident.created_at + timedelta(hours=subcategory.sla_hours)
            
            db.session.add(incident)
            db.session.commit()
            
            print(f"✅ Инцидент создан с ID: {incident.id}")
            print(f"📅 Создан: {incident.created_at}")
            if incident.sla_deadline:
                print(f"⏰ SLA крайний срок: {incident.sla_deadline}")
            
            # Создаем запись в истории
            history = IncidentHistory(
                incident_id=incident.id,
                changed_by=1,
                field_name='status',
                old_value=None,
                new_value='new',
                change_reason='Инцидент создан (тест)'
            )
            db.session.add(history)
            db.session.commit()
            
            print("📝 Запись в истории создана")
            
            # Проверяем созданный инцидент
            created_incident = Incident.query.get(incident.id)
            print(f"\n📊 Проверка созданного инцидента:")
            print(f"   Номер: {created_incident.incident_number}")
            print(f"   Заголовок: {created_incident.title}")
            print(f"   Статус: {created_incident.status}")
            print(f"   Магазин: {created_incident.store.name}")
            print(f"   Категория: {created_incident.category.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при создании инцидента: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = test_incident_creation()
    sys.exit(0 if success else 1)