# sniper541

Personal website and Telegram helper bot for managing content on
[sniper541.ru](https://sniper541.ru).

![Home page](docs/screenshots/home.png)

## Project Structure

```text
.
├── site/                 # Website files served by nginx
├── bot/                  # Telegram bot for updating books and games
├── nginx/                # nginx virtual host config
├── docs/screenshots/     # README assets
├── .env.example          # Example environment variables
└── .gitignore
```

## Website

The website is a small personal hub with separate sections for games, books,
resume, and map pages.

The production nginx config serves the site from:

```text
/var/www/sniper541.ru/html
```

When this repository is used as the source of truth, that path can be symlinked
to:

```text
project/sniper541/site
```

## Telegram Bot

The bot updates JSON data files used by the book and game sections.

Main files:

```text
bot/bot.py
bot/logic.py
bot/config.py
```

The bot reads secrets and runtime paths from `bot/.env`. The real `.env` file is
not committed.

Create it from the example:

```bash
cp bot/.env.example bot/.env
```

Required variables:

```env
BOT_TOKEN=
GAME_JSON=/var/www/sniper541.ru/html/sites/game/games.json
BOOK_JSON=/var/www/sniper541.ru/html/sites/book/books.json
```

Run the bot:

```bash
cd bot
python bot.py
```

## nginx

The nginx config is stored in:

```text
nginx/sniper541.ru
```

Production location:

```text
/etc/nginx/sites-available/sniper541.ru
```

After changing nginx config:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Secrets

Do not commit real tokens, passwords, logs, or cache files. They are ignored by
`.gitignore`:

```text
.env
*.log
nohup.out
__pycache__/
*.pyc
.idea/
```

## Deploy Notes

Recommended production layout:

```text
project/sniper541/site  -> /var/www/sniper541.ru/html
project/sniper541/bot   -> /root/tgbot/mylife
project/sniper541/nginx/sniper541.ru -> /etc/nginx/sites-available/sniper541.ru
```

The repository should contain the clean project files. Server-only secrets stay
in `.env` files on the server.