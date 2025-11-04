FROM python:3.9-slim
WORKDIR /app

# 
# !!! ДОДАЙТЕ ЦІ РЯДКИ ДЛЯ ВСТАНОВЛЕННЯ CURL !!!
#
RUN apt-get update && apt-get install -y curl --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
#
# (Кінець доданого коду)
#

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Backend слухає на порту 5001 (всередині Docker)
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]