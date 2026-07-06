import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _load_env_file(path: Path):
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file(BASE_DIR / ".env")

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Create bot/.env from bot/.env.example.")

GAME_JSON = os.getenv("GAME_JSON", "/var/www/sniper541.ru/html/sites/game/games.json")
BOOK_JSON = os.getenv("BOOK_JSON", "/var/www/sniper541.ru/html/sites/book/books.json")