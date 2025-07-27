@echo off
echo Настройка MCP серверов для Kiro IDE...

echo Установка зависимостей MCP...
pip install mcp psycopg2-binary PyYAML

echo Создание каталогов...
if not exist ".kiro" mkdir .kiro
if not exist ".kiro\settings" mkdir .kiro\settings

echo Копирование переменных окружения...
if not exist ".env" copy .env.mcp .env

echo Проверка OpenAPI спецификации...
if not exist "api\openapi.yaml" (
    echo ВНИМАНИЕ: Файл api\openapi.yaml не найден!
    echo Создайте OpenAPI спецификацию для работы генератора кода.
)

echo.
echo MCP серверы настроены!
echo.
echo Доступные серверы:
echo 1. postgresql-server - SQL запросы к PostgreSQL
echo 2. flask-docs - Документация Flask/SQLAlchemy  
echo 3. openapi-codegen - Генерация кода по OpenAPI
echo.
echo Для активации перезапустите Kiro IDE
pause