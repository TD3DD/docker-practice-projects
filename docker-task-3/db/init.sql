/* Створюємо таблицю, якщо її ще не існує */
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

/* Додаємо початкові дані (тільки якщо таблиця порожня) */
INSERT INTO users (name) 
VALUES ('Alice (from DB)'), ('Bob (from DB)')
ON CONFLICT DO NOTHING;