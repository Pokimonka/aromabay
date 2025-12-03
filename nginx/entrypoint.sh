#!/bin/sh
# Entrypoint скрипт для nginx, который проверяет наличие SSL сертификатов

set -e

# Проверяем наличие SSL сертификатов
if [ -f /etc/letsencrypt/live/aromabay.site/fullchain.pem ] && \
   [ -f /etc/letsencrypt/live/aromabay.site/privkey.pem ]; then
    echo "✅ SSL сертификаты найдены, включаем HTTPS"
    # Генерируем конфигурацию с SSL
    cat > /etc/nginx/conf.d/default.conf << 'EOF'
# Редирект с HTTP на HTTPS для домена
server {
    listen 80;
    server_name aromabay.site www.aromabay.site;
    return 301 https://$server_name$request_uri;
}

# Конфигурация для работы по IP-адресу (без SSL)
server {
    listen 80 default_server;
    server_name _;

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# HTTPS конфигурация для домена
server {
    listen 443 ssl http2;
    server_name aromabay.site www.aromabay.site;

    ssl_certificate /etc/letsencrypt/live/aromabay.site/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/aromabay.site/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF
else
    echo "⚠️ SSL сертификаты не найдены, используем базовую HTTP конфигурацию"
    # Базовая конфигурация уже скопирована из nginx.conf в Dockerfile
    # Просто используем её как есть
fi

# Запускаем nginx
exec nginx -g 'daemon off;'

