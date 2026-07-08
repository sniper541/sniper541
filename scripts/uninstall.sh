#!/bin/bash
set -e

echo "==> Stopping bot"
systemctl stop mylife || true
systemctl disable mylife || true

echo "==> Removing systemd link"
rm -f /etc/systemd/system/mylife.service
systemctl daemon-reload

echo "==> Removing nginx links"
rm -f /etc/nginx/sites-enabled/sniper541.ru
rm -f /etc/nginx/sites-available/sniper541.ru

echo "==> Testing nginx"
nginx -t

echo "==> Reloading nginx"
systemctl reload nginx

echo "DONE: sniper541 uninstalled from nginx/systemd"
echo "Project files in /opt/project/sniper541 were NOT deleted"
