@echo off
echo Установка зависимостей...
pip install -r requirements.txt

echo Сбор статических файлов...
python manage.py collectstatic --noinput

echo Применение миграций...
python manage.py migrate

echo Build завершен!