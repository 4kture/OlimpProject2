from src.screens import *
from src.authorization import *


def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            order_name TEXT NOT NULL,
                            status TEXT NOT NULL,
                            responsible_id INTEGER
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Materials (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        material_name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        unit_price REAL NOT NULL
                    )''')

    conn.commit()
    conn.close()


def insert_multiple_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    materials_data = [
        ('Материал 1', 100, 50.0),
        ('Материал 2', 200, 30.0),
        ('Материал 3', 150, 45.0)
    ]
    cursor.executemany("INSERT INTO Materials (material_name, quantity, unit_price) VALUES (?, ?, ?)", materials_data)

    conn.commit()
    conn.close()
    print("Данные успешно вставлены.")


def main():
    create_db()

    while True:
        print("\nГлавное меню:")
        print("1. Вход")
        print("2. Регистрация")
        print("3. Выход")
        choice = input("Выберите опцию: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            user = login_user(username, password)
            if user:
                if user[3] == 'заказчик':
                    customer_screen(user[0])
                elif user[3] == 'менеджер':
                    manager_screen(user[0])
                elif user[3] == 'кладовщик':
                    warehouse_screen()
                elif user[3] == 'руководитель':
                    director_screen()
        elif choice == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            role = input("Введите роль (заказчик/менеджер/кладовщик/руководитель): ")
            register_user(username, password, role)
        elif choice == '3':
            print("Выход...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
