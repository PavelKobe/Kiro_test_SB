-- Схема базы данных для системы управления инцидентами торговой сети Stockmann
-- Создано для PostgreSQL

-- Справочник стран
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) NOT NULL UNIQUE, -- ISO код страны (FIN, EST, LVA)
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Справочник городов
CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES countries(id),
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Справочник магазинов/торговых точек
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE, -- Код магазина (например, HEL001, TAL002)
    name VARCHAR(200) NOT NULL,
    address TEXT,
    city_id INTEGER REFERENCES cities(id),
    store_type VARCHAR(50) NOT NULL, -- department_store, outlet, online
    area_sqm INTEGER, -- Площадь магазина
    phone VARCHAR(50),
    email VARCHAR(100),
    manager_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    opened_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Справочник отделов/секций магазина
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    floor_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Связь магазинов и отделов (многие ко многим)
CREATE TABLE store_departments (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    department_id INTEGER REFERENCES departments(id),
    is_active BOOLEAN DEFAULT true,
    UNIQUE(store_id, department_id)
);

-- Справочник пользователей системы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(50),
    position VARCHAR(100), -- Должность
    store_id INTEGER REFERENCES stores(id), -- Привязка к магазину
    role VARCHAR(50) NOT NULL DEFAULT 'user', -- admin, manager, user, security
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Категории инцидентов
CREATE TABLE incident_categories (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(7), -- HEX цвет для UI
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Подкатегории инцидентов
CREATE TABLE incident_subcategories (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES incident_categories(id),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    sla_hours INTEGER DEFAULT 24, -- SLA в часах
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Основная таблица инцидентов
CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    incident_number VARCHAR(50) NOT NULL UNIQUE, -- Уникальный номер инцидента
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    
    -- Классификация
    category_id INTEGER REFERENCES incident_categories(id),
    subcategory_id INTEGER REFERENCES incident_subcategories(id),
    priority VARCHAR(20) NOT NULL DEFAULT 'medium', -- low, medium, high, critical
    severity VARCHAR(20) NOT NULL DEFAULT 'minor', -- minor, major, critical
    
    -- Локация
    store_id INTEGER REFERENCES stores(id),
    department_id INTEGER REFERENCES departments(id),
    location_details TEXT, -- Дополнительное описание места
    
    -- Статус и временные метки
    status VARCHAR(30) NOT NULL DEFAULT 'new', -- new, assigned, in_progress, resolved, closed, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_at TIMESTAMP,
    resolved_at TIMESTAMP,
    closed_at TIMESTAMP,
    
    -- Участники
    reporter_id INTEGER REFERENCES users(id), -- Кто сообщил
    assigned_to INTEGER REFERENCES users(id), -- Кому назначен
    resolver_id INTEGER REFERENCES users(id), -- Кто решил
    
    -- Дополнительная информация
    customer_affected BOOLEAN DEFAULT false, -- Затронуты ли клиенты
    financial_impact DECIMAL(10,2), -- Финансовый ущерб
    resolution_notes TEXT, -- Описание решения
    
    -- SLA
    sla_deadline TIMESTAMP, -- Крайний срок по SLA
    sla_breached BOOLEAN DEFAULT false, -- Нарушен ли SLA
    
    -- Метаданные
    source VARCHAR(50) DEFAULT 'manual', -- manual, email, phone, system
    external_ticket_id VARCHAR(100), -- ID во внешней системе
    
    CONSTRAINT chk_priority CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    CONSTRAINT chk_severity CHECK (severity IN ('minor', 'major', 'critical')),
    CONSTRAINT chk_status CHECK (status IN ('new', 'assigned', 'in_progress', 'resolved', 'closed', 'cancelled')),
    CONSTRAINT chk_source CHECK (source IN ('manual', 'email', 'phone', 'system', 'mobile_app'))
);

-- История изменений инцидентов
CREATE TABLE incident_history (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id),
    changed_by INTEGER REFERENCES users(id),
    field_name VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Комментарии к инцидентам
CREATE TABLE incident_comments (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id),
    user_id INTEGER REFERENCES users(id),
    comment_text TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT false, -- Внутренний комментарий или для клиента
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Файлы и вложения
CREATE TABLE incident_attachments (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id),
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Связанные инциденты
CREATE TABLE incident_relations (
    id SERIAL PRIMARY KEY,
    parent_incident_id INTEGER REFERENCES incidents(id),
    child_incident_id INTEGER REFERENCES incidents(id),
    relation_type VARCHAR(20) NOT NULL, -- duplicate, related, blocks, caused_by
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_relation_type CHECK (relation_type IN ('duplicate', 'related', 'blocks', 'caused_by')),
    CONSTRAINT chk_not_self_related CHECK (parent_incident_id != child_incident_id)
);

-- Эскалации инцидентов
CREATE TABLE incident_escalations (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id),
    escalated_from INTEGER REFERENCES users(id),
    escalated_to INTEGER REFERENCES users(id),
    escalation_level INTEGER NOT NULL DEFAULT 1, -- Уровень эскалации
    reason TEXT NOT NULL,
    escalated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- SLA правила
CREATE TABLE sla_rules (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES incident_categories(id),
    subcategory_id INTEGER REFERENCES incident_subcategories(id),
    priority VARCHAR(20),
    severity VARCHAR(20),
    response_time_hours INTEGER NOT NULL, -- Время на первый ответ
    resolution_time_hours INTEGER NOT NULL, -- Время на решение
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Уведомления
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER REFERENCES incidents(id),
    user_id INTEGER REFERENCES users(id),
    notification_type VARCHAR(50) NOT NULL, -- email, sms, push, system
    subject VARCHAR(200),
    message TEXT NOT NULL,
    sent_at TIMESTAMP,
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Рабочие смены (для отслеживания времени работы)
CREATE TABLE work_shifts (
    id SERIAL PRIMARY KEY,
    store_id INTEGER REFERENCES stores(id),
    shift_name VARCHAR(50) NOT NULL, -- morning, evening, night
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- Индексы для оптимизации производительности
CREATE INDEX idx_incidents_store_id ON incidents(store_id);
CREATE INDEX idx_incidents_status ON incidents(status);
CREATE INDEX idx_incidents_priority ON incidents(priority);
CREATE INDEX idx_incidents_created_at ON incidents(created_at);
CREATE INDEX idx_incidents_assigned_to ON incidents(assigned_to);
CREATE INDEX idx_incidents_category_id ON incidents(category_id);
CREATE INDEX idx_incidents_number ON incidents(incident_number);
CREATE INDEX idx_incident_history_incident_id ON incident_history(incident_id);
CREATE INDEX idx_incident_comments_incident_id ON incident_comments(incident_id);
CREATE INDEX idx_stores_code ON stores(code);
CREATE INDEX idx_stores_city_id ON stores(city_id);
CREATE INDEX idx_users_store_id ON users(store_id);
CREATE INDEX idx_users_role ON users(role);

-- Триггеры для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_incidents_updated_at BEFORE UPDATE ON incidents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stores_updated_at BEFORE UPDATE ON stores
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Триггер для автоматической генерации номера инцидента
CREATE OR REPLACE FUNCTION generate_incident_number()
RETURNS TRIGGER AS $$
DECLARE
    store_code VARCHAR(10);
    year_part VARCHAR(4);
    sequence_num INTEGER;
BEGIN
    -- Получаем код магазина
    SELECT code INTO store_code FROM stores WHERE id = NEW.store_id;
    
    -- Получаем год
    year_part := EXTRACT(YEAR FROM CURRENT_DATE)::VARCHAR;
    
    -- Получаем следующий номер в последовательности для данного магазина и года
    SELECT COALESCE(MAX(CAST(SUBSTRING(incident_number FROM '[0-9]+$') AS INTEGER)), 0) + 1
    INTO sequence_num
    FROM incidents 
    WHERE incident_number LIKE store_code || '-' || year_part || '-%';
    
    -- Формируем номер инцидента: STORE-YYYY-NNNN
    NEW.incident_number := store_code || '-' || year_part || '-' || LPAD(sequence_num::VARCHAR, 4, '0');
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER generate_incident_number_trigger 
    BEFORE INSERT ON incidents
    FOR EACH ROW 
    WHEN (NEW.incident_number IS NULL OR NEW.incident_number = '')
    EXECUTE FUNCTION generate_incident_number();

-- Триггер для автоматического расчета SLA
CREATE OR REPLACE FUNCTION calculate_sla_deadline()
RETURNS TRIGGER AS $$
DECLARE
    sla_hours INTEGER;
BEGIN
    -- Получаем SLA из правил или подкатегории
    SELECT COALESCE(sr.resolution_time_hours, isc.sla_hours, 24)
    INTO sla_hours
    FROM incident_subcategories isc
    LEFT JOIN sla_rules sr ON sr.subcategory_id = isc.id 
        AND sr.priority = NEW.priority 
        AND sr.severity = NEW.severity
        AND sr.is_active = true
    WHERE isc.id = NEW.subcategory_id;
    
    -- Устанавливаем крайний срок
    NEW.sla_deadline := NEW.created_at + (sla_hours || ' hours')::INTERVAL;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_sla_deadline_trigger 
    BEFORE INSERT ON incidents
    FOR EACH ROW 
    EXECUTE FUNCTION calculate_sla_deadline();