import json
from config import GAME_JSON, BOOK_JSON

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"games": []} if "game" in path else {"books": []}

def save_json(path, data):
    if "games" in data:
        data["total_count"] = len(data["games"])
    elif "books" in data:
        data["total_count"] = len(data["books"])

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_game(name, image_url, date):
    data = load_json(GAME_JSON)
    games = data.get("games", [])
    games.insert(0, {
        "name": name,
        "image_url": image_url,
        "date": date,
        "number": 1
    })
    for i, g in enumerate(games, 1):
        g["number"] = i
    save_json(GAME_JSON, {"games": games})

def add_book(title, author, image_url, year):
    data = load_json(BOOK_JSON)
    books = data.get("books", [])
    books.insert(0, {
        "title": title,
        "author": author,
        "image_url": image_url,
        "year": year,
        "number": 1
    })
    for i, b in enumerate(books, 1):
        b["number"] = i
    save_json(BOOK_JSON, {"books": books})

def delete_game_by_number(number):
    data = load_json(GAME_JSON)
    games = [g for g in data.get("games", []) if g["number"] != number]
    for i, g in enumerate(games, 1):
        g["number"] = i
    save_json(GAME_JSON, {"games": games})

def delete_book_by_number(number):
    data = load_json(BOOK_JSON)
    books = [b for b in data.get("books", []) if b["number"] != number]
    for i, b in enumerate(books, 1):
        b["number"] = i
    save_json(BOOK_JSON, {"books": books})
