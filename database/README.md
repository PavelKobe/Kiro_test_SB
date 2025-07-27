# База данных системы управления инцидентами Stockmann

## Обзор

Схема базы данных разработана специально для торговой сети Stockmann и учитывает:
- Многострановую структуру (Финляндия, Эстония, Латвия)
- Различные типы магазинов (универмаги, аутлеты, онлайн)
- Отделы и секции магазинов
- Специфику ритейла и обслуживания клиентов

## Структура базы данных

### Основные таблицы

#### Географическая структура
- **countries** - Страны присутствия Stockmann
- **cities** - Города с магазинами
- **stores** - Магазины и торговые точки
- **departments** - Отделы магазинов
- **store_departments** - Связь магазинов и отделов

#### Пользователи и роли
- **users** - Сотрудники системы
- **work_shifts** - Рабочие смены

#### Система инцидентов
- **incident_categories** - Категории инцидентов
- **incident_subcategories** - Подкатегории с SLA
- **incidents** - Основная таблица инцидентов
- **incident_history** - История изменений
- **incident_comments** - Комментарии
- **incident_attachments** - Файлы и вложения
- **incident_relations** - Связи между инцидентами
- **incident_escalations** - Эскалации

#### Управление и отчетность
- **sla_rules** - Правила SLA
- **notifications** - Уведомления

## Категории инцидентов

### TECH - Технические проблемы
- **POS_DOWN** - Касса не работает (SLA: 2 часа)
- **NETWORK** - Проблемы с сетью (SLA: 4 часа)
- **PRINTER** - Принтер не работает (SLA: 8 часов)
- **SYSTEM_SLOW** - Система работает медленно (SLA: 24 часа)

### SAFETY - Безопасность
- **THEFT** - Кража (SLA: 1 час)
- **ACCIDENT** - Несчастный случай (SLA: 1 час)
- **FIRE_ALARM** - Пожарная сигнализация (SLA: 30 минут)
- **SUSPICIOUS** - Подозрительная активность (SLA: 2 часа)

### CUSTOMER - Обслуживание клиентов
- **COMPLAINT** - Жалоба клиента (SLA: 24 часа)
- **REFUND** - Проблемы с возвратом (SLA: 8 часов)
- **LOST_FOUND** - Потерянные вещи (SLA: 48 часов)

### STAFF - Персонал
- **ABSENCE** - Отсутствие сотрудника (SLA: 4 часа)
- **CONFLICT** - Конфликт (SLA: 24 часа)
- **TRAINING** - Обучение (SLA: 72 часа)

### FACILITY - Помещения
- **CLEANING** - Уборка (SLA: 4 часа)
- **HVAC** - Климат (SLA: 8 часов)
- **LIGHTING** - Освещение (SLA: 12 часов)
- **ELEVATOR** - Лифт (SLA: 2 часа)

### INVENTORY - Товары
- **DAMAGED** - Поврежденный товар (SLA: 24 часа)
- **MISSING** - Недостача (SLA: 8 часов)
- **DELIVERY** - Проблемы с поставкой (SLA: 48 часов)

### FINANCE - Финансы
- **CASH_DIFF** - Расхождение в кассе (SLA: 4 часа)
- **CARD_ISSUE** - Проблемы с картами (SLA: 2 часа)

## Приоритеты и серьезность

### Приоритеты (Priority)
- **low** - Низкий
- **medium** - Средний (по умолчанию)
- **high** - Высокий
- **critical** - Критический

### Серьезность (Severity)
- **minor** - Незначительная (по умолчанию)
- **major** - Значительная
- **critical** - Критическая

## Статусы инцидентов

- **new** - Новый (по умолчанию)
- **assigned** - Назначен
- **in_progress** - В работе
- **resolved** - Решен
- **closed** - Закрыт
- **cancelled** - Отменен

## Роли пользователей

- **admin** - Администратор системы
- **manager** - Менеджер магазина
- **user** - Обычный пользователь
- **security** - Служба безопасности

## Автоматические функции

### Генерация номеров инцидентов
Формат: `STORE-YYYY-NNNN`
Пример: `HEL001-2025-0001`

### Расчет SLA
Автоматический расчет крайних сроков на основе:
- Категории и подкатегории
- Приоритета и серьезности
- Настроенных правил SLA

### Триггеры обновления
- Автоматическое обновление `updated_at`
- Отслеживание изменений в истории

## Установка и настройка

### 1. Настройка переменных окружения

Создайте файл `.env`:
```env
DB_NAME=stockmann_incidents
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 2. Инициализация базы данных

```bash
# Установка зависимостей
pip install psycopg2-binary python-dotenv

# Инициализация БД
python database/init_db.py
```

### 3. Ручная установка

```sql
-- Создание базы данных
CREATE DATABASE stockmann_incidents;

-- Выполнение схемы
\i database/stockmann_schema.sql

-- Загрузка тестовых данных
\i database/test_data.sql
```

## Примеры запросов

### Статистика по магазинам
```sql
SELECT 
    s.name as store_name,
    COUNT(i.id) as total_incidents,
    COUNT(CASE WHEN i.status IN ('new', 'assigned', 'in_progress') THEN 1 END) as active_incidents,
    COUNT(CASE WHEN i.sla_breached = true THEN 1 END) as overdue_incidents
FROM stores s
LEFT JOIN incidents i ON s.id = i.store_id
GROUP BY s.id, s.name
ORDER BY total_incidents DESC;
```

### Просроченные инциденты
```sql
SELECT 
    i.incident_number,
    i.title,
    s.name as store_name,
    ic.name as category,
    i.sla_deadline,
    EXTRACT(EPOCH FROM (NOW() - i.sla_deadline))/3600 as hours_overdue
FROM incidents i
JOIN stores s ON i.store_id = s.id
JOIN incident_categories ic ON i.category_id = ic.id
WHERE i.sla_deadline < NOW() 
  AND i.status NOT IN ('resolved', 'closed', 'cancelled')
ORDER BY hours_overdue DESC;
```

### Рабочая нагрузка пользователей
```sql
SELECT 
    u.first_name || ' ' || u.last_name as user_name,
    u.position,
    s.name as store_name,
    COUNT(i.id) as assigned_incidents,
    COUNT(CASE WHEN i.priority = 'critical' THEN 1 END) as critical_incidents
FROM users u
LEFT JOIN incidents i ON u.id = i.assigned_to AND i.status IN ('assigned', 'in_progress')
LEFT JOIN stores s ON u.store_id = s.id
WHERE u.is_active = true
GROUP BY u.id, u.first_name, u.last_name, u.position, s.name
ORDER BY assigned_incidents DESC;
```

## Индексы для производительности

Созданы индексы для оптимизации часто используемых запросов:
- По магазинам и статусам инцидентов
- По датам создания и обновления
- По назначенным пользователям
- По категориям и приоритетам

## Расширение схемы

### Добавление новых категорий
```sql
INSERT INTO incident_categories (code, name, description, color) 
VALUES ('NEW_CAT', 'Новая категория', 'Описание', '#FF0000');

INSERT INTO incident_subcategories (category_id, code, name, sla_hours) 
VALUES (currval('incident_categories_id_seq'), 'SUB_CODE', 'Подкатегория', 24);
```

### Добавление новых магазинов
```sql
-- Добавить страну (если нужно)
INSERT INTO countries (code, name) VALUES ('LTU', 'Литва');

-- Добавить город
INSERT INTO cities (country_id, name) VALUES (4, 'Вильнюс');

-- Добавить магазин
INSERT INTO stores (code, name, address, city_id, store_type, manager_name) 
VALUES ('VIL001', 'Stockmann Vilnius', 'Gedimino pr. 9', 8, 'department_store', 'Менеджер');
```

## Мониторинг и обслуживание

### Регулярные задачи
- Архивация старых инцидентов
- Очистка истории изменений
- Обновление статистики
- Проверка нарушений SLA

### Резервное копирование
```bash
# Создание бэкапа
pg_dump stockmann_incidents > backup_$(date +%Y%m%d).sql

# Восстановление
psql stockmann_incidents < backup_20250127.sql
```