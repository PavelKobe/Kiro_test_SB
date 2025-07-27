-- Дополнительные данные для системы управления инцидентами Stockmann
-- Расширение категорий, подкатегорий и магазинов

-- ===== ДОПОЛНИТЕЛЬНЫЕ ГОРОДА =====
INSERT INTO cities (country_id, name, region) VALUES 
-- Финляндия
(1, 'Эспоо', 'Уусимаа'),
(1, 'Вантаа', 'Уусимаа'),
(1, 'Оулу', 'Северная Остроботния'),
(1, 'Йювяскюля', 'Центральная Финляндия'),
(1, 'Лахти', 'Пяйят-Хяме'),
(1, 'Куопио', 'Северное Саво'),
-- Эстония
(2, 'Пярну', 'Пярнумаа'),
(2, 'Нарва', 'Ида-Вирумаа'),
-- Латвия
(3, 'Лиепая', 'Курземе'),
(3, 'Елгава', 'Земгале'),
(3, 'Вентспилс', 'Курземе');

-- ===== ДОПОЛНИТЕЛЬНЫЕ МАГАЗИНЫ =====
INSERT INTO stores (code, name, address, city_id, store_type, area_sqm, phone, email, manager_name, opened_date) VALUES 
-- Финляндия - новые магазины
('ESP001', 'Stockmann Espoo Iso Omena', 'Piispansilta 11, Espoo', 8, 'department_store', 7500, '+358-9-8520-1000', 'espoo@stockmann.com', 'Петра Лаакконен', '2005-10-15'),
('VAN001', 'Stockmann Vantaa Jumbo', 'Vantaanportinkatu 3, Vantaa', 9, 'outlet', 4000, '+358-9-8520-2000', 'vantaa@stockmann.com', 'Матти Хейккинен', '2008-03-20'),
('OUL001', 'Stockmann Oulu', 'Kirkkokatu 3, Oulu', 10, 'department_store', 5500, '+358-8-5584-1000', 'oulu@stockmann.com', 'Сату Ниеми', '2001-09-05'),
('JYV001', 'Stockmann Jyväskylä', 'Kauppakatu 20, Jyväskylä', 11, 'department_store', 4500, '+358-14-337-1000', 'jyvaskyla@stockmann.com', 'Кари Лехто', '2003-05-12'),
('LAH001', 'Stockmann Lahti', 'Aleksanterinkatu 18, Lahti', 12, 'outlet', 3000, '+358-3-8142-1000', 'lahti@stockmann.com', 'Анна-Лиза Корхонен', '2010-11-08'),

-- Эстония - новые магазины
('PAR001', 'Stockmann Pärnu', 'Rüütli 14, Pärnu', 15, 'department_store', 3500, '+372-447-9000', 'parnu@stockmann.ee', 'Кадри Тамм', '2012-06-15'),
('TAR001', 'Stockmann Tartu', 'Rüütli 2, Tartu', 5, 'outlet', 2500, '+372-730-9000', 'tartu@stockmann.ee', 'Мартин Кивистик', '2015-04-20'),

-- Латвия - новые магазины
('LIE001', 'Stockmann Liepāja', 'Graudu iela 27/29, Liepāja', 16, 'outlet', 2800, '+371-6342-5000', 'liepaja@stockmann.lv', 'Лига Озолиня', '2013-08-10'),
('JEL001', 'Stockmann Jelgava', 'Lielā iela 6, Jelgava', 17, 'outlet', 2200, '+371-6302-5000', 'jelgava@stockmann.lv', 'Андрис Берзиньш', '2016-03-25'),

-- Онлайн магазины
('FIN_ON', 'Stockmann Online Finland', 'Digital Commerce Center, Helsinki', 1, 'online', NULL, '+358-9-121-4500', 'online.fi@stockmann.com', 'Лаура Виртанен', '2018-01-01'),
('EST_ON', 'Stockmann Online Estonia', 'Digital Hub, Tallinn', 4, 'online', NULL, '+372-631-9600', 'online.ee@stockmann.ee', 'Кристель Кару', '2018-01-01'),
('LAT_ON', 'Stockmann Online Latvia', 'E-commerce Center, Riga', 6, 'online', NULL, '+371-6728-5600', 'online.lv@stockmann.lv', 'Санта Озола', '2018-01-01');

-- ===== ДОПОЛНИТЕЛЬНЫЕ ОТДЕЛЫ =====
INSERT INTO departments (code, name, description, floor_number) VALUES 
('LUXURY', 'Люкс', 'Премиальные бренды и дизайнерская одежда', 2),
('LINGERIE', 'Нижнее белье', 'Женское и мужское нижнее белье', 1),
('MATERNITY', 'Для беременных', 'Одежда для будущих мам', 3),
('PLUS_SIZE', 'Большие размеры', 'Одежда больших размеров', 2),
('VINTAGE', 'Винтаж', 'Винтажная и ретро одежда', 4),
('ELECTRONICS', 'Электроника', 'Бытовая техника и гаджеты', 5),
('BOOKS', 'Книги', 'Книги, журналы, канцелярия', 4),
('CAFE', 'Кафе', 'Кафе и ресторан в магазине', 1),
('SERVICES', 'Услуги', 'Ремонт, подгонка, персональный шоппинг', -1),
('SEASONAL', 'Сезонные товары', 'Праздничные и сезонные товары', 5);

-- ===== СВЯЗИ МАГАЗИНОВ И ОТДЕЛОВ =====
-- Большие магазины (все отделы)
INSERT INTO store_departments (store_id, department_id) VALUES 
-- Espoo (большой магазин)
(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 7), (7, 8), (7, 11), (7, 12), (7, 15), (7, 16), (7, 18),
-- Oulu (большой магазин)  
(9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 7), (9, 8), (9, 11), (9, 16), (9, 18),
-- Jyväskylä (средний магазин)
(10, 1), (10, 2), (10, 4), (10, 5), (10, 7), (10, 11), (10, 18),
-- Pärnu (средний магазин)
(12, 1), (12, 2), (12, 4), (12, 5), (12, 7), (12, 8), (12, 18),

-- Аутлеты (ограниченные отделы)
-- Vantaa Outlet
(8, 1), (8, 2), (8, 7), (8, 13), (8, 15),
-- Lahti Outlet  
(11, 1), (11, 2), (11, 7), (11, 13),
-- Tartu Outlet
(13, 1), (13, 2), (13, 7), (13, 15),
-- Liepāja Outlet
(14, 1), (14, 2), (14, 7),
-- Jelgava Outlet
(15, 1), (15, 2), (15, 7);

-- ===== ДОПОЛНИТЕЛЬНЫЕ ПОЛЬЗОВАТЕЛИ =====
INSERT INTO users (username, email, first_name, last_name, phone, position, store_id, role) VALUES 
-- Менеджеры новых магазинов
('petra.laakkonen', 'petra.laakkonen@stockmann.com', 'Петра', 'Лаакконен', '+358-40-201-1111', 'Store Manager', 7, 'manager'),
('matti.heikkinen', 'matti.heikkinen@stockmann.com', 'Матти', 'Хейккинен', '+358-40-202-2222', 'Outlet Manager', 8, 'manager'),
('satu.niemi', 'satu.niemi@stockmann.com', 'Сату', 'Ниеми', '+358-40-203-3333', 'Store Manager', 9, 'manager'),
('kari.lehto', 'kari.lehto@stockmann.com', 'Кари', 'Лехто', '+358-40-204-4444', 'Store Manager', 10, 'manager'),
('kadri.tamm', 'kadri.tamm@stockmann.ee', 'Кадри', 'Тамм', '+372-555-5555', 'Store Manager', 12, 'manager'),
('martin.kivistik', 'martin.kivistik@stockmann.ee', 'Мартин', 'Кивистик', '+372-555-6666', 'Outlet Manager', 13, 'manager'),
('liga.ozolina', 'liga.ozolina@stockmann.lv', 'Лига', 'Озолиня', '+371-222-7777', 'Outlet Manager', 14, 'manager'),

-- Сотрудники безопасности
('security.esp', 'security.espoo@stockmann.com', 'Охрана', 'Эспоо', '+358-40-301-1111', 'Security Officer', 7, 'security'),
('security.oul', 'security.oulu@stockmann.com', 'Охрана', 'Оулу', '+358-40-302-2222', 'Security Officer', 9, 'security'),
('security.par', 'security.parnu@stockmann.ee', 'Охрана', 'Пярну', '+372-555-8888', 'Security Officer', 12, 'security'),

-- IT поддержка
('it.finland', 'it.finland@stockmann.com', 'IT', 'Финляндия', '+358-40-400-1111', 'IT Support', NULL, 'user'),
('it.estonia', 'it.estonia@stockmann.ee', 'IT', 'Эстония', '+372-555-9999', 'IT Support', NULL, 'user'),
('it.latvia', 'it.latvia@stockmann.lv', 'IT', 'Латвия', '+371-222-0000', 'IT Support', NULL, 'user'),

-- Продавцы
('sales.luxury', 'sales.luxury@stockmann.com', 'Элина', 'Сало', '+358-40-501-1111', 'Luxury Sales Associate', 1, 'user'),
('sales.beauty', 'sales.beauty@stockmann.com', 'Мария', 'Лехтинен', '+358-40-502-2222', 'Beauty Consultant', 1, 'user'),
('sales.men', 'sales.men@stockmann.com', 'Юхани', 'Корхонен', '+358-40-503-3333', 'Men Sales Associate', 1, 'user');

-- ===== ДОПОЛНИТЕЛЬНЫЕ КАТЕГОРИИ ИНЦИДЕНТОВ =====
INSERT INTO incident_categories (code, name, description, color) VALUES 
('DELIVERY', 'Доставка', 'Проблемы с доставкой товаров клиентам', '#9B59B6'),
('MARKETING', 'Маркетинг', 'Проблемы с рекламой и маркетинговыми акциями', '#E67E22'),
('LEGAL', 'Юридические вопросы', 'Правовые вопросы и соответствие требованиям', '#34495E'),
('ENVIRONMENT', 'Экология', 'Экологические инциденты и устойчивое развитие', '#27AE60'),
('QUALITY', 'Качество', 'Проблемы с качеством товаров и услуг', '#E74C3C'),
('SUPPLIER', 'Поставщики', 'Проблемы с поставщиками и партнерами', '#F39C12'),
('TRAINING', 'Обучение', 'Вопросы обучения и развития персонала', '#3498DB'),
('COMMUNICATION', 'Коммуникации', 'Проблемы внутренних и внешних коммуникаций', '#1ABC9C');

-- ===== ДОПОЛНИТЕЛЬНЫЕ ПОДКАТЕГОРИИ =====
-- Доставка
INSERT INTO incident_subcategories (category_id, code, name, description, sla_hours) VALUES 
(8, 'LATE_DELIVERY', 'Задержка доставки', 'Доставка товара с опозданием', 24),
(8, 'DAMAGED_DELIVERY', 'Повреждение при доставке', 'Товар поврежден во время доставки', 8),
(8, 'WRONG_ADDRESS', 'Неверный адрес', 'Доставка по неправильному адресу', 12),
(8, 'COURIER_ISSUE', 'Проблемы с курьером', 'Некорректное поведение курьера', 4),

-- Маркетинг
(9, 'WRONG_PRICE', 'Неверная цена', 'Ошибка в ценнике или рекламе', 2),
(9, 'AD_COMPLAINT', 'Жалоба на рекламу', 'Жалобы клиентов на рекламные материалы', 24),
(9, 'PROMO_ERROR', 'Ошибка в акции', 'Технические проблемы с промо-акциями', 4),
(9, 'BRAND_ISSUE', 'Проблемы с брендом', 'Вопросы использования торговых марок', 48),

-- Юридические вопросы
(10, 'CONTRACT_DISPUTE', 'Спор по договору', 'Разногласия по условиям договора', 72),
(10, 'COMPLIANCE', 'Соответствие требованиям', 'Нарушение нормативных требований', 24),
(10, 'COPYRIGHT', 'Авторские права', 'Вопросы интеллектуальной собственности', 48),
(10, 'DATA_PRIVACY', 'Защита данных', 'Нарушение конфиденциальности данных', 4),

-- Экология
(11, 'WASTE_ISSUE', 'Проблемы с отходами', 'Неправильная утилизация отходов', 12),
(11, 'ENERGY_WASTE', 'Расход энергии', 'Избыточное потребление энергии', 24),
(11, 'PACKAGING', 'Упаковка', 'Проблемы с экологичной упаковкой', 48),
(11, 'SUSTAINABILITY', 'Устойчивое развитие', 'Вопросы экологической политики', 72),

-- Качество
(12, 'DEFECTIVE_PRODUCT', 'Бракованный товар', 'Товар с производственным браком', 8),
(12, 'SIZE_ISSUE', 'Проблемы с размерами', 'Несоответствие размеров товара', 12),
(12, 'COLOR_DIFFERENCE', 'Расхождение цвета', 'Цвет товара не соответствует описанию', 24),
(12, 'MATERIAL_ISSUE', 'Проблемы с материалом', 'Некачественный материал товара', 8),

-- Поставщики
(13, 'LATE_SUPPLY', 'Задержка поставки', 'Поставщик задерживает поставку', 24),
(13, 'QUALITY_SUPPLY', 'Качество поставки', 'Низкое качество поставленных товаров', 12),
(13, 'CONTRACT_SUPPLY', 'Договорные вопросы', 'Проблемы с договором поставки', 48),
(13, 'NEW_SUPPLIER', 'Новый поставщик', 'Вопросы работы с новыми поставщиками', 72),

-- Обучение
(14, 'SKILL_GAP', 'Недостаток навыков', 'Сотруднику не хватает навыков для работы', 48),
(14, 'TRAINING_REQUEST', 'Запрос на обучение', 'Запрос на дополнительное обучение', 72),
(14, 'CERTIFICATION', 'Сертификация', 'Вопросы получения сертификатов', 168),
(14, 'ONBOARDING', 'Адаптация', 'Проблемы адаптации новых сотрудников', 24),

-- Коммуникации
(15, 'INTERNAL_COMM', 'Внутренние коммуникации', 'Проблемы внутренней связи', 8),
(15, 'EXTERNAL_COMM', 'Внешние коммуникации', 'Проблемы связи с клиентами/партнерами', 4),
(15, 'LANGUAGE_BARRIER', 'Языковой барьер', 'Проблемы из-за языковых различий', 12),
(15, 'MISCOMMUNICATION', 'Недопонимание', 'Неправильная передача информации', 6);

-- ===== ДОПОЛНИТЕЛЬНЫЕ SLA ПРАВИЛА =====
INSERT INTO sla_rules (category_id, subcategory_id, priority, severity, response_time_hours, resolution_time_hours) VALUES 
-- Критические правила для новых категорий
(8, 26, 'critical', 'critical', 1, 4),  -- Повреждение при доставке
(9, 29, 'high', 'major', 0.5, 2),      -- Неверная цена
(10, 35, 'critical', 'critical', 2, 4), -- Защита данных
(12, 37, 'high', 'major', 2, 8),       -- Бракованный товар
(15, 47, 'high', 'major', 1, 4);       -- Внешние коммуникации

-- ===== РАБОЧИЕ СМЕНЫ ДЛЯ НОВЫХ МАГАЗИНОВ =====
INSERT INTO work_shifts (store_id, shift_name, start_time, end_time) VALUES 
-- Espoo
(7, 'Утренняя', '09:00', '15:00'),
(7, 'Дневная', '13:00', '21:00'),
(7, 'Вечерняя', '17:00', '22:00'),
-- Vantaa (аутлет - короткие смены)
(8, 'Дневная', '10:00', '18:00'),
(8, 'Вечерняя', '14:00', '20:00'),
-- Oulu
(9, 'Утренняя', '10:00', '16:00'),
(9, 'Вечерняя', '14:00', '20:00'),
-- Jyväskylä
(10, 'Дневная', '10:00', '18:00'),
(10, 'Вечерняя', '14:00', '20:00'),
-- Pärnu
(12, 'Утренняя', '10:00', '16:00'),
(12, 'Вечерняя', '14:00', '21:00');

-- ===== ТЕСТОВЫЕ ИНЦИДЕНТЫ ДЛЯ НОВЫХ КАТЕГОРИЙ =====
INSERT INTO incidents (title, description, category_id, subcategory_id, priority, severity, store_id, department_id, reporter_id, status, customer_affected, source, location_details) VALUES 
('Задержка доставки премиум заказа', 'VIP клиент не получил заказ дизайнерской одежды в срок. Заказ должен был прийти вчера к 18:00.', 8, 24, 'high', 'major', 7, 11, 7, 'new', true, 'phone', 'Служба доставки'),
('Неверная цена на витрине', 'На витрине указана цена 299€, а в системе 399€. Клиенты требуют продать по цене витрины.', 9, 29, 'high', 'major', 9, 1, 9, 'assigned', true, 'manual', 'Витрина женской одежды'),
('Бракованная обувь', 'Клиент купил туфли за 450€, через день отклеилась подошва. Требует возврат и компенсацию.', 12, 37, 'medium', 'major', 1, 7, 5, 'new', true, 'email', 'Отдел обуви, касса №2'),
('Проблемы с новым поставщиком', 'Поставщик косметики прислал товар не того оттенка. Весь заказ на 15000€ не соответствует спецификации.', 13, 42, 'high', 'major', 1, 4, 2, 'in_progress', false, 'manual', 'Склад косметики'),
('Языковой барьер с туристами', 'Группа японских туристов не может получить помощь в отделе. Нужен переводчик или сотрудник со знанием английского.', 15, 47, 'medium', 'minor', 1, 11, 16, 'new', true, 'manual', 'Отдел люкс, 2 этаж');

-- ===== КОММЕНТАРИИ К НОВЫМ ИНЦИДЕНТАМ =====
INSERT INTO incident_comments (incident_id, user_id, comment_text, is_internal) VALUES 
(6, 7, 'Связался со службой доставки. Заказ застрял на таможне из-за неправильного оформления документов.', true),
(6, 7, 'Клиенту предложена компенсация и экспресс-доставка завтра утром.', false),
(7, 9, 'Проверил все ценники в отделе. Найдено еще 3 товара с неверными ценами.', true),
(8, 5, 'Товар принят к возврату. Связываюсь с поставщиком для выяснения причин брака.', true),
(9, 2, 'Поставщик признал ошибку. Обещают заменить весь заказ в течение недели.', true),
(10, 16, 'Нашел сотрудника со знанием английского. Туристы получили необходимую помощь.', false);

-- ===== ИСТОРИЯ ИЗМЕНЕНИЙ ДЛЯ НОВЫХ ИНЦИДЕНТОВ =====
INSERT INTO incident_history (incident_id, changed_by, field_name, old_value, new_value, change_reason) VALUES 
(7, 9, 'status', 'new', 'assigned', 'Назначен менеджер магазина для решения'),
(7, 9, 'assigned_to', NULL, '9', 'Самоназначение для быстрого решения'),
(9, 2, 'status', 'new', 'in_progress', 'Начаты переговоры с поставщиком'),
(10, 16, 'status', 'new', 'resolved', 'Проблема решена, туристы обслужены');

-- Обновляем счетчики последовательностей для корректной генерации ID
SELECT setval('cities_id_seq', (SELECT MAX(id) FROM cities));
SELECT setval('stores_id_seq', (SELECT MAX(id) FROM stores));
SELECT setval('departments_id_seq', (SELECT MAX(id) FROM departments));
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('incident_categories_id_seq', (SELECT MAX(id) FROM incident_categories));
SELECT setval('incident_subcategories_id_seq', (SELECT MAX(id) FROM incident_subcategories));
SELECT setval('incidents_id_seq', (SELECT MAX(id) FROM incidents));
SELECT setval('incident_comments_id_seq', (SELECT MAX(id) FROM incident_comments));
SELECT setval('incident_history_id_seq', (SELECT MAX(id) FROM incident_history));
SELECT setval('sla_rules_id_seq', (SELECT MAX(id) FROM sla_rules));
SELECT setval('work_shifts_id_seq', (SELECT MAX(id) FROM work_shifts));