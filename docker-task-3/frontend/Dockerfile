# Базовий образ Nginx
FROM nginx:alpine

# Копіюємо наш сайт (index.html)
COPY index.html /usr/share/nginx/html/index.html

# Видаляємо стандартний конфіг Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Копіюємо наш власний конфіг
COPY nginx.conf /etc/nginx/conf.d/custom.conf