@echo off
echo Запуск системы управления инцидентами Stockmann...

echo Проверка базы данных...
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', user='postgres', password='1234', database='stockmann_incidents'); print('База данных доступна'); conn.close()" 2>nul
if errorlevel 1 (
    echo ОШИБКА: База данных недоступна!
    echo Убедитесь что:
    echo 1. PostgreSQL запущен
    echo 2. База данных stockmann_incidents создана
    echo 3. Настройки в .env файле корректны
    echo.
    echo Для инициализации БД запустите: python database/init_db.py
    pause
    exit /b 1
)

echo База данных подключена успешно!
echo.
echo Запуск Flask приложения...
echo Приложение будет доступно по адресу: http://localhost:5000
echo.
echo Тестовые учетные записи:
echo - admin / 12345 (Администратор)
echo - anna.virtanen / password (Менеджер Helsinki)
echo - security.hel / security123 (Безопасность)
echo.

python app.py
pause