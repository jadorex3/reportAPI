"""
Есть API для получения списка задач и api для получения списка юзеров:
https://json.medrating.org/todos
https://json.medrating.org/users
Используя только эти API составить отчёты по всем юзерам в отдельных текстовых файлах.
"""

import os
import json
import urllib.request
from datetime import datetime

if not os.path.exists('tasks'):
    os.mkdir('tasks')

with urllib.request.urlopen("https://json.medrating.org/users") as url:
    USERS = json.loads(url.read().decode())

with urllib.request.urlopen("https://json.medrating.org/todos") as url:
    TODOS = json.loads(url.read().decode())


def three_dots(string, ln=50):
    """Срезает строку до ln и стовит '...' """
    string = f"{string[:ln]}...\n" if string[ln:] else f"{string}\n"
    return string


def todo_list(id_user):
    """Формирует строку выполненных и невыполненых заданий id_user пользователя"""
    completed = ''
    not_completed = ''

    for todo in TODOS:
        if id_user == todo.get('userId'):
            if todo['completed']:
                completed += three_dots(todo['title'])
            else:
                not_completed += three_dots(todo['title'])
    return completed, not_completed


for user in USERS:
    COMPLETED, NOT_COMPLETED = todo_list(user.get('id'))
    if 'username' in user:
        PATH = f"tasks/{user['username']}.txt"

    if os.path.exists(PATH):
        pass  # Проверка существования файла
    else:
        with open(PATH, 'w', encoding='utf-8') as file:
            file.write(
                f"{user['name']} <{user['email']}> {datetime.today().strftime('%d.%m.%Y %H:%M')}\n"
                f"{user['company']['name']}\n"
                f"\n"
                f"Завершенные задачи:\n"
                f"{COMPLETED}\n"
                f"Оставшиеся задачи:\n"
                f"{NOT_COMPLETED}\n"
            )
