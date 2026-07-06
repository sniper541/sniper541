# -*- coding: utf-8 -*-
import json
import sys

# Настройка кодировки вывода
sys.stdout.reconfigure(encoding='utf-8')

# Абсолютный путь к файлу
JSON_FILE_PATH = "/var/www/sniper541.ru/html/sites/game/games.json"

def load_json(file_path=JSON_FILE_PATH):
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {"games": [], "statistics": {"years": {}}, "total_count": 0}

def save_json(data, file_path=JSON_FILE_PATH):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def add_game(name, image_url, date):
    data = load_json()
    total_count = data["total_count"] + 1
    new_game = {
        "name": name,
        "image_url": image_url,
        "date": date,
        "number": total_count
    }
    data["games"].insert(0, new_game)

    for i, game in enumerate(data["games"], 1):
        game["number"] = i

    update_statistics(data)
    data["total_count"] = total_count
    save_json(data)
    print("Игра успешно добавлена!")

def delete_game(number):
    data = load_json()
    try:
        number = int(number)
        games = data["games"]
        if 1 <= number <= len(games):
            del games[number - 1]
            for i, game in enumerate(games, 1):
                game["number"] = i
            update_statistics(data)
            data["total_count"] = len(games)
            save_json(data)
            print(f"Игра под номером {number} удалена!")
        else:
            print("Некорректный номер игры.")
    except ValueError:
        print("Ошибка: Номер должен быть числом.")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def edit_game(number, name=None, image_url=None, date=None):
    data = load_json()
    try:
        number = int(number)
        games = data["games"]
        if 1 <= number <= len(games):
            game = games[number - 1]
            game["name"] = name if name is not None else game["name"]
            game["image_url"] = image_url if image_url is not None else game["image_url"]
            game["date"] = date if date is not None else game["date"]
            update_statistics(data)
            save_json(data)
            print(f"Игра №{number} успешно отредактирована!")
        else:
            print("Некорректный номер игры.")
    except ValueError:
        print("Ошибка: Номер должен быть числом.")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def update_statistics(data):
    games = data["games"]
    stats = {"years": {}}
    for game in games:
        year = game["date"].split()[-1] if game["date"] else "Unknown"
        stats["years"][year] = stats["years"].get(year, 0) + 1
    data["statistics"] = stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 add_game.py <действие> [аргументы]")
        print("Действия: add, delete, edit")
        print("Пример добавления: python3 add_game.py add 'Название' 'Ссылка' 'октябрь 2024'")
        print("Пример удаления: python3 add_game.py delete 1")
        print("Пример редактирования: python3 add_game.py edit 1 'Новое название' '' 'ноябрь 2024'")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "add" and len(sys.argv) == 5:
        add_game(sys.argv[2], sys.argv[3], sys.argv[4])
    elif action == "delete" and len(sys.argv) == 3:
        delete_game(sys.argv[2])
    elif action == "edit" and len(sys.argv) >= 3:
        args = sys.argv[2:] + [""] * (5 - len(sys.argv))  # Дополняем пустыми строками
        edit_game(args[0], args[1] or None, args[2] or None, args[3] or None)
    else:
        print("Неверные аргументы. Используйте: add <name> <image_url> <date>, delete <number>, или edit <number> [name] [image_url] [date]")
        sys.exit(1)