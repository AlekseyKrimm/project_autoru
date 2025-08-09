#!/bin/bash
# entrypoint.sh

set -e

echo "Waiting for database directory to be ready..."

# Создаем директорию для базы данных если её нет
mkdir -p /app/data

# Проверяем права доступа
if [ ! -w "/app/data" ]; then
    echo "ERROR: No write permission to /app/data directory"
    ls -la /app/
    exit 1
fi

echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Creating superuser if not exists..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoru.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "Initializing data..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoru.settings')
django.setup()

from cars.models import CarBrand, CarModel

# Создаем базовые данные
brands_models = {
    'Toyota': ['Camry', 'Corolla', 'RAV4'],
    'BMW': ['3 Series', '5 Series', 'X3'],
    'Mercedes-Benz': ['C-Class', 'E-Class', 'GLC'],
}

for brand_name, models in brands_models.items():
    brand, created = CarBrand.objects.get_or_create(name=brand_name)
    if created:
        print(f'Created brand: {brand_name}')
    
    for model_name in models:
        model, created = CarModel.objects.get_or_create(
            brand=brand,
            name=model_name
        )
        if created:
            print(f'Created model: {brand_name} {model_name}')
"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"