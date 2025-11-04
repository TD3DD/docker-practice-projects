# Використовуємо легкий офіційний образ Nginx
FROM nginx:alpine

# Видаляємо стандартний файл конфігурації Nginx
RUN rm /etc/nginx/nginx.conf

# Копіюємо наш власний файл конфігурації на його місце
COPY nginx.conf /etc/nginx/nginx.conf

# (Для документації) Nginx за замовчуванням слухає порт 80
EXPOSE 80