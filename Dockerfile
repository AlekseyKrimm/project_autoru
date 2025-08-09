# Dockerfile
FROM python:3.13.5-slim

# Создаем пользователя для приложения
RUN groupadd -r django && useradd -r -g django django

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем директории и устанавливаем права доступа
RUN mkdir -p /app/staticfiles /app/media /app/data && \
    chown -R django:django /app && \
    chmod -R 755 /app && \
    chmod -R 775 /app/data /app/media /app/staticfiles

# Создаем скрипт запуска
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && chown django:django /app/entrypoint.sh

# Переключаемся на пользователя django
USER django

# Открываем порт
EXPOSE 8000

# Точка входа
ENTRYPOINT ["/app/entrypoint.sh"]

# Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "autoru.wsgi:application"]