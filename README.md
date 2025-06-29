# Сервис управления рассылками (Django)

Первая часть курсового проекта: реализация административного интерфейса для рассылки писем клиентам.

## Возможности

- CRUD для клиентов (email, ФИО, комментарий)
- CRUD для сообщений (тема, тело письма)
- CRUD для рассылок (период действия, статус, получатели)
- Ручной запуск рассылок
- Учёт попыток отправки (успешно/неуспешно, ответ сервера)
- Главная страница со статистикой:
  - общее число рассылок;
  - активные рассылки (статус "Запущена");
  - уникальные получатели.

## Запуск проекта

```bash
git clone <repo>
cd mailing_service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Настройки почты

В `settings.py` или `.env`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

Для теста:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Стек

- Python 3.12+
- Django 4+
- Bootstrap 5 (для UI)

## Структура

- `mailings/` — приложение рассылки
- `templates/mailings/` — шаблоны
- `utils.py` — логика отправки писем
