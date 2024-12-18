import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from src.validate import *


def register_user(username, password, role):
    allowed_roles = ["заказчик", "менеджер", "кладовщик", "руководитель"]

    if not validate_username(username):
        return

    if not validate_password(password):
        return

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print(f"Пользователь с никнеймом {username} уже существует.")
        conn.close()
        return

    if role.lower() not in allowed_roles:
        print(f"Некорректная роль. Допустимые роли: {', '.join(allowed_roles)}.")
        return

    password_hash = generate_password_hash(password)
    cursor.execute("INSERT INTO Users (username, password_hash, role) VALUES (?, ?, ?)",
                   (username, password_hash, role))
    conn.commit()
    conn.close()
    print(f"Пользователь {username} успешно зарегистрирован!")


def login_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        print(f"Добро пожаловать, {username}!")
        return user
    else:
        print("Неверное имя пользователя или пароль.")
        return None