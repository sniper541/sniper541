from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Путь к файлу data.json (в той же директории)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# Пароль для редактирования
EDIT_PASSWORD = "masters"

# Инициализация файла, если его нет
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Загрузка меток
@app.route('/get_places', methods=['GET'])
def get_places():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

# Сохранение меток
@app.route('/save_places', methods=['POST'])
def save_places():
    # Проверка пароля
    password = request.headers.get('X-Edit-Password')
    if password != EDIT_PASSWORD:
        return jsonify({'error': 'Неверный пароль'}), 403

    data = request.get_json()
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)