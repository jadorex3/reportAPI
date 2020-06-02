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


def todo_list():
    completed = ''
    not_completed = ''

    for todo in TODOS:
        if user['id'] == todo.get('userId'):
            if todo['completed']:
                if len(todo['title']) <= 50:
                    completed += f"{todo['title']}\n"
                else:
                    completed += f"{todo['title'][:50]}...\n"
            elif not todo['completed']:
                if len(todo['title']) <= 50:
                    not_completed += f"{todo['title']}\n"
                else:
                    not_completed += f"{todo['title'][:50]}...\n"
    return completed, not_completed


for user in USERS:
    todo_list()
    if 'username' in user:
        with open(f'tasks/{user["username"]}.txt', 'w', encoding='utf-8') as file:
            file.write(
                f"""
{user['name']} <{user["email"]}> {datetime.today().strftime('%d.%m.%Y %H:%M')}
{user["company"]["name"]}

Завершенные задачи:
{todo_list()[0]}

Оставшиеся задачи:
{todo_list()[1]}
""")
