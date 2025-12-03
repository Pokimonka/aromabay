FROM nginx:alpine

# Копируем entrypoint скрипт
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Копируем базовую конфигурацию (будет заменена entrypoint.sh при наличии SSL)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Используем наш entrypoint
ENTRYPOINT ["/entrypoint.sh"]

