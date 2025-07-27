# Flask Web Application

Веб-приложение на Flask с четкой архитектурой и разделением компонентов.

## Структура проекта

```
project/
├── app.py              # Основной файл приложения
├── config.py           # Конфигурация проекта
├── forms.py            # Веб-формы
├── models.py           # Модели данных
├── requirements.txt    # Зависимости Python
├── migrations/         # Миграции базы данных
├── static/            # Статические файлы
│   ├── css/           # CSS стили
│   └── js/            # JavaScript файлы
└── templates/         # HTML шаблоны
    ├── base.html      # Базовый шаблон
    ├── index.html     # Главная страница
    └── contact.html   # Страница контактов
```

## Установка и запуск

1. Создайте виртуальное окружение:
```bash
python -m venv .venv
```

2. Активируйте виртуальное окружение:
```bash
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env на основе .env.example:
```bash
cp .env.example .env
```

5. Инициализируйте базу данных:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Запустите приложение:
```bash
python app.py
```

Приложение будет доступно по адресу: http://localhost:5000

## Компоненты архитектуры

- **app.py** — точка входа в приложение, настройка Flask и маршруты
- **config.py** — централизованная конфигурация с поддержкой переменных окружения
- **forms.py** — классы форм с валидацией на основе WTForms
- **models.py** — модели данных для работы с базой данных через SQLAlchemy
- **migrations/** — версионирование схемы базы данных
- **static/** — статические ресурсы (CSS, JS, изображения)
- **templates/** — HTML шаблоны с использованием Jinja2