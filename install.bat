@echo off
echo Переустановка зависимостей Flask приложения...

echo Удаление старых зависимостей...
pip uninstall -y Flask Flask-SQLAlchemy Flask-Migrate Flask-WTF WTForms Werkzeug python-dotenv

echo Установка новых зависимостей...
pip install -r requirements.txt

echo Готово! Теперь можно запускать приложение командой: python app.py
pause