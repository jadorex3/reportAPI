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


def todo_list(id_user):
    """Формирует строку выполненных и невыполненых заданий пользователя"""
    completed = ''
    not_completed = ''

    for todo in TODOS:
        if id_user == todo.get('userId'):
            if todo['completed']:
                if len(todo['title']) <= 50:
                    completed += f"{todo['title']}\n"
                else:
                    completed += f"{todo['title'][:50]}...\n"
            else:
                if len(todo['title']) <= 50:
                    not_completed += f"{todo['title']}\n"
                else:
                    not_completed += f"{todo['title'][:50]}...\n"
    return completed, not_completed


for user in USERS:
    COMPLETED, NOT_COMPLETED = todo_list(user.get('id'))

    if 'username' in user:
        with open(f'tasks/{user["username"]}.txt', 'w', encoding='utf-8') as file:
            file.write(
                f"""
{user['name']} <{user["email"]}> {datetime.today().strftime('%d.%m.%Y %H:%M')}
{user["company"]["name"]}

Завершенные задачи:
{COMPLETED}

Оставшиеся задачи:
{NOT_COMPLETED}
                """)
