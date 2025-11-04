import os
import time
import psycopg2
from psycopg2 import OperationalError
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    """
    Подключается к БД.
    Добавлен цикл повторных попыток, так как веб-сервис может запуститься
    быстрее, чем база данных будет готова принимать соединения.
    """
    retries = 5
    conn = None
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST'),  # Имя сервиса из docker-compose
                database=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                port=5432
            )
            print("Successfully connected to the database!")
            return conn
        except OperationalError as e:
            print(f"Database connection failed: {e}")
            retries -= 1
            print(f"Retrying connection... {retries} attempts left.")
            time.sleep(5)  # Ждем 5 секунд перед следующей попыткой
    
    print("Could not connect to the database after several attempts.")
    return None

def init_db():
    """Создает таблицу и добавляет начальных пользователей."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            # Создаем таблицу, если ее не существует
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                );
            """)
            
            # Добавляем начальных пользователей (только если таблица пустая)
            cur.execute("SELECT COUNT(*) FROM users;")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO users (name) VALUES (%s), (%s);",
                            ('Alice', 'Bob'))
                print("Initial users inserted.")

        conn.commit()
    except Exception as e:
        print(f"Error during DB initialization: {e}")
    finally:
        if conn:
            conn.close()

@app.route('/users')
def get_users():
    """Эндпоинт, который возвращает список пользователей из БД."""
    users_list = []
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Could not connect to database"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM users;")
            users = cur.fetchall()
            for user in users:
                users_list.append({"id": user[0], "name": user[1]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
            
    return jsonify(users_list)

# ... (код функції get_users) ...

# 
# !!! ВИКЛИКАЄМО ІНІЦІАЛІЗАЦІЮ БД ТУТ !!!
# Цей код виконається, коли Gunicorn імпортує файл.
#
print("--- Initializing Database (if needed) ---")
init_db()
print("--- Database Initialization Complete ---")


if __name__ == '__main__':
    # Цей блок тепер буде використовуватися, лише якщо ви
    # запустите файл напряму через "python app.py"
    print("Starting Flask application directly...")
    app.run(host='0.0.0.0', port=5000)