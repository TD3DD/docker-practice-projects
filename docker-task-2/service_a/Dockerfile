# Базовий образ Python
FROM python:3.9-slim
WORKDIR /app

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код
COPY . .

# Порт, на якому Gunicorn буде слухати (всередині контейнера)
EXPOSE 5001

# Запускаємо сервіс
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]