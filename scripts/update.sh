#!/bin/bash
set -e

PROJECT_DIR="/opt/project/sniper541"

cd "$PROJECT_DIR"

echo "==> Pulling latest changes"
git pull

echo "==> Testing nginx"
nginx -t

echo "==> Reloading nginx"
systemctl reload nginx

echo "==> Restarting bot"
systemctl restart mylife

echo "==> Status"
systemctl --no-pager status mylife || true

echo "DONE: sniper541 updated"
