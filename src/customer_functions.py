import sqlite3


def create_order(user_id, order_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Orders (user_id, order_name, status) VALUES (?, ?, ?)",
                   (user_id, order_name, "Новый"))
    conn.commit()
    conn.close()
    print(f"Заказ '{order_name}' успешно создан!")


def update_order(user_id, order_id, new_order_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders WHERE id = ? AND user_id = ? AND status = 'Новый'", (order_id, user_id))
    order = cursor.fetchone()

    if order:
        cursor.execute("UPDATE Orders SET order_name = ? WHERE id = ?", (new_order_name, order_id))
        conn.commit()
        print(f"Заказ {order_id} успешно обновлен!")
    else:
        print("Ошибка: заказ не найден или уже был проверен менеджером.")

    conn.close()


def show_user_orders(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders WHERE user_id = ?", (user_id,))
    orders = cursor.fetchall()
    conn.close()

    if orders:
        for order in orders:
            print(f"ID: {order[0]}, Название: {order[2]}, Статус: {order[3]}")
    else:
        print("У вас нет заказов.")