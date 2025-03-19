# Функция для валидации дедлайна (ожидаем формат DD-MM-YYYY)

from  flask import Flask, request,jsonify
from datetime import datetime

app = Flask(__name__)

tasks = [] # Список для хранения задач

def validate_deadline(deadline):
    """Проверка что строка соответсвует формату 'DD-MM-YYYY' """
    try:
        datetime.strptime(deadline, "%d-%m-%y")
        return True
    except ValueError:
        return False

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    #Проверка на то что заполнены все поля
    if not all(k in data for k in ["title","description","deadline"]):
        return jsonify({"error": "Заполните поля"}), 400

        #Новая задача
    task = {
        "id": len(tasks)+1,
        "title": data["title"],
        "description": data["description"],
        "deadline": data["dataline"]
    }

    tasks.append(task) # Добавление в список
    return jsonify(task), 201 #Возращение созданной задачи с кодом 201



@app.route("/tasks", methods= ["GET"])
def get_tasks():
    sorted_tasks = sorted(tasks, key=lambda x:datetime.strptime(x["deadline"], "%d-%m-%Y"))
    return jsonify(sorted_tasks)

@app.route("/tasks/<int:task_id>", methods= ["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [tasks for task in tasks if task["id"] != task_id]

    return jsonify({"message": "Задача удалена"}), 200

@app.route("/")
def home():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)

"""
Улучшения:
1. Использовать базу данных (например, SQLite или PostgreSQL) вместо списка в памяти.
2. Добавить проверку дубликатов задач перед добавлением.
3. Использовать UUID вместо числового ID, чтобы избежать конфликтов.
4. Реализовать обновление задач (PUT /tasks/<id>).
5. Добавить логирование и обработку ошибок.
"""