# Руководство по MCP серверам для Flask приложения

## Обзор

Настроены 3 MCP сервера для разработки Flask приложения в Kiro IDE:

1. **PostgreSQL Server** - выполнение SQL запросов (только чтение)
2. **Flask Docs Server** - поиск по документации Flask/SQLAlchemy
3. **OpenAPI CodeGen Server** - генерация кода на основе OpenAPI спецификации

## Установка и настройка

### 1. Быстрая установка
```bash
# Запустите скрипт установки
setup_mcp.bat
```

### 2. Ручная установка
```bash
# Установите зависимости
pip install mcp psycopg2-binary PyYAML

# Создайте каталоги
mkdir .kiro\settings

# Скопируйте переменные окружения
copy .env.mcp .env
```

### 3. Настройка PostgreSQL
Отредактируйте `.env` файл с вашими настройками БД:
```env
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Использование MCP серверов

### PostgreSQL Server

#### Доступные инструменты:

**pg_query** - Выполнение SQL запросов
```json
{
  "query": "SELECT * FROM users WHERE active = %(active)s",
  "params": {"active": true}
}
```

**get_schema** - Получение схемы БД
```json
{
  "table_name": "users"  // опционально
}
```

**list_tables** - Список всех таблиц
```json
{}
```

#### Примеры использования:
```
Kiro: Покажи все активные инциденты
MCP: pg_query {"query": "SELECT * FROM incidents WHERE status = 'active'"}

Kiro: Какая структура таблицы users?
MCP: get_schema {"table_name": "users"}
```

### Flask Docs Server

Автоматически подключается к документации Flask и SQLAlchemy.

#### Примеры запросов:
```
Kiro: Как создать модель SQLAlchemy с отношениями?
MCP: Найдет документацию по relationships в SQLAlchemy

Kiro: Как настроить Flask-Migrate?
MCP: Покажет документацию по миграциям
```

### OpenAPI CodeGen Server

#### Доступные инструменты:

**generate_model** - Генерация модели SQLAlchemy
```json
{
  "schema_name": "Incident",
  "table_name": "incidents"  // опционально
}
```

**generate_route** - Генерация Flask маршрута
```json
{
  "path": "/incidents/{incident_id}",
  "method": "GET"
}
```

**validate_spec** - Валидация OpenAPI спецификации
```json
{}
```

**list_schemas** - Список всех схем
```json
{}
```

#### Примеры использования:
```
Kiro: Создай модель для схемы Incident
MCP: generate_model {"schema_name": "Incident"}

Kiro: Сгенерируй маршрут для получения инцидента
MCP: generate_route {"path": "/incidents/{incident_id}", "method": "GET"}
```

## Структура файлов

```
project/
├── .kiro/
│   └── settings/
│       └── mcp.json              # Конфигурация MCP серверов
├── app/
│   └── mcp/
│       ├── __init__.py
│       ├── pg_server.py          # PostgreSQL MCP сервер
│       ├── openapi_server.py     # OpenAPI генератор
│       └── requirements.txt      # Зависимости MCP
├── api/
│   └── openapi.yaml              # OpenAPI спецификация
├── .env.mcp                      # Переменные окружения
├── setup_mcp.bat                 # Скрипт установки
└── MCP_GUIDE.md                  # Это руководство
```

## Конфигурация MCP (.kiro/settings/mcp.json)

```json
{
  "mcpServers": {
    "postgresql-server": {
      "command": "python",
      "args": ["app/mcp/pg_server.py"],
      "env": {
        "DB_NAME": "flask_app",
        "DB_USER": "postgres",
        "DB_PASSWORD": "password",
        "DB_HOST": "localhost"
      },
      "autoApprove": ["pg_query", "get_schema", "list_tables"]
    },
    "flask-docs": {
      "command": "uvx",
      "args": ["mcp-server-docs@latest", "--source", "flask"],
      "autoApprove": ["search_docs"]
    },
    "openapi-codegen": {
      "command": "python", 
      "args": ["app/mcp/openapi_server.py"],
      "autoApprove": ["generate_model", "generate_route"]
    }
  }
}
```

## Безопасность

### PostgreSQL Server
- **Только чтение**: Разрешены только SELECT, WITH, EXPLAIN запросы
- **Параметризованные запросы**: Защита от SQL инъекций
- **Ограничения подключения**: Только к указанной БД

### OpenAPI Server
- **Валидация схем**: Проверка корректности спецификации
- **Безопасная генерация**: Только разрешенные типы кода

## Отладка

### Проверка статуса серверов
В Kiro IDE откройте панель MCP Servers для просмотра статуса подключений.

### Логи
Логи серверов доступны в консоли Kiro IDE. Уровень логирования настраивается через `FASTMCP_LOG_LEVEL`.

### Тестирование подключения
```python
# Тест PostgreSQL подключения
python -c "import psycopg2; print('PostgreSQL OK')"

# Тест загрузки OpenAPI
python -c "import yaml; print('YAML OK')"
```

## Расширение функциональности

### Добавление нового инструмента в PostgreSQL Server
```python
@self.server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]):
    if name == "my_new_tool":
        return await self._handle_my_new_tool(arguments)
```

### Создание нового MCP сервера
1. Создайте новый файл в `app/mcp/`
2. Добавьте конфигурацию в `mcp.json`
3. Перезапустите Kiro IDE

## Поддержка

При возникновении проблем:
1. Проверьте логи в Kiro IDE
2. Убедитесь в корректности переменных окружения
3. Проверьте доступность PostgreSQL
4. Валидируйте OpenAPI спецификацию

## Примеры рабочих процессов

### Разработка новой функции
1. **Анализ БД**: `list_tables` → `get_schema`
2. **Поиск документации**: Запрос к flask-docs
3. **Генерация кода**: `generate_model` → `generate_route`
4. **Тестирование**: `pg_query` для проверки данных

### Отладка проблем
1. **Проверка данных**: `pg_query` с диагностическими запросами
2. **Анализ схемы**: `get_schema` для понимания структуры
3. **Поиск решений**: Запросы к документации Flask/SQLAlchemy