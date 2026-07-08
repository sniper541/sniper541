#!/bin/bash
set -e

PROJECT_DIR="/opt/project/sniper541"
NGINX_CONF="$PROJECT_DIR/nginx/sniper541.ru"
NGINX_AVAILABLE="/etc/nginx/sites-available/sniper541.ru"
NGINX_ENABLED="/etc/nginx/sites-enabled/sniper541.ru"
SYSTEMD_SERVICE="$PROJECT_DIR/systemd/mylife.service"
SYSTEMD_LINK="/etc/systemd/system/mylife.service"

echo "==> Checking project directory"
test -d "$PROJECT_DIR"
test -f "$NGINX_CONF"
test -f "$SYSTEMD_SERVICE"

echo "==> Checking required commands"
command -v nginx >/dev/null
command -v python3 >/dev/null
command -v systemctl >/dev/null

echo "==> Checking bot .env"
if [ ! -f "$PROJECT_DIR/bot/.env" ]; then
    echo "ERROR: $PROJECT_DIR/bot/.env not found"
    echo "Create it from bot/.env.example"
    exit 1
fi

echo "==> Linking nginx config"
rm -f "$NGINX_AVAILABLE"
ln -s "$NGINX_CONF" "$NGINX_AVAILABLE"

rm -f "$NGINX_ENABLED"
ln -s "$NGINX_AVAILABLE" "$NGINX_ENABLED"

echo "==> Testing nginx"
nginx -t

echo "==> Reloading nginx"
systemctl reload nginx

echo "==> Linking systemd service"
rm -f "$SYSTEMD_LINK"
ln -s "$SYSTEMD_SERVICE" "$SYSTEMD_LINK"

echo "==> Starting bot service"
systemctl daemon-reload
systemctl enable mylife
systemctl restart mylife

echo "==> Status"
systemctl --no-pager status mylife || true

echo "DONE: sniper541 installed"
