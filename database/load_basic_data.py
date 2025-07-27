#!/usr/bin/env python3
"""
Скрипт загрузки базовых данных для тестирования форм
"""

import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def load_basic_data():
    """Загружает минимальные данные для работы форм"""
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
        
        # Очищаем существующие данные
        print("Очистка существующих данных...")
        cursor.execute("TRUNCATE TABLE countries, cities, stores, departments, users, incident_categories, incident_subcategories RESTART IDENTITY CASCADE")
        
        # Базовые данные
        print("Загрузка базовых данных...")
        
        # Страны
        cursor.execute("""
            INSERT INTO countries (code, name) VALUES 
            ('FIN', 'Финляндия'),
            ('EST', 'Эстония'),
            ('LVA', 'Латвия')
        """)
        
        # Города
        cursor.execute("""
            INSERT INTO cities (country_id, name, region) VALUES 
            (1, 'Хельсинки', 'Уусимаа'),
            (1, 'Тампере', 'Пирканмаа'),
            (1, 'Турку', 'Варсинайс-Суоми'),
            (1, 'Эспоо', 'Уусимаа'),
            (1, 'Оулу', 'Северная Остроботния'),
            (2, 'Таллин', 'Харьюмаа'),
            (2, 'Тарту', 'Тартумаа'),
            (2, 'Пярну', 'Пярнумаа'),
            (3, 'Рига', 'Рижский край'),
            (3, 'Даугавпилс', 'Латгалия'),
            (3, 'Лиепая', 'Курземе')
        """)
        
        # Магазины
        cursor.execute("""
            INSERT INTO stores (code, name, address, city_id, store_type, area_sqm, phone, email, manager_name, opened_date) VALUES 
            ('HEL001', 'Stockmann Helsinki Keskusta', 'Aleksanterinkatu 52, Helsinki', 1, 'department_store', 15000, '+358-9-121-4211', 'helsinki@stockmann.com', 'Анна Виртанен', '1962-09-01'),
            ('TAM001', 'Stockmann Tampere', 'Hämeenkatu 4, Tampere', 2, 'department_store', 8000, '+358-3-212-1111', 'tampere@stockmann.com', 'Микко Лехтинен', '1985-03-15'),
            ('TUR001', 'Stockmann Turku', 'Yliopistonkatu 22, Turku', 3, 'department_store', 6000, '+358-2-267-8111', 'turku@stockmann.com', 'Лиза Коскинен', '1990-11-20'),
            ('ESP001', 'Stockmann Espoo', 'Piispansilta 11, Espoo', 4, 'department_store', 7500, '+358-9-8520-1000', 'espoo@stockmann.com', 'Петра Лаакконен', '2005-10-15'),
            ('OUL001', 'Stockmann Oulu', 'Kirkkokatu 3, Oulu', 5, 'department_store', 5500, '+358-8-5584-1000', 'oulu@stockmann.com', 'Сату Ниеми', '2001-09-05'),
            ('TAL001', 'Stockmann Tallinn', 'Liivalaia 53, Tallinn', 6, 'department_store', 12000, '+372-631-9500', 'tallinn@stockmann.ee', 'Кристина Мяги', '1995-05-10'),
            ('TAR001', 'Stockmann Tartu', 'Rüütli 2, Tartu', 7, 'outlet', 2500, '+372-730-9000', 'tartu@stockmann.ee', 'Мартин Кивистик', '2015-04-20'),
            ('PAR001', 'Stockmann Pärnu', 'Rüütli 14, Pärnu', 8, 'department_store', 3500, '+372-447-9000', 'parnu@stockmann.ee', 'Кадри Тамм', '2012-06-15'),
            ('RIG001', 'Stockmann Riga', 'Dzirnavu iela 67, Riga', 9, 'department_store', 10000, '+371-6728-5555', 'riga@stockmann.lv', 'Инга Калниня', '1997-09-12'),
            ('DAU001', 'Stockmann Daugavpils', 'Rigas iela 20, Daugavpils', 10, 'outlet', 3000, '+371-6542-5000', 'daugavpils@stockmann.lv', 'Артурс Озолс', '2010-08-15'),
            ('LIE001', 'Stockmann Liepāja', 'Graudu iela 27/29, Liepāja', 11, 'outlet', 2800, '+371-6342-5000', 'liepaja@stockmann.lv', 'Лига Озолиня', '2013-08-10')
        """)
        
        # Отделы
        cursor.execute("""
            INSERT INTO departments (code, name, description, floor_number) VALUES 
            ('WOMEN', 'Женская одежда', 'Женская одежда и аксессуары', 1),
            ('MEN', 'Мужская одежда', 'Мужская одежда и аксессуары', 2),
            ('CHILD', 'Детская одежда', 'Детская одежда и игрушки', 3),
            ('BEAUTY', 'Красота', 'Косметика и парфюмерия', 1),
            ('HOME', 'Дом', 'Товары для дома и интерьера', 4),
            ('FOOD', 'Продукты', 'Деликатесы и продукты питания', -1),
            ('SHOES', 'Обувь', 'Обувь для всей семьи', 2),
            ('BAGS', 'Сумки', 'Сумки и кожгалантерея', 1),
            ('JEWELRY', 'Ювелирные изделия', 'Украшения и часы', 1),
            ('SPORT', 'Спорт', 'Спортивная одежда и товары', 3),
            ('LUXURY', 'Люкс', 'Премиальные бренды и дизайнерская одежда', 2),
            ('LINGERIE', 'Нижнее белье', 'Женское и мужское нижнее белье', 1),
            ('ELECTRONICS', 'Электроника', 'Бытовая техника и гаджеты', 5),
            ('BOOKS', 'Книги', 'Книги, журналы, канцелярия', 4),
            ('CAFE', 'Кафе', 'Кафе и ресторан в магазине', 1)
        """)
        
        # Пользователи
        cursor.execute("""
            INSERT INTO users (username, email, first_name, last_name, phone, position, store_id, role) VALUES 
            ('admin', 'admin@stockmann.com', 'Системный', 'Администратор', '+358-40-123-4567', 'IT Administrator', NULL, 'admin'),
            ('anna.virtanen', 'anna.virtanen@stockmann.com', 'Анна', 'Виртанен', '+358-40-111-2222', 'Store Manager', 1, 'manager'),
            ('mikko.lehtinen', 'mikko.lehtinen@stockmann.com', 'Микко', 'Лехтинен', '+358-40-333-4444', 'Store Manager', 2, 'manager'),
            ('petra.laakkonen', 'petra.laakkonen@stockmann.com', 'Петра', 'Лаакконен', '+358-40-201-1111', 'Store Manager', 4, 'manager'),
            ('satu.niemi', 'satu.niemi@stockmann.com', 'Сату', 'Ниеми', '+358-40-203-3333', 'Store Manager', 5, 'manager'),
            ('kristina.magi', 'kristina.magi@stockmann.ee', 'Кристина', 'Мяги', '+372-555-1234', 'Store Manager', 6, 'manager'),
            ('inga.kalnina', 'inga.kalnina@stockmann.lv', 'Инга', 'Калниня', '+371-222-3333', 'Store Manager', 9, 'manager'),
            ('security.hel', 'security.helsinki@stockmann.com', 'Охрана', 'Хельсинки', '+358-40-555-6666', 'Security Officer', 1, 'security'),
            ('sales.women', 'sales.women@stockmann.com', 'Мария', 'Коскинен', '+358-40-777-8888', 'Sales Associate', 1, 'user'),
            ('tech.support', 'tech.support@stockmann.com', 'Техническая', 'Поддержка', '+358-40-999-0000', 'Technical Support', NULL, 'user')
        """)
        
        # Категории инцидентов
        cursor.execute("""
            INSERT INTO incident_categories (code, name, description, color) VALUES 
            ('TECH', 'Технические проблемы', 'Проблемы с оборудованием и IT системами', '#FF6B6B'),
            ('SAFETY', 'Безопасность', 'Вопросы безопасности и охраны', '#FF8E53'),
            ('CUSTOMER', 'Обслуживание клиентов', 'Жалобы и проблемы клиентов', '#4ECDC4'),
            ('STAFF', 'Персонал', 'Вопросы, связанные с персоналом', '#45B7D1'),
            ('FACILITY', 'Помещения', 'Проблемы с помещениями и инфраструктурой', '#96CEB4'),
            ('INVENTORY', 'Товары', 'Проблемы с товарами и инвентарем', '#FFEAA7'),
            ('FINANCE', 'Финансы', 'Финансовые вопросы и кассовые операции', '#DDA0DD'),
            ('DELIVERY', 'Доставка', 'Проблемы с доставкой товаров клиентам', '#9B59B6'),
            ('MARKETING', 'Маркетинг', 'Проблемы с рекламой и маркетинговыми акциями', '#E67E22'),
            ('QUALITY', 'Качество', 'Проблемы с качеством товаров и услуг', '#E74C3C'),
            ('SUPPLIER', 'Поставщики', 'Проблемы с поставщиками и партнерами', '#F39C12'),
            ('COMMUNICATION', 'Коммуникации', 'Проблемы внутренних и внешних коммуникаций', '#1ABC9C')
        """)
        
        # Подкатегории инцидентов
        cursor.execute("""
            INSERT INTO incident_subcategories (category_id, code, name, description, sla_hours) VALUES 
            -- Технические проблемы
            (1, 'POS_DOWN', 'Касса не работает', 'Проблемы с кассовым оборудованием', 2),
            (1, 'NETWORK', 'Проблемы с сетью', 'Отсутствие интернета или сетевые проблемы', 4),
            (1, 'PRINTER', 'Принтер не работает', 'Проблемы с принтерами чеков или этикеток', 8),
            (1, 'SYSTEM_SLOW', 'Система работает медленно', 'Медленная работа IT систем', 24),
            
            -- Безопасность
            (2, 'THEFT', 'Кража', 'Случаи кражи товаров или имущества', 1),
            (2, 'ACCIDENT', 'Несчастный случай', 'Травмы клиентов или сотрудников', 1),
            (2, 'FIRE_ALARM', 'Пожарная сигнализация', 'Срабатывание пожарной сигнализации', 0.5),
            (2, 'SUSPICIOUS', 'Подозрительная активность', 'Подозрительное поведение посетителей', 2),
            
            -- Обслуживание клиентов
            (3, 'COMPLAINT', 'Жалоба клиента', 'Жалобы на обслуживание или товары', 24),
            (3, 'REFUND', 'Проблемы с возвратом', 'Сложности при возврате товаров', 8),
            (3, 'LOST_FOUND', 'Потерянные вещи', 'Потерянные или найденные вещи', 48),
            
            -- Персонал
            (4, 'ABSENCE', 'Отсутствие сотрудника', 'Незапланированное отсутствие', 4),
            (4, 'CONFLICT', 'Конфликт', 'Конфликты между сотрудниками', 24),
            (4, 'TRAINING', 'Обучение', 'Вопросы обучения персонала', 72),
            
            -- Помещения
            (5, 'CLEANING', 'Уборка', 'Проблемы с чистотой помещений', 4),
            (5, 'HVAC', 'Климат', 'Проблемы с отоплением/кондиционированием', 8),
            (5, 'LIGHTING', 'Освещение', 'Проблемы с освещением', 12),
            (5, 'ELEVATOR', 'Лифт', 'Неисправности лифтов', 2),
            
            -- Товары
            (6, 'DAMAGED', 'Поврежденный товар', 'Обнаружение поврежденных товаров', 24),
            (6, 'MISSING', 'Недостача', 'Недостача товаров', 8),
            (6, 'DELIVERY', 'Проблемы с поставкой', 'Задержки или проблемы с поставками', 48),
            
            -- Финансы
            (7, 'CASH_DIFF', 'Расхождение в кассе', 'Недостача или излишек в кассе', 4),
            (7, 'CARD_ISSUE', 'Проблемы с картами', 'Проблемы с оплатой картами', 2),
            
            -- Доставка
            (8, 'LATE_DELIVERY', 'Задержка доставки', 'Доставка товара с опозданием', 24),
            (8, 'DAMAGED_DELIVERY', 'Повреждение при доставке', 'Товар поврежден во время доставки', 8),
            (8, 'WRONG_ADDRESS', 'Неверный адрес', 'Доставка по неправильному адресу', 12),
            
            -- Маркетинг
            (9, 'WRONG_PRICE', 'Неверная цена', 'Ошибка в ценнике или рекламе', 2),
            (9, 'AD_COMPLAINT', 'Жалоба на рекламу', 'Жалобы клиентов на рекламные материалы', 24),
            (9, 'PROMO_ERROR', 'Ошибка в акции', 'Технические проблемы с промо-акциями', 4),
            
            -- Качество
            (10, 'DEFECTIVE_PRODUCT', 'Бракованный товар', 'Товар с производственным браком', 8),
            (10, 'SIZE_ISSUE', 'Проблемы с размерами', 'Несоответствие размеров товара', 12),
            (10, 'COLOR_DIFFERENCE', 'Расхождение цвета', 'Цвет товара не соответствует описанию', 24),
            
            -- Поставщики
            (11, 'LATE_SUPPLY', 'Задержка поставки', 'Поставщик задерживает поставку', 24),
            (11, 'QUALITY_SUPPLY', 'Качество поставки', 'Низкое качество поставленных товаров', 12),
            (11, 'CONTRACT_SUPPLY', 'Договорные вопросы', 'Проблемы с договором поставки', 48),
            
            -- Коммуникации
            (12, 'INTERNAL_COMM', 'Внутренние коммуникации', 'Проблемы внутренней связи', 8),
            (12, 'EXTERNAL_COMM', 'Внешние коммуникации', 'Проблемы связи с клиентами/партнерами', 4),
            (12, 'LANGUAGE_BARRIER', 'Языковой барьер', 'Проблемы из-за языковых различий', 12)
        """)
        
        # Связи магазинов и отделов (основные)
        cursor.execute("""
            INSERT INTO store_departments (store_id, department_id) VALUES 
            -- Helsinki (все отделы)
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15),
            -- Tampere (основные отделы)
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 7), (2, 8), (2, 11),
            -- Turku (основные отделы)
            (3, 1), (3, 2), (3, 4), (3, 5), (3, 7), (3, 11),
            -- Espoo (большой магазин)
            (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 7), (4, 8), (4, 11), (4, 12), (4, 13), (4, 15),
            -- Oulu (средний магазин)
            (5, 1), (5, 2), (5, 4), (5, 5), (5, 7), (5, 11),
            -- Tallinn (большой магазин)
            (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 11),
            -- Tartu (аутлет)
            (7, 1), (7, 2), (7, 7),
            -- Pärnu (средний магазин)
            (8, 1), (8, 2), (8, 4), (8, 5), (8, 7), (8, 11),
            -- Riga (большой магазин)
            (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 7), (9, 8), (9, 9), (9, 11),
            -- Daugavpils (аутлет)
            (10, 1), (10, 2), (10, 7),
            -- Liepāja (аутлет)
            (11, 1), (11, 2), (11, 7)
        """)
        
        conn.commit()
        
        # Показываем статистику
        cursor.execute("SELECT COUNT(*) FROM stores")
        stores_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incident_categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM incident_subcategories")
        subcategories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        print(f"\n✅ Базовые данные загружены успешно!")
        print(f"\n📊 Статистика:")
        print(f"🏪 Магазины: {stores_count}")
        print(f"📂 Категории: {categories_count}")
        print(f"📋 Подкатегории: {subcategories_count}")
        print(f"👥 Пользователи: {users_count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при загрузке данных: {e}")
        return False

if __name__ == '__main__':
    success = load_basic_data()
    sys.exit(0 if success else 1)