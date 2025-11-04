from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/info')
def get_info():
    """
    Ендпоінт, який повертає інформацію про сервіс.
    Саме сюди буде перенаправляти запити наш Nginx.
    """
    return jsonify({
        "service_name": "Service A",
        "status": "running",
        "message": "Hello from Service A! I was called via API Gateway."
    })

if __name__ == '__main__':
    # Gunicorn буде використовувати порт 5001 з Dockerfile
    app.run(host='0.0.0.0', port=5001)