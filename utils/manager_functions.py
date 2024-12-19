import sqlite3


def show_all_orders():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders")
    orders = cursor.fetchall()
    conn.close()

    if orders:
        for order in orders:
            print(f"ID: {order[0]}, Название: {order[2]}, Статус: {order[3]}, Ответственный: ID-{order[4]}")
    else:
        print("Нет заказов для отображения.")


def approve_or_reject_order(order_id, action, manager_id):
    if action == "одобрить":
        new_status = "Одобрен"
    elif action == "отклонить":
        new_status = "Отклонён"
    else:
        print("Неверное действие. Выберите 'одобрить' или 'отклонить'.")
        return

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE Orders SET status = ? WHERE id = ?", (new_status, order_id))

    if new_status == "Одобрен":
        cursor.execute("UPDATE Orders SET responsible_id = ? WHERE id = ?", (manager_id, order_id))
        print(f"Заказ {order_id} был одобрен. Менеджер ID-{manager_id} назначен ответственным за заказ.")
    else:
        print(f"Заказ {order_id} был отклонен.")

    conn.commit()
    conn.close()


def update_order_status(order_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM Orders WHERE id = ?", (order_id,))
    result = cursor.fetchone()

    if not result:
        print(f"Заказ с ID {order_id} не найден.")
        conn.close()
        return

    current_status = result[0]

    if current_status == "Одобрен":
        new_status = "Отклонён"
    elif current_status == "Отклонён":
        new_status = "Одобрен"
    else:
        print(f"Неизвестный статус '{current_status}' для заказа {order_id}.")
        conn.close()
        return

    cursor.execute("UPDATE Orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

    print(f"Статус заказа {order_id} изменён с '{current_status}' на '{new_status}'.")
