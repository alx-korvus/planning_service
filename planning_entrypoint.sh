#!/bin/sh

# Выходить из скрипта при любой ошибке
set -e

# применяем миграции базы данных
echo "Applying database migrations..."
python manage.py migrate

# собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --no-input

# создаем суперпользователя (если его нет)
echo "Initializing admin..."
python manage.py initadmin

# (ТОЛЬКО ДЛЯ ТЕСТОВОГО ЗАПУСКА!!!) создаем несколько пользователей
echo "Creating fake users..."
python manage.py fake_users

# запускаем основной процесс (Gunicorn), который передан как команда в docker-compose.
# exec "$@" заменяет текущий процесс скрипта на Gunicorn,
# что позволяет ему корректно получать сигналы от Docker.
exec "$@"
