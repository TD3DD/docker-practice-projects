import os
import time
import psycopg2
from psycopg2 import OperationalError
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    """Спроба підключення до БД з повторами."""
    retries = 5
    conn = None
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST'), # 'db' з docker-compose
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
            time.sleep(5)
    
    print("Could not connect to the database after several attempts.")
    return None

@app.route('/api/users')
def get_users():
    """Ендпоінт, який Frontend буде викликати."""
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

@app.route('/health')
def health_check():
    """(Бонус) Ендпоінт для healthcheck."""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Gunicorn буде запускати 'app'
    app.run(host='0.0.0.0', port=5001)