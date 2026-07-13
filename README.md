# sniper541

Personal website and Telegram bot for managing content on **sniper541.ru**.

The repository contains everything required for the project except secrets
(Telegram token, SSL certificates, etc.).

---

# Project structure

```
sniper541/

├── site/                 # Website
├── bot/                  # Telegram bot
├── nginx/                # nginx configuration
├── systemd/              # systemd services
├── scripts/              # install / update / uninstall
├── docs/
├── README.md
└── .gitignore
```

---

# Architecture

The project lives entirely inside:

```
/opt/project/sniper541
```

Nothing inside the application depends on `/var/www`.

The project itself is the source of truth.

Server directories (`/etc/nginx`, `/etc/systemd`, etc.) only contain symbolic
links to files stored inside the project.

---

# Requirements

Ubuntu 22.04+

Installed:

- nginx
- php8.1-fpm
- python3
- certbot (optional)
- git

---

# Installation

Clone repository

```bash
git clone <repository>
cd /opt/project/sniper541
```

Create bot configuration

```bash
cp bot/.env.example bot/.env
nano bot/.env
```

Example

```env
BOT_TOKEN=

GAME_JSON=/opt/project/sniper541/site/sites/game/games.json
BOOK_JSON=/opt/project/sniper541/site/sites/book/books.json
```

Run installer

```bash
sudo ./scripts/install.sh
```

Installer automatically:

- checks required software
- installs nginx configuration
- enables nginx site
- tests nginx configuration
- reloads nginx
- installs systemd service
- enables Telegram bot
- starts Telegram bot

---

# Updating

```bash
cd /opt/project/sniper541

git pull

sudo ./scripts/update.sh
```

---

# Uninstall

```bash
sudo ./scripts/uninstall.sh
```

Project files are not removed.

---

# Website

Website files are located in

```
site/
```

nginx serves files directly from

```
/opt/project/sniper541/site
```

---

# Telegram Bot

Location

```
bot/
```

Start manually

```bash
cd bot

python3 bot.py
```

Production uses systemd.

Configuration

```
bot/.env
```

Example

```
bot/.env.example
```

---

# nginx

Project configuration

```
nginx/sniper541.ru
```

Installed as

```
/etc/nginx/sites-available/sniper541.ru
```

through a symbolic link.

---

# systemd

Service definition

```
systemd/mylife.service
```

Installed as

```
/etc/systemd/system/mylife.service
```

through a symbolic link.

Useful commands

```bash
systemctl status mylife

systemctl restart mylife

journalctl -u mylife -f
```

---

# Secrets

Never commit

- .env
- Telegram tokens
- passwords
- SSL certificates
- logs

---

# .gitignore

```
.env
*.log
*.pyc
__pycache__/
.idea/
.vscode/
```

---

# Repository philosophy

Everything that can be versioned is stored inside the repository.

Server configuration only contains symbolic links.

This allows deploying the whole project on a new server by cloning the
repository and running

```bash
sudo ./scripts/install.sh
```