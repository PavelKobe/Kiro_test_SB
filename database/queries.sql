-- Полезные SQL запросы для системы управления инцидентами Stockmann

-- ===== СТАТИСТИКА ПО МАГАЗИНАМ =====

-- Общая статистика инцидентов по магазинам
SELECT 
    s.code as store_code,
    s.name as store_name,
    c.name as country,
    COUNT(i.id) as total_incidents,
    COUNT(CASE WHEN i.status IN ('new', 'assigned', 'in_progress') THEN 1 END) as active_incidents,
    COUNT(CASE WHEN i.status = 'resolved' THEN 1 END) as resolved_incidents,
    COUNT(CASE WHEN i.sla_breached = true THEN 1 END) as overdue_incidents,
    ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL 
        THEN EXTRACT(EPOCH FROM (i.resolved_at - i.created_at))/3600 
        END), 2) as avg_resolution_hours
FROM stores s
LEFT JOIN incidents i ON s.id = i.store_id
LEFT JOIN cities ct ON s.city_id = ct.id
LEFT JOIN countries c ON ct.country_id = c.id
GROUP BY s.id, s.code, s.name, c.name
ORDER BY total_incidents DESC;

-- ===== ПРОСРОЧЕННЫЕ ИНЦИДЕНТЫ =====

-- Все просроченные инциденты с детализацией
SELECT 
    i.incident_number,
    i.title,
    s.name as store_name,
    d.name as department,
    ic.name as category,
    isc.name as subcategory,
    i.priority,
    i.severity,
    u.first_name || ' ' || u.last_name as assigned_to,
    i.created_at,
    i.sla_deadline,
    ROUND(EXTRACT(EPOCH FROM (NOW() - i.sla_deadline))/3600, 1) as hours_overdue,
    CASE 
        WHEN i.customer_affected THEN 'Да' 
        ELSE 'Нет' 
    END as customer_affected
FROM incidents i
JOIN stores s ON i.store_id = s.id
LEFT JOIN departments d ON i.department_id = d.id
JOIN incident_categories ic ON i.category_id = ic.id
JOIN incident_subcategories isc ON i.subcategory_id = isc.id
LEFT JOIN users u ON i.assigned_to = u.id
WHERE i.sla_deadline < NOW() 
  AND i.status NOT IN ('resolved', 'closed', 'cancelled')
ORDER BY hours_overdue DESC;

-- ===== РАБОЧАЯ НАГРУЗКА =====

-- Рабочая нагрузка пользователей
SELECT 
    u.username,
    u.first_name || ' ' || u.last_name as full_name,
    u.position,
    s.name as store_name,
    u.role,
    COUNT(i.id) as assigned_incidents,
    COUNT(CASE WHEN i.priority = 'critical' THEN 1 END) as critical_incidents,
    COUNT(CASE WHEN i.priority = 'high' THEN 1 END) as high_incidents,
    COUNT(CASE WHEN i.sla_deadline < NOW() THEN 1 END) as overdue_incidents
FROM users u
LEFT JOIN incidents i ON u.id = i.assigned_to 
    AND i.status IN ('assigned', 'in_progress')
LEFT JOIN stores s ON u.store_id = s.id
WHERE u.is_active = true
GROUP BY u.id, u.username, u.first_name, u.last_name, u.position, s.name, u.role
ORDER BY assigned_incidents DESC;

-- ===== АНАЛИЗ ПО КАТЕГОРИЯМ =====

-- Статистика по категориям инцидентов
SELECT 
    ic.name as category,
    isc.name as subcategory,
    COUNT(i.id) as total_count,
    COUNT(CASE WHEN i.status IN ('new', 'assigned', 'in_progress') THEN 1 END) as active_count,
    COUNT(CASE WHEN i.customer_affected = true THEN 1 END) as customer_affected_count,
    ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL 
        THEN EXTRACT(EPOCH FROM (i.resolved_at - i.created_at))/3600 
        END), 2) as avg_resolution_hours,
    isc.sla_hours as sla_target_hours,
    COUNT(CASE WHEN i.sla_breached = true THEN 1 END) as sla_breached_count,
    ROUND(COUNT(CASE WHEN i.sla_breached = true THEN 1 END) * 100.0 / COUNT(i.id), 2) as sla_breach_percentage
FROM incident_categories ic
JOIN incident_subcategories isc ON ic.id = isc.category_id
LEFT JOIN incidents i ON isc.id = i.subcategory_id
GROUP BY ic.id, ic.name, isc.id, isc.name, isc.sla_hours
ORDER BY total_count DESC;

-- ===== ВРЕМЕННАЯ АНАЛИТИКА =====

-- Инциденты по дням недели
SELECT 
    EXTRACT(DOW FROM i.created_at) as day_of_week,
    CASE EXTRACT(DOW FROM i.created_at)
        WHEN 0 THEN 'Воскресенье'
        WHEN 1 THEN 'Понедельник'
        WHEN 2 THEN 'Вторник'
        WHEN 3 THEN 'Среда'
        WHEN 4 THEN 'Четверг'
        WHEN 5 THEN 'Пятница'
        WHEN 6 THEN 'Суббота'
    END as day_name,
    COUNT(i.id) as incident_count,
    COUNT(CASE WHEN i.priority IN ('high', 'critical') THEN 1 END) as high_priority_count
FROM incidents i
WHERE i.created_at >= NOW() - INTERVAL '30 days'
GROUP BY EXTRACT(DOW FROM i.created_at)
ORDER BY day_of_week;

-- Инциденты по часам дня
SELECT 
    EXTRACT(HOUR FROM i.created_at) as hour_of_day,
    COUNT(i.id) as incident_count,
    COUNT(CASE WHEN i.category_id = (SELECT id FROM incident_categories WHERE code = 'TECH') THEN 1 END) as tech_incidents,
    COUNT(CASE WHEN i.category_id = (SELECT id FROM incident_categories WHERE code = 'SAFETY') THEN 1 END) as safety_incidents
FROM incidents i
WHERE i.created_at >= NOW() - INTERVAL '30 days'
GROUP BY EXTRACT(HOUR FROM i.created_at)
ORDER BY hour_of_day;

-- ===== ФИНАНСОВЫЙ АНАЛИЗ =====

-- Финансовое влияние инцидентов
SELECT 
    s.name as store_name,
    ic.name as category,
    COUNT(i.id) as incident_count,
    SUM(COALESCE(i.financial_impact, 0)) as total_financial_impact,
    AVG(COALESCE(i.financial_impact, 0)) as avg_financial_impact,
    COUNT(CASE WHEN i.customer_affected = true THEN 1 END) as customer_affected_count
FROM incidents i
JOIN stores s ON i.store_id = s.id
JOIN incident_categories ic ON i.category_id = ic.id
WHERE i.created_at >= NOW() - INTERVAL '90 days'
  AND i.financial_impact IS NOT NULL
GROUP BY s.id, s.name, ic.id, ic.name
ORDER BY total_financial_impact DESC;

-- ===== ЭФФЕКТИВНОСТЬ РАБОТЫ =====

-- Среднее время решения по пользователям
SELECT 
    u.first_name || ' ' || u.last_name as resolver_name,
    u.position,
    s.name as store_name,
    COUNT(i.id) as resolved_incidents,
    ROUND(AVG(EXTRACT(EPOCH FROM (i.resolved_at - i.created_at))/3600), 2) as avg_resolution_hours,
    COUNT(CASE WHEN i.sla_breached = false THEN 1 END) as within_sla_count,
    ROUND(COUNT(CASE WHEN i.sla_breached = false THEN 1 END) * 100.0 / COUNT(i.id), 2) as sla_compliance_percentage
FROM incidents i
JOIN users u ON i.resolver_id = u.id
LEFT JOIN stores s ON u.store_id = s.id
WHERE i.resolved_at IS NOT NULL
  AND i.created_at >= NOW() - INTERVAL '90 days'
GROUP BY u.id, u.first_name, u.last_name, u.position, s.name
HAVING COUNT(i.id) >= 5
ORDER BY sla_compliance_percentage DESC, avg_resolution_hours ASC;

-- ===== ОТЧЕТЫ ДЛЯ МЕНЕДЖМЕНТА =====

-- Ежемесячный отчет по инцидентам
SELECT 
    DATE_TRUNC('month', i.created_at) as month,
    COUNT(i.id) as total_incidents,
    COUNT(CASE WHEN i.status = 'resolved' THEN 1 END) as resolved_incidents,
    COUNT(CASE WHEN i.priority = 'critical' THEN 1 END) as critical_incidents,
    COUNT(CASE WHEN i.customer_affected = true THEN 1 END) as customer_affected_incidents,
    COUNT(CASE WHEN i.sla_breached = true THEN 1 END) as sla_breached_incidents,
    ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL 
        THEN EXTRACT(EPOCH FROM (i.resolved_at - i.created_at))/3600 
        END), 2) as avg_resolution_hours,
    SUM(COALESCE(i.financial_impact, 0)) as total_financial_impact
FROM incidents i
WHERE i.created_at >= NOW() - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', i.created_at)
ORDER BY month DESC;

-- Топ-10 самых частых проблем
SELECT 
    isc.name as subcategory,
    ic.name as category,
    COUNT(i.id) as incident_count,
    COUNT(CASE WHEN i.created_at >= NOW() - INTERVAL '30 days' THEN 1 END) as last_30_days,
    ROUND(AVG(EXTRACT(EPOCH FROM (i.resolved_at - i.created_at))/3600), 2) as avg_resolution_hours,
    COUNT(CASE WHEN i.customer_affected = true THEN 1 END) as customer_affected_count
FROM incident_subcategories isc
JOIN incident_categories ic ON isc.category_id = ic.id
LEFT JOIN incidents i ON isc.id = i.subcategory_id
GROUP BY isc.id, isc.name, ic.name
ORDER BY incident_count DESC
LIMIT 10;

-- ===== МОНИТОРИНГ SLA =====

-- SLA соответствие по магазинам
SELECT 
    s.name as store_name,
    COUNT(i.id) as total_incidents,
    COUNT(CASE WHEN i.sla_breached = false AND i.status IN ('resolved', 'closed') THEN 1 END) as within_sla,
    COUNT(CASE WHEN i.sla_breached = true THEN 1 END) as breached_sla,
    ROUND(
        COUNT(CASE WHEN i.sla_breached = false AND i.status IN ('resolved', 'closed') THEN 1 END) * 100.0 / 
        NULLIF(COUNT(CASE WHEN i.status IN ('resolved', 'closed') THEN 1 END), 0), 
        2
    ) as sla_compliance_percentage
FROM stores s
LEFT JOIN incidents i ON s.id = i.store_id
WHERE i.created_at >= NOW() - INTERVAL '90 days'
GROUP BY s.id, s.name
ORDER BY sla_compliance_percentage DESC;

-- ===== АКТИВНОСТЬ ПОЛЬЗОВАТЕЛЕЙ =====

-- Последняя активность пользователей
SELECT 
    u.username,
    u.first_name || ' ' || u.last_name as full_name,
    u.role,
    s.name as store_name,
    u.last_login,
    (SELECT COUNT(*) FROM incidents WHERE reporter_id = u.id AND created_at >= NOW() - INTERVAL '30 days') as incidents_reported_30d,
    (SELECT COUNT(*) FROM incidents WHERE assigned_to = u.id AND status IN ('assigned', 'in_progress')) as currently_assigned,
    (SELECT COUNT(*) FROM incident_comments WHERE user_id = u.id AND created_at >= NOW() - INTERVAL '7 days') as comments_7d
FROM users u
LEFT JOIN stores s ON u.store_id = s.id
WHERE u.is_active = true
ORDER BY u.last_login DESC NULLS LAST;

-- ===== ПОИСК И ФИЛЬТРАЦИЯ =====

-- Поиск инцидентов по ключевым словам
-- Параметр: заменить 'касса' на нужное слово
SELECT 
    i.incident_number,
    i.title,
    i.description,
    s.name as store_name,
    ic.name as category,
    i.status,
    i.created_at
FROM incidents i
JOIN stores s ON i.store_id = s.id
JOIN incident_categories ic ON i.category_id = ic.id
WHERE (
    LOWER(i.title) LIKE LOWER('%касса%') OR 
    LOWER(i.description) LIKE LOWER('%касса%')
)
ORDER BY i.created_at DESC;

-- Инциденты с комментариями за последние 24 часа
SELECT DISTINCT
    i.incident_number,
    i.title,
    s.name as store_name,
    i.status,
    COUNT(ic.id) as comment_count,
    MAX(ic.created_at) as last_comment_at
FROM incidents i
JOIN stores s ON i.store_id = s.id
JOIN incident_comments ic ON i.id = ic.incident_id
WHERE ic.created_at >= NOW() - INTERVAL '24 hours'
GROUP BY i.id, i.incident_number, i.title, s.name, i.status
ORDER BY last_comment_at DESC;