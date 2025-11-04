# 1. Используем официальный базовый образ Python
FROM python:3.9-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем остальной код нашего приложения
COPY . .

# 5. Указываем команду для запуска нашего сервиса
# Мы используем Gunicorn для запуска Flask-приложения
# "app:app" означает "в файле app.py найди объект app"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]