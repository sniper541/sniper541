# -*- coding: utf-8 -*-
import json
import sys

# Настройка кодировки вывода
sys.stdout.reconfigure(encoding='utf-8')

# Абсолютный путь к файлу
JSON_FILE_PATH = "/opt/project/sniper541/site/sites/book/books.json"

def load_json(file_path=JSON_FILE_PATH):
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {"books": [], "statistics": {"years": {}}, "total_count": 0}

def save_json(data, file_path=JSON_FILE_PATH):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def add_book(title, author, image_url, year):
    data = load_json()
    total_count = data["total_count"] + 1
    new_book = {
        "title": title,
        "author": author,
        "image_url": image_url,
        "year": year,
        "number": total_count
    }
    data["books"].insert(0, new_book)

    for i, book in enumerate(data["books"], 1):
        book["number"] = i

    update_statistics(data)
    data["total_count"] = total_count
    save_json(data)
    print("Книга успешно добавлена!")

def delete_book(number):
    data = load_json()
    try:
        number = int(number)
        books = data["books"]
        if 1 <= number <= len(books):
            del books[number - 1]
            for i, book in enumerate(books, 1):
                book["number"] = i
            update_statistics(data)
            data["total_count"] = len(books)
            save_json(data)
            print(f"Книга под номером {number} удалена!")
        else:
            print("Некорректный номер книги.")
    except ValueError:
        print("Ошибка: Номер должен быть числом.")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def edit_book(number, title=None, author=None, image_url=None, year=None):
    data = load_json()
    try:
        number = int(number)
        books = data["books"]
        if 1 <= number <= len(books):
            book = books[number - 1]
            book["title"] = title if title is not None else book["title"]
            book["author"] = author if author is not None else book["author"]
            book["image_url"] = image_url if image_url is not None else book["image_url"]
            book["year"] = year if year is not None else book["year"]
            update_statistics(data)
            save_json(data)
            print(f"Книга №{number} успешно отредактирована!")
        else:
            print("Некорректный номер книги.")
    except ValueError:
        print("Ошибка: Номер должен быть числом.")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def update_statistics(data):
    books = data["books"]
    stats = {"years": {}}
    for book in books:
        stats["years"][book["year"]] = stats["years"].get(book["year"], 0) + 1
    data["statistics"] = stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 add_book.py <действие> [аргументы]")
        print("Действия: add, delete, edit")
        print("Пример добавления: python3 add_book.py add 'Название' 'Автор' 'Ссылка' 'Год'")
        print("Пример удаления: python3 add_book.py delete 1")
        print("Пример редактирования: python3 add_book.py edit 1 'Новое название' '' '' '2025'")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action == "add" and len(sys.argv) == 6:
        add_book(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif action == "delete" and len(sys.argv) == 3:
        delete_book(sys.argv[2])
    elif action == "edit" and len(sys.argv) >= 3:
        args = sys.argv[2:] + [""] * (6 - len(sys.argv))  # Дополняем пустыми строками
        edit_book(args[0], args[1] or None, args[2] or None, args[3] or None, args[4] or None)
    else:
        print("Неверные аргументы. Используйте: add <title> <author> <image_url> <year>, delete <number>, или edit <number> [title] [author] [image_url] [year]")
        sys.exit(1)