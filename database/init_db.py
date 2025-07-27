#!/usr/bin/env python3
"""
Скрипт инициализации базы данных для системы управления инцидентами Stockmann
"""

import os
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from flask import Flask
sys.path.append(str(Path(__file__).parent.parent / 'models'))
from stockmann_models import db
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database_if_not_exists():
    """Создает базу данных, если она не существует"""
    db_name = os.getenv('DB_NAME', 'stockmann_incidents')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    
    try:
        # Подключаемся к PostgreSQL без указания базы данных
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        
        # Проверяем, существует ли база данных
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Создание базы данных '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"База данных '{db_name}' создана успешно!")
        else:
            print(f"База данных '{db_name}' уже существует.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        return False
    
    return True

def init_database():
    """Инициализирует структуру базы данных"""
    app = Flask(__name__)
    
    # Настройка подключения к базе данных
    db_name = os.getenv('DB_NAME', 'stockmann_incidents')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            print("Создание таблиц...")
            db.create_all()
            print("Таблицы созданы успешно!")
            
            # Выполняем SQL скрипт для создания триггеров и функций
            schema_file = Path(__file__).parent / 'stockmann_schema.sql'
            if schema_file.exists():
                print("Выполнение дополнительных SQL команд...")
                with open(schema_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                # Разделяем на отдельные команды
                commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
                
                for cmd in commands:
                    if cmd.upper().startswith(('CREATE TRIGGER', 'CREATE OR REPLACE FUNCTION', 'CREATE INDEX')):
                        try:
                            db.session.execute(cmd)
                            db.session.commit()
                        except Exception as e:
                            print(f"Предупреждение при выполнении команды: {e}")
                            db.session.rollback()
            
            return True
            
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            return False

def load_test_data():
    """Загружает тестовые данные"""
    test_data_file = Path(__file__).parent / 'test_data.sql'
    
    if not test_data_file.exists():
        print("Файл с тестовыми данными не найден.")
        return False
    
    try:
        print("Загрузка тестовых данных...")
        
        db_name = os.getenv('DB_NAME', 'stockmann_incidents')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', 'password')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        cursor = conn.cursor()
        
        with open(test_data_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Выполняем SQL команды
        cursor.execute(sql_content)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("Тестовые данные загружены успешно!")
        return True
        
    except Exception as e:
        print(f"Ошибка при загрузке тестовых данных: {e}")
        return False

def main():
    """Основная функция инициализации"""
    print("=== Инициализация базы данных Stockmann Incidents ===")
    
    # Проверяем переменные окружения
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        print("Используются значения по умолчанию.")
    
    # Создаем базу данных
    if not create_database_if_not_exists():
        print("Не удалось создать базу данных. Завершение.")
        return False
    
    # Инициализируем структуру
    if not init_database():
        print("Не удалось создать структуру базы данных. Завершение.")
        return False
    
    # Загружаем тестовые данные
    load_test = input("Загрузить тестовые данные? (y/N): ").lower().strip()
    if load_test in ['y', 'yes', 'да']:
        if not load_test_data():
            print("Не удалось загрузить тестовые данные.")
        else:
            print("\n=== Тестовые учетные записи ===")
            print("admin / admin123 - Системный администратор")
            print("anna.virtanen / password - Менеджер магазина Helsinki")
            print("security.hel / security123 - Служба безопасности")
    
    print("\n=== Инициализация завершена ===")
    print(f"База данных: {os.getenv('DB_NAME', 'stockmann_incidents')}")
    print(f"Хост: {os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}")
    
    return True

if __name__ == '__main__':
    # Загружаем переменные окружения из .env файла
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Установите python-dotenv для загрузки переменных окружения")
    
    success = main()
    sys.exit(0 if success else 1)