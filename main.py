import re
from werkzeug.security import generate_password_hash, check_password_hash

from src.customer_functions import *
from src.manager_functions import *
from src.warehouse_functions import *
from src.director_functions import *

def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        order_name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES Users(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Materials (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        material_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        unit_price REAL NOT NULL)''')

    conn.commit()
    conn.close()


def validate_username(username):
    min_length = 3
    max_length = 16

    if len(username) < min_length:
        print(f"Длина имени пользователя должна составлять не менее {min_length} символов.")
        return False
    if len(username) > max_length:
        print(f"Длина имени пользователя не должна превышать {max_length} символов.")
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        print("Имя пользователя может содержать только буквы, цифры и символы подчеркивания.")
        return False
    return True


def validate_password(password):
    min_length = 6
    max_length = 20

    if len(password) < min_length:
        print(f"Длина пароля должна составлять не менее {min_length} символов.")
        return False
    if len(password) > max_length:
        print(f"Длина пароля не должна превышать {max_length} символов.")
        return False
    if not re.search(r'[A-Z]', password):
        print("Пароль должен содержать хотя бы одну заглавную букву.")
        return False
    if not re.search(r'[a-z]', password):
        print("Пароль должен содержать хотя бы одну строчную букву.")
        return False
    if not re.search(r'[0-9]', password):
        print("Пароль должен содержать хотя бы одну цифру.")
        return False
    if not re.search(r'[!@#$%^]', password):
        print("Пароль должен содержать хотя бы один специальный символ (!@#$%^).")
        return False
    return True


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


def customer_screen(user_id):
    while True:
        print("\nЭкран заказчика:")
        print("1. Создать заказ")
        print("2. Редактировать заказ")
        print("3. Просмотреть мои заказы")
        print("4. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            order_name = input("Введите название заказа: ")
            create_order(user_id, order_name)
        elif choice == '2':
            order_id = int(input("Введите ID заказа для редактирования: "))
            new_order_name = input("Введите новое название заказа: ")
            update_order(user_id, order_id, new_order_name)
        elif choice == '3':
            show_user_orders(user_id)
        elif choice == '4':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def manager_screen():
    while True:
        print("\nЭкран менеджера:")
        print("1. Просмотреть все заказы")
        print("2. Одобрить/Отклонить заказ")
        print("3. Изменить статус заказа")
        print("4. Просмотреть все материалы")
        print("5. Обновить материал")
        print("6. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            show_orders(0)  # Просмотр всех заказов
        elif choice == '2':
            change_order_status()  # Мини-функция для изменения статуса заказа
        elif choice == '3':
            change_order_status()  # Мини-функция для изменения статуса заказа
        elif choice == '4':
            show_materials()  # Мини-функция для просмотра материалов
        elif choice == '5':
            update_material_info()  # Мини-функция для обновления материала
        elif choice == '6':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def warehouse_screen():
    while True:
        print("\nЭкран кладовщика:")
        print("1. Добавить материал")
        print("2. Просмотреть все материалы")
        print("3. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            material_name = input("Введите название материала: ")
            quantity = int(input("Введите количество: "))
            unit_price = float(input("Введите цену единицы: "))
            add_material(material_name, quantity, unit_price)
        elif choice == '2':
            show_materials()  # Мини-функция для просмотра материалов
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def director_screen():
    while True:
        print("\nЭкран директора:")
        print("1. Просмотреть все заказы")
        print("2. Просмотреть все материалы")
        print("3. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            show_orders(0)  # Просмотр всех заказов
        elif choice == '2':
            show_materials()  # Мини-функция для просмотра материалов
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def main():
    create_db()

    while True:
        print("\nГлавное меню:")
        print("1. Регистрация")
        print("2. Вход")
        print("3. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            role = input("Введите роль (заказчик/менеджер/кладовщик/руководитель): ")
            register_user(username, password, role)
        elif choice == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            user = login_user(username, password)
            if user:
                if user[3] == 'заказчик':
                    customer_screen(user[0])
                elif user[3] == 'менеджер':
                    manager_screen()
                elif user[3] == 'кладовщик':
                    warehouse_screen()
                elif user[3] == 'руководитель':
                    director_screen()
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
