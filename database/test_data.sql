-- Тестовые данные для системы управления инцидентами Stockmann

-- Страны
INSERT INTO countries (code, name) VALUES 
('FIN', 'Финляндия'),
('EST', 'Эстония'),
('LVA', 'Латвия');

-- Города
INSERT INTO cities (country_id, name, region) VALUES 
(1, 'Хельсинки', 'Уусимаа'),
(1, 'Тампере', 'Пирканмаа'),
(1, 'Турку', 'Варсинайс-Суоми'),
(2, 'Таллин', 'Харьюмаа'),
(2, 'Тарту', 'Тартумаа'),
(3, 'Рига', 'Рижский край'),
(3, 'Даугавпилс', 'Латгалия');

-- Магазины
INSERT INTO stores (code, name, address, city_id, store_type, area_sqm, phone, email, manager_name, opened_date) VALUES 
('HEL001', 'Stockmann Helsinki Keskusta', 'Aleksanterinkatu 52, Helsinki', 1, 'department_store', 15000, '+358-9-121-4211', 'helsinki@stockmann.com', 'Анна Виртанен', '1962-09-01'),
('TAM001', 'Stockmann Tampere', 'Hämeenkatu 4, Tampere', 2, 'department_store', 8000, '+358-3-212-1111', 'tampere@stockmann.com', 'Микко Лехтинен', '1985-03-15'),
('TUR001', 'Stockmann Turku', 'Yliopistonkatu 22, Turku', 3, 'department_store', 6000, '+358-2-267-8111', 'turku@stockmann.com', 'Лиза Коскинен', '1990-11-20'),
('TAL001', 'Stockmann Tallinn', 'Liivalaia 53, Tallinn', 4, 'department_store', 12000, '+372-631-9500', 'tallinn@stockmann.ee', 'Кристина Мяги', '1995-05-10'),
('RIG001', 'Stockmann Riga', 'Dzirnavu iela 67, Riga', 6, 'department_store', 10000, '+371-6728-5555', 'riga@stockmann.lv', 'Инга Калниня', '1997-09-12'),
('HEL002', 'Stockmann Outlet Helsinki', 'Itäkeskus, Helsinki', 1, 'outlet', 3000, '+358-9-345-6789', 'outlet.helsinki@stockmann.com', 'Юха Ниеми', '2010-04-01');

-- Отделы
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
('SPORT', 'Спорт', 'Спортивная одежда и товары', 3);

-- Связь магазинов и отделов
INSERT INTO store_departments (store_id, department_id) VALUES 
-- Helsinki Keskusta (все отделы)
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
-- Tampere (основные отделы)
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 7), (2, 8),
-- Turku (основные отделы)
(3, 1), (3, 2), (3, 4), (3, 5), (3, 7),
-- Tallinn (большой магазин)
(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
-- Riga (большой магазин)
(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 7), (5, 8), (5, 9),
-- Outlet Helsinki (ограниченные отделы)
(6, 1), (6, 2), (6, 7);

-- Пользователи
INSERT INTO users (username, email, first_name, last_name, phone, position, store_id, role) VALUES 
('admin', 'admin@stockmann.com', 'Системный', 'Администратор', '+358-40-123-4567', 'IT Administrator', NULL, 'admin'),
('anna.virtanen', 'anna.virtanen@stockmann.com', 'Анна', 'Виртанен', '+358-40-111-2222', 'Store Manager', 1, 'manager'),
('mikko.lehtinen', 'mikko.lehtinen@stockmann.com', 'Микко', 'Лехтинен', '+358-40-333-4444', 'Store Manager', 2, 'manager'),
('security.hel', 'security.helsinki@stockmann.com', 'Охрана', 'Хельсинки', '+358-40-555-6666', 'Security Officer', 1, 'security'),
('sales.women', 'sales.women@stockmann.com', 'Мария', 'Коскинен', '+358-40-777-8888', 'Sales Associate', 1, 'user'),
('tech.support', 'tech.support@stockmann.com', 'Техническая', 'Поддержка', '+358-40-999-0000', 'Technical Support', NULL, 'user'),
('kristina.magi', 'kristina.magi@stockmann.ee', 'Кристина', 'Мяги', '+372-555-1234', 'Store Manager', 4, 'manager'),
('inga.kalnina', 'inga.kalnina@stockmann.lv', 'Инга', 'Калниня', '+371-222-3333', 'Store Manager', 5, 'manager');

-- Категории инцидентов
INSERT INTO incident_categories (code, name, description, color) VALUES 
('TECH', 'Технические проблемы', 'Проблемы с оборудованием и IT системами', '#FF6B6B'),
('SAFETY', 'Безопасность', 'Вопросы безопасности и охраны', '#FF8E53'),
('CUSTOMER', 'Обслуживание клиентов', 'Жалобы и проблемы клиентов', '#4ECDC4'),
('STAFF', 'Персонал', 'Вопросы, связанные с персоналом', '#45B7D1'),
('FACILITY', 'Помещения', 'Проблемы с помещениями и инфраструктурой', '#96CEB4'),
('INVENTORY', 'Товары', 'Проблемы с товарами и инвентарем', '#FFEAA7'),
('FINANCE', 'Финансы', 'Финансовые вопросы и кассовые операции', '#DDA0DD');

-- Подкатегории инцидентов
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
(7, 'CARD_ISSUE', 'Проблемы с картами', 'Проблемы с оплатой картами', 2);

-- Тестовые инциденты
INSERT INTO incidents (title, description, category_id, subcategory_id, priority, severity, store_id, department_id, reporter_id, status, customer_affected, source) VALUES 
('Касса №3 не работает', 'Касса в отделе женской одежды не включается после обеда. Клиенты не могут оплачивать покупки.', 1, 1, 'high', 'major', 1, 1, 5, 'new', true, 'manual'),
('Жалоба на грубое обслуживание', 'Клиент жалуется на грубость продавца в отделе косметики. Требует разбирательства.', 3, 9, 'medium', 'minor', 1, 4, 2, 'assigned', true, 'email'),
('Подозрительный покупатель', 'Мужчина в черной куртке ведет себя подозрительно в отделе ювелирных изделий. Возможна попытка кражи.', 2, 8, 'high', 'major', 1, 9, 4, 'in_progress', false, 'manual'),
('Лифт застрял между этажами', 'Лифт №2 застрял между 1 и 2 этажами. Внутри находятся 3 человека.', 5, 18, 'critical', 'critical', 1, NULL, 2, 'resolved', true, 'phone'),
('Недостача в отделе обуви', 'При инвентаризации обнаружена недостача 5 пар обуви на сумму 800 евро.', 6, 20, 'medium', 'major', 2, 7, 3, 'new', false, 'manual');

-- История изменений
INSERT INTO incident_history (incident_id, changed_by, field_name, old_value, new_value, change_reason) VALUES 
(2, 2, 'status', 'new', 'assigned', 'Назначен ответственный менеджер'),
(2, 2, 'assigned_to', NULL, '2', 'Назначение менеджера магазина'),
(3, 4, 'status', 'new', 'in_progress', 'Начато расследование'),
(4, 2, 'status', 'new', 'resolved', 'Лифт отремонтирован, люди эвакуированы');

-- Комментарии
INSERT INTO incident_comments (incident_id, user_id, comment_text, is_internal) VALUES 
(1, 5, 'Касса полностью не реагирует на нажатия. Пробовала перезагрузить - не помогает.', false),
(1, 6, 'Выезжаю на место для диагностики. Ожидаемое время прибытия - 30 минут.', true),
(2, 2, 'Связался с клиентом, извинился от имени магазина. Проведу беседу с сотрудником.', true),
(3, 4, 'Подозреваемый покинул магазин. Просматриваю записи камер видеонаблюдения.', true),
(4, 2, 'Вызвана аварийная служба лифтов. Люди в безопасности, общаемся через переговорное устройство.', false);

-- SLA правила
INSERT INTO sla_rules (category_id, subcategory_id, priority, severity, response_time_hours, resolution_time_hours) VALUES 
(1, 1, 'critical', 'critical', 0.5, 2),
(1, 1, 'high', 'major', 1, 4),
(2, 6, 'critical', 'critical', 0.25, 1),
(2, 7, 'critical', 'critical', 0.25, 0.5),
(5, 18, 'critical', 'critical', 0.5, 2),
(7, 21, 'high', 'major', 1, 4);

-- Рабочие смены
INSERT INTO work_shifts (store_id, shift_name, start_time, end_time) VALUES 
(1, 'Утренняя', '09:00', '15:00'),
(1, 'Дневная', '13:00', '21:00'),
(1, 'Вечерняя', '17:00', '22:00'),
(2, 'Утренняя', '10:00', '16:00'),
(2, 'Вечерняя', '14:00', '20:00'),
(4, 'Утренняя', '10:00', '16:00'),
(4, 'Вечерняя', '14:00', '21:00'),
(5, 'Утренняя', '10:00', '16:00'),
(5, 'Вечерняя', '14:00', '20:00');