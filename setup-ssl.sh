#!/bin/bash
# Скрипт для получения SSL сертификата через certbot

# Установка certbot (если не установлен)
# sudo apt-get update
# sudo apt-get install -y certbot python3-certbot-nginx

# Остановка nginx контейнера перед получением сертификата
docker-compose stop nginx

# Получение сертификата (certbot должен быть установлен на хосте, не в контейнере)
sudo certbot certonly --standalone -d aromabay.site -d www.aromabay.site

# После получения сертификата запустите контейнеры снова
# docker-compose up -d

echo "✅ Сертификат получен! Теперь запустите: docker-compose up -d"

